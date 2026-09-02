# `sensitivity.yaml` — tornado sweep ranges

One-at-a-time low/high pairs swept around `configs/default.yaml` by `python -m cwo sensitivity`. Metric: cumulative SADs of the **constant joint** diagnostic (\(u_W=u_D=0.5\), an even split of the one unit annual advocacy budget), not a re-optimized policy.

| Parameter | Key | Units | Low | High | Default (for reference) |
|---|---|---|---|---|---|
| Demand-reduction rate | `lambda_D` | 1 / year | 0.0 | 0.06 | 0.04 |
| Price ceiling (WTP) | `P_lim` | price index | 1.08 | 1.30 | 1.15 |
| High-welfare SAD rate | `phi_hw` | SAD / animal-year | 0.4 | 0.8 | 0.6 |
| Welfare footprint penalty | `kappa` | dimensionless | 0.11 | 0.367 | 0.144 |
| BAU demand growth | `r` | 1 / year | 0.007 | 0.018 | 0.011 |
| Density-relief threshold | `N_rho_over_N0` | dimensionless (ratio) | 0.70 | 1.00 | 0.85 |
| Density-relief speed | `eta_rho` | 1 / year | 0.0 | 0.16 | 0.08 |
| Delicacy-price threshold | `N_delta_over_N0` | dimensionless (ratio) | 0.50 | 1.00 | 0.70 |
| Delicacy-price exponent | `nu_P` | dimensionless | 0.0 | 0.50 | 0.25 |

`s_coeff` (the species-replacement slope) is **not** in this sweep, despite being a first-order, low-confidence assumption per the model doc — it is held fixed at its default (0.2) in every tornado run.
