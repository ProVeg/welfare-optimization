"""Smoothed ODE right-hand side and algebraic maps.

Stack mapping (literature/welfare-models-architecture.md): numpy evaluation of
the §4.2 system in models/constrained-welfare-optimization.md. Path ceilings
are *not* imposed here; slack is reported so open-loop runs may go below or
above a limit.
"""

from __future__ import annotations

import numpy as np

from cwo.parameters import Params

# State order: Y, Q, E, P, L
STATE_NAMES = ("Y", "Q", "E", "P", "L")


def smooth_plus(x, eps: float):
    """C^1 approximation of max(x, 0)."""
    return 0.5 * (x + np.sqrt(x * x + eps))


def density_relief(n, p: Params):
    """(1 - N/N_ρ)_+ : extra Q growth only after headcount falls past the density threshold."""
    return smooth_plus(1.0 - n / max(p.N_rho, 1e-30), p.smooth_eps)


def delicacy_markup(n, p: Params):
    """(N_δ / min(N, N_δ))^ν : 1 until N < N_δ, then a residual-luxury premium."""
    n_min = n - smooth_plus(n - p.N_delta, p.smooth_eps)
    return (p.N_delta / max(float(n_min), 1e-30)) ** p.nu_P


def productivity(quality, p: Params):
    return p.pi0 / (1.0 + p.kappa_pi * quality)


def species_replacement(price, p: Params):
    """S(P): more small-bodied animals when the meat basket gets dearer."""
    return 1.0 + p.s_coeff * (price - p.P0) / p.P0


def welfare_cost(quality, p: Params):
    """h(Q): convex-increasing production cost, h(0) = P0."""
    return p.P0 * np.exp(p.h_exp * quality)


def sad_rate(quality, p: Params):
    """phi(Q): linear interpolant, SAD / animal-year."""
    q_span = max(p.Q_ecc, 1e-12)
    weight = np.clip(quality / q_span, 0.0, 1.0)
    return p.phi_conv + (p.phi_hw - p.phi_conv) * weight


def operational_failure(ratio, p: Params):
    """Hill function σ(N/L)."""
    xi = np.maximum(ratio, 0.0)
    power = p.sigma_p
    num = xi**power
    den = p.xi_star**power + num
    return p.sigma0 * num / np.maximum(den, 1e-30)


def advocacy_effective(u_w, price, p: Params):
    overshoot = smooth_plus(price - p.P_lim, p.smooth_eps)
    return u_w * np.exp(-p.psi * overshoot)


def headcount(output_y, quality, price, p: Params):
    """Standing animals N = Y S(P) / π(Q)."""
    return output_y * species_replacement(price, p) / productivity(quality, p)


def sad_flow(output_y, quality, price, p: Params):
    """Instantaneous SAD / year."""
    n = headcount(output_y, quality, price, p)
    return p.omega * n * sad_rate(quality, p)


def slack(output_y, quality, pressure, price, labor, u_w, u_d, p: Params) -> dict[str, float]:
    """Positive slack means the inequality still has room (state < ceiling)."""
    n = headcount(output_y, quality, price, p)
    return {
        "E": float(p.E_lim - pressure),
        "P": float(p.P_lim - price),
        "labor": float(p.xi_lim - n / max(labor, 1e-30)),
        "budget": float(p.B - (p.c_W * u_w + p.c_D * u_d)),
        "u_W_box": float(1.0 - u_w),
        "u_D_box": float(1.0 - u_d),
    }


def rhs(time, state, u_w, u_d, p: Params) -> np.ndarray:
    """dx/dt for x = [Y, Q, E, P, L]. time is years from t0 (unused if r constant)."""
    del time
    output_y, quality, pressure, price, labor = state
    labor = max(float(labor), 1e-30)
    n = headcount(output_y, quality, price, p)
    a_w = advocacy_effective(u_w, price, p)
    sigma = operational_failure(n / labor, p)

    dY = (
        p.r * (1.0 - p.epsilon * (price - p.P0) / p.P0) * species_replacement(price, p)
        - p.lambda_D * u_d
    ) * output_y
    dQ = (
        p.eta_W * a_w * (p.Q_max - quality)
        + p.eta_rho * density_relief(n, p) * (p.Q_max - quality)
        - sigma * quality
    )
    dE = p.alpha_E * n * (1.0 + p.kappa * quality) - p.delta_E * pressure
    dP = p.gamma * (
        welfare_cost(quality, p)
        * np.exp(p.beta * (pressure - p.E0) / p.E_lim)
        * delicacy_markup(n, p)
        - price
    )
    dL = p.theta_L * a_w * n - p.delta_L * labor
    return np.array([dY, dQ, dE, dP, dL], dtype=float)


def initial_state(p: Params) -> np.ndarray:
    return np.array([p.Y0, p.Q0, p.E0, p.P0, p.L0], dtype=float)
