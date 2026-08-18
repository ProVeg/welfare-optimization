"""2050 snapshot NLP with inequality ceilings (scipy SLSQP)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import Bounds, NonlinearConstraint, minimize

from cwo.parameters import Params


@dataclass
class StaticResult:
    Y: float
    alpha: float
    u_W: float
    u_D: float
    N: float
    P_over_P0: float
    J: float
    slack: dict[str, float]
    success: bool
    message: str
    label: str


def _closed(alpha: float, u_w: float, u_d: float, p: Params):
    """Demand-determined 2050 snapshot. Ceilings are inequalities."""
    alpha = float(np.clip(alpha, 0.0, 1.0))
    u_w = float(np.clip(u_w, 0.0, 1.0))
    u_d = float(np.clip(u_d, 0.0, 1.0))
    price_ratio = (1.0 - alpha) + alpha * p.h_ecc
    y_bau = p.Y0 * np.exp(p.r * p.horizon_years)
    s_rep = 1.0 + p.s_coeff * (price_ratio - 1.0)
    demand_cut = 1.0 - np.exp(-p.lambda_D * u_d * p.horizon_years)
    y = y_bau * (1.0 - demand_cut) * (1.0 - p.epsilon * (price_ratio - 1.0)) * s_rep
    y = max(float(y), 1e-8)
    pi_conv = p.pi0
    pi_hw = p.pi0 / (1.0 + p.kappa_pi * p.Q_ecc)
    n = y * ((1.0 - alpha) / pi_conv + alpha / pi_hw)
    phi = (1.0 - alpha) * p.phi_conv + alpha * p.phi_hw
    j = p.omega * n * phi
    e_stock = p.E0 * (y / p.Y0) * (1.0 + p.kappa * alpha)
    labor_need = n * ((1.0 - alpha) + alpha * 1.3)
    inherited = 0.10
    alpha_max = inherited + (1.0 - inherited) * (1.0 - np.exp(-p.static_alpha_max_k * u_w))
    slacks = {
        "E": p.E_lim - e_stock,
        "P": p.P_lim / p.P0 - price_ratio,
        "labor": p.xi_lim * p.L0 - labor_need,
        "budget": p.B - (p.c_W * u_w + p.c_D * u_d),
        "alpha_cap": alpha_max - alpha,
    }
    return y, n, j, price_ratio, slacks


def evaluate_static(p: Params, alpha, u_w, u_d, label: str) -> StaticResult:
    y, n, j, price_ratio, slacks = _closed(alpha, u_w, u_d, p)
    return StaticResult(
        Y=float(y),
        alpha=float(alpha),
        u_W=float(u_w),
        u_D=float(u_d),
        N=float(n),
        P_over_P0=float(price_ratio),
        J=float(j),
        slack={k: float(v) for k, v in slacks.items()},
        success=all(v >= -1e-6 for v in slacks.values()),
        message="evaluated",
        label=label,
    )


def diagnostics(p: Params) -> list[StaticResult]:
    return [
        evaluate_static(p, 0.10, 0.0, 0.0, "BAU"),
        evaluate_static(p, 0.50, 1.0, 0.0, "Welfare-only"),
        evaluate_static(p, 0.10, 0.0, 1.0, "Reduction-only"),
        evaluate_static(p, 0.70, 0.7, 0.7, "Joint (diagnostic)"),
    ]


def solve_static(p: Params) -> StaticResult:
    x0 = np.array([0.1, 0.0, 1.0])

    def obj(x):
        return _closed(x[0], x[1], x[2], p)[2]

    def ineq(x):
        slacks = _closed(x[0], x[1], x[2], p)[4]
        return np.array(list(slacks.values()))

    result = minimize(
        obj,
        x0,
        method="SLSQP",
        bounds=Bounds([0.0, 0.0, 0.0], [1.0, 1.0, 1.0]),
        constraints=NonlinearConstraint(ineq, 0.0, np.inf),
        options={"maxiter": 200, "ftol": 1e-10, "disp": False},
    )
    alpha, u_w, u_d = result.x
    out = evaluate_static(p, alpha, u_w, u_d, "Static optimum")
    out.success = all(v >= -1e-6 for v in out.slack.values())
    out.message = str(result.message)
    return out
