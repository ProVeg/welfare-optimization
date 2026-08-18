"""Inequality-constrained optimal control: GEKKO collocation, SLSQP fallback.

Stack mapping: GEKKO IMODE=6 + IPOPT for the Bolza problem in
models/constrained-welfare-optimization.md §4–5. Path ceilings are inequalities
(variable upper bounds and g >= 0), never E == E_lim. GEKKO states are
nondimensional (Y/Y0, E/E_lim, P/P0, L/L0) so IPOPT is not asked to mix 1e10 with 1.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import dataclass

import numpy as np
from scipy.optimize import Bounds, NonlinearConstraint, minimize

from cwo.parameters import Params
from cwo.simulate import Trajectory, piecewise_control, simulate

GEKKO_TIMEOUT_SEC = 120


@dataclass
class OptResult:
    trajectory: Trajectory
    solver: str
    success: bool
    message: str
    J: float
    starts_tried: list[str]


def _interp_control(mesh: np.ndarray, u_w: np.ndarray, u_d: np.ndarray):
    def fn(tau: float) -> tuple[float, float]:
        return (
            float(np.clip(np.interp(tau, mesh, u_w), 0.0, 1.0)),
            float(np.clip(np.interp(tau, mesh, u_d), 0.0, 1.0)),
        )

    return fn


def _starts(n: int) -> list[tuple[str, np.ndarray, np.ndarray]]:
    ones = np.ones(n)
    zeros = np.zeros(n)
    mix = 0.7 * ones
    return [
        ("reduction_only", zeros, ones),
        ("joint", mix, mix),
        ("welfare_only", ones, zeros),
        ("bau", zeros, zeros),
    ]


def _gekko_solve(p: Params, u_w0: np.ndarray, u_d0: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    from gekko import GEKKO

    nt = len(u_w0)
    mesh = np.linspace(0.0, p.horizon_years, nt)
    y0 = p.Y0
    n0 = p.N0
    l0 = p.L0
    pi_q0 = p.productivity(p.Q0)
    alpha_e_hat = p.alpha_E * n0 / p.E_lim
    theta_hat = p.theta_L * n0 / l0
    xi_hat = p.xi_lim * l0 / n0
    xi_star_hat = p.xi_star * l0 / n0

    m = GEKKO(remote=False)
    m.time = mesh
    m.options.IMODE = 6
    m.options.NODES = 2
    m.options.SOLVER = 3
    m.options.MAX_ITER = min(p.ocp_max_iter, 200)
    m.options.OTOL = 1e-4
    m.options.RTOL = 1e-4

    u_w = m.MV(value=u_w0, lb=0.0, ub=1.0)
    u_d = m.MV(value=u_d0, lb=0.0, ub=1.0)
    u_w.STATUS = 1
    u_d.STATUS = 1
    u_w.DCOST = 1e-3
    u_d.DCOST = 1e-3

    y = m.Var(value=1.0, lb=1e-6)  # Y / Y0
    q = m.Var(value=p.Q0, lb=0.0, ub=p.Q_max)
    e0 = p.E0 / p.E_lim
    e = m.Var(value=e0, lb=0.0)  # no upper bound: we may already be past E_lim
    pr = m.Var(value=1.0, lb=1e-6, ub=p.P_lim / p.P0)  # P / P0
    el = m.Var(value=1.0, lb=1e-6)  # L / L0
    j = m.Var(value=0.0, lb=0.0)

    pi = p.pi0 / (1.0 + p.kappa_pi * q)
    s_rep = 1.0 + p.s_coeff * (pr - 1.0)
    n_hat = m.Intermediate((pi_q0 / pi) * y * s_rep)
    overshoot = 0.5 * ((pr - p.P_lim / p.P0) + m.sqrt((pr - p.P_lim / p.P0) ** 2 + p.smooth_eps))
    a_w = u_w * m.exp(-p.psi * overshoot)
    xi = n_hat / el
    sigma = p.sigma0 * (xi ** p.sigma_p) / (xi_star_hat ** p.sigma_p + xi ** p.sigma_p)
    raw = q / p.Q_ecc
    weight = raw - 0.5 * ((raw - 1.0) + m.sqrt((raw - 1.0) ** 2 + p.smooth_eps))
    phi = p.phi_conv + (p.phi_hw - p.phi_conv) * weight
    h_over_p0 = m.exp(p.h_exp * q)
    n_rho_hat = p.N_rho_over_N0
    n_delta_hat = p.N_delta_over_N0
    dens_gap = 0.5 * (
        (1.0 - n_hat / n_rho_hat)
        + m.sqrt((1.0 - n_hat / n_rho_hat) ** 2 + p.smooth_eps)
    )
    n_min_hat = n_hat - 0.5 * (
        (n_hat - n_delta_hat) + m.sqrt((n_hat - n_delta_hat) ** 2 + p.smooth_eps)
    )
    delicacy = (n_delta_hat / n_min_hat) ** p.nu_P

    m.Equation(
        y.dt() == (p.r * (1.0 - p.epsilon * (pr - 1.0)) * s_rep - p.lambda_D * u_d) * y
    )
    m.Equation(
        q.dt()
        == p.eta_W * a_w * (p.Q_max - q)
        + p.eta_rho * dens_gap * (p.Q_max - q)
        - sigma * q
    )
    m.Equation(e.dt() == alpha_e_hat * n_hat * (1.0 + p.kappa * q) - p.delta_E * e)
    m.Equation(
        pr.dt()
        == p.gamma * (h_over_p0 * m.exp(p.beta * (e - e0)) * delicacy - pr)
    )
    m.Equation(el.dt() == theta_hat * a_w * n_hat - p.delta_L * el)
    m.Equation(j.dt() == n_hat * (phi / p.phi_conv))

    m.Equation(xi_hat * el - n_hat >= 0)
    m.Equation(p.B - p.c_W * u_w - p.c_D * u_d >= 0)
    # Already past the ceiling: do not require e(t)<=1 at t0 (infeasible).
    # Do not worsen the overshoot; from the EAT-Lancet year onward E<=E_lim.
    m.Equation(e <= e0 + 0.05)
    restore = (p.t0 + mesh >= p.fsb_year).astype(float)
    m.Equation(e * m.Param(value=restore) <= restore)

    final = np.zeros(nt)
    final[-1] = 1.0
    m.Minimize(j * m.Param(value=final))
    m.solve(disp=False)

    uw = np.array([float(v) for v in u_w.value], dtype=float)
    ud = np.array([float(v) for v in u_d.value], dtype=float)
    return mesh, uw, ud


def _gekko_with_timeout(p: Params, u_w0: np.ndarray, u_d0: np.ndarray):
    with ProcessPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_gekko_solve, p, u_w0, u_d0)
        return future.result(timeout=GEKKO_TIMEOUT_SEC)


def _slsqp_solve(p: Params, u_w0: np.ndarray, u_d0: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, bool, str]:
    n = p.slsqp_pieces
    knots = np.linspace(0.0, p.horizon_years, n + 1)
    uw0 = np.interp(knots[:-1], np.linspace(0.0, p.horizon_years, len(u_w0)), u_w0)
    ud0 = np.interp(knots[:-1], np.linspace(0.0, p.horizon_years, len(u_d0)), u_d0)
    z0 = np.concatenate([uw0, ud0])

    def unpack(z):
        return z[:n], z[n:]

    def traj_from(z) -> Trajectory:
        uw, ud = unpack(z)
        coarse = np.linspace(0.0, p.horizon_years, max(49, int(p.horizon_years) + 1))
        return simulate(
            p,
            piecewise_control(knots, uw, ud),
            label="slsqp",
            t_eval=coarse,
        )

    def objective(z):
        return traj_from(z).J

    def ineq(z):
        tr = traj_from(z)
        e_noworse = float(p.E0 * 1.05 - np.max(tr.E))
        e_restore = _restore_slack(tr, p)
        return np.array(
            [
                e_noworse,
                e_restore,
                float(np.min(tr.slack_P)),
                float(np.min(tr.slack_labor)),
                float(np.min(tr.slack_budget)),
            ]
        )

    result = minimize(
        objective,
        z0,
        method="SLSQP",
        bounds=Bounds(0.0, 1.0),
        constraints=NonlinearConstraint(ineq, 0.0, np.inf),
        options={"maxiter": 40, "ftol": 1e-5, "disp": False},
    )
    uw, ud = unpack(result.x)
    return knots, uw, ud, bool(result.success), str(result.message)


def _restore_slack(traj: Trajectory, p: Params) -> float:
    """Tightest environmental slack from the food-system target year onward."""
    mask = np.asarray(traj.t) >= p.fsb_year
    if not np.any(mask):
        return float(traj.slack_E[-1])
    return float(np.min(traj.slack_E[mask]))


def _is_feasible(traj: Trajectory, p: Params) -> bool:
    """Price, labor, and budget must hold along the path.

    If environmental pressure already starts above the ceiling, require no
    further rise and E<=E_lim from the EAT-Lancet year onward — not at t0.
    """
    p_ok = float(traj.slack_P.min()) >= -1e-3
    labor_ok = float(traj.slack_labor.min()) >= -1e-3
    budget_ok = float(traj.slack_budget.min()) >= -1e-3
    starts_over = float(traj.slack_E[0]) < -1e-3
    if starts_over:
        e_ok = (float(np.max(traj.E)) <= float(traj.E[0]) * 1.05 + 1e-6) and (
            _restore_slack(traj, p) >= -1e-3
        )
    else:
        e_ok = float(np.min(traj.slack_E)) >= -1e-3
    return p_ok and labor_ok and budget_ok and e_ok


def optimize(p: Params, prefer: str = "gekko") -> OptResult:
    """Multi-start OCP. Re-simulates the best controls with the IVP for plots."""
    tried: list[str] = []
    best: OptResult | None = None
    nt = min(int(p.ocp_nodes), 121)
    mesh_default = np.linspace(0.0, p.horizon_years, nt)

    def consider(name: str, solver: str, mesh, uw, ud, message: str) -> None:
        nonlocal best
        tried.append(f"{name}/{solver}")
        control = (
            _interp_control(mesh, uw, ud)
            if len(uw) == len(mesh)
            else piecewise_control(mesh, uw, ud)
        )
        traj = simulate(p, control, label=f"Optimum ({solver})", color="#1f4e79", linestyle="-")
        feasible = _is_feasible(traj, p)
        note = (
            "feasible on the simulated path; states may sit below ceilings"
            if feasible
            else f"{message} (infeasible on the simulated path)"
        )
        cand = OptResult(traj, solver, feasible, note, traj.J, tried.copy())
        if best is None:
            best = cand
            return
        cand_ok, best_ok = _is_feasible(cand.trajectory, p), _is_feasible(best.trajectory, p)
        if cand_ok and not best_ok:
            best = cand
        elif cand_ok == best_ok and cand.J < best.J:
            best = cand

    if prefer == "gekko":
        for name, uw0, ud0 in _starts(nt)[:2]:
            try:
                mesh, uw, ud = _gekko_with_timeout(p, uw0, ud0)
                consider(name, "gekko", mesh, uw, ud, "GEKKO/IPOPT")
            except FuturesTimeout:
                tried.append(f"{name}/gekko-timeout")
            except Exception as exc:  # noqa: BLE001
                tried.append(f"{name}/gekko-fail:{type(exc).__name__}")

    if best is None or not _is_feasible(best.trajectory, p):
        for name, uw0, ud0 in _starts(nt):
            try:
                knots, uw, ud, ok, msg = _slsqp_solve(p, uw0, ud0)
                consider(name, "slsqp", knots, uw, ud, msg)
            except Exception as exc:  # noqa: BLE001
                tried.append(f"{name}/slsqp-fail:{type(exc).__name__}")

    if best is None:
        traj = simulate(
            p,
            piecewise_control(mesh_default, np.zeros(nt), np.ones(nt)),
            label="Fallback reduction-only",
        )
        return OptResult(traj, "fallback", False, "All starts failed", traj.J, tried)
    best.starts_tried = tried
    return best
