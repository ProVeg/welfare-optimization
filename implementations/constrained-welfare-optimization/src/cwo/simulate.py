"""Open-loop integration of the welfare-limits ODE (scipy.integrate)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from cwo.dynamics import headcount, initial_state, rhs, sad_flow, slack
from cwo.parameters import Params

ControlFn = Callable[[float], tuple[float, float]]


@dataclass
class Trajectory:
    """Time series for one control path. Slack > 0 means below the ceiling."""

    label: str
    t: np.ndarray  # calendar years
    tau: np.ndarray  # years from t0
    Y: np.ndarray
    Q: np.ndarray
    E: np.ndarray
    P: np.ndarray
    L: np.ndarray
    N: np.ndarray
    u_W: np.ndarray
    u_D: np.ndarray
    sad_rate: np.ndarray
    J_cum: np.ndarray
    slack_E: np.ndarray
    slack_P: np.ndarray
    slack_labor: np.ndarray
    slack_budget: np.ndarray
    color: str = "#333333"
    linestyle: str = "-"

    @property
    def J(self) -> float:
        return float(self.J_cum[-1])

    def to_frame(self):
        import pandas as pd

        return pd.DataFrame(
            {
                "year": self.t,
                "Y_kg_per_year": self.Y,
                "Q": self.Q,
                "E": self.E,
                "P": self.P,
                "L": self.L,
                "N_standing": self.N,
                "u_W": self.u_W,
                "u_D": self.u_D,
                "sad_per_year": self.sad_rate,
                "J_cumulative_SAD": self.J_cum,
                "slack_E": self.slack_E,
                "slack_P": self.slack_P,
                "slack_labor": self.slack_labor,
                "slack_budget": self.slack_budget,
            }
        )


def constant_control(u_w: float, u_d: float) -> ControlFn:
    def _fn(_tau: float) -> tuple[float, float]:
        return u_w, u_d

    return _fn


def piecewise_control(knots: np.ndarray, u_w: np.ndarray, u_d: np.ndarray) -> ControlFn:
    """Right-continuous piecewise constant controls on [knots[0], knots[-1]]."""

    def _fn(tau: float) -> tuple[float, float]:
        idx = int(np.searchsorted(knots, tau, side="right") - 1)
        idx = min(max(idx, 0), len(u_w) - 1)
        return float(u_w[idx]), float(u_d[idx])

    return _fn


def simulate(
    p: Params,
    control: ControlFn,
    label: str = "run",
    color: str = "#333333",
    linestyle: str = "-",
    t_eval: np.ndarray | None = None,
) -> Trajectory:
    """Integrate with an implicit method. Constraints are monitored, not enforced."""
    tau_end = p.horizon_years
    if t_eval is None:
        t_eval = np.linspace(0.0, tau_end, p.n_points)

    def fun(tau, state):
        u_w, u_d = control(float(tau))
        u_w = float(np.clip(u_w, 0.0, 1.0))
        u_d = float(np.clip(u_d, 0.0, 1.0))
        return rhs(tau, state, u_w, u_d, p)

    sol = solve_ivp(
        fun,
        (0.0, tau_end),
        initial_state(p),
        method=p.ivp_method,
        t_eval=t_eval,
        rtol=p.ivp_rtol,
        atol=p.ivp_atol,
        dense_output=False,
    )
    if not sol.success:
        raise RuntimeError(f"IVP failed ({label}): {sol.message}")

    y, q, e, price, labor = sol.y
    n = headcount(y, q, price, p)
    u = np.array([control(float(tau)) for tau in sol.t], dtype=float)
    u_w, u_d = u[:, 0], u[:, 1]
    flow = sad_flow(y, q, price, p) * np.exp(-p.rho * sol.t)
    j_cum = np.concatenate([[0.0], np.cumsum(0.5 * (flow[1:] + flow[:-1]) * np.diff(sol.t))])

    slacks = [slack(y[i], q[i], e[i], price[i], labor[i], u_w[i], u_d[i], p) for i in range(len(sol.t))]
    return Trajectory(
        label=label,
        t=p.t0 + sol.t,
        tau=sol.t,
        Y=y,
        Q=q,
        E=e,
        P=price,
        L=labor,
        N=n,
        u_W=u_w,
        u_D=u_d,
        sad_rate=flow,
        J_cum=j_cum,
        slack_E=np.array([s["E"] for s in slacks]),
        slack_P=np.array([s["P"] for s in slacks]),
        slack_labor=np.array([s["labor"] for s in slacks]),
        slack_budget=np.array([s["budget"] for s in slacks]),
        color=color,
        linestyle=linestyle,
    )


def min_slacks(traj: Trajectory) -> dict[str, float]:
    return {
        "E": float(np.min(traj.slack_E)),
        "P": float(np.min(traj.slack_P)),
        "labor": float(np.min(traj.slack_labor)),
        "budget": float(np.min(traj.slack_budget)),
    }
