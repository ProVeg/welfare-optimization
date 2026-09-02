# `default.yaml` — parameter reference

Actual values used by `configs/default.yaml`, the central calibration for the aggregate small-bodied (poultry-like) model. Keys map 1:1 to YAML fields; override any of them with `--set key=value` (dotted for nested `horizon.*` keys, e.g. `horizon.T=2100`). Full literature sourcing behind each choice is in [`models/constrained-welfare-optimization.md` §7](../../../../models/constrained-welfare-optimization.md) and [`models/parameters/`](../../../../models/parameters/); this table is for scanning the actual number the code runs with, not for citing.

## Horizon and solver

| Key | Units | Value | Meaning |
|---|---|---|---|
| `horizon.t0` | calendar year | 2026 | Start year |
| `horizon.T` | calendar year | 2050 | Last year of the run (set to 2100 for a century path) |
| `horizon.n_points` | count | 241 | Output samples written to CSVs |
| `horizon.fsb_year` | calendar year | 2050 | From this year onward the optimizer must keep environmental pressure at or below `E_lim` |
| `ivp_method` | solver name | BDF | SciPy IVP method for open-loop trajectories |
| `ivp_rtol` | dimensionless | 1e-6 | Integrator relative tolerance |
| `ivp_atol` | dimensionless | 1e-8 | Integrator absolute tolerance |
| `ocp_nodes` | count | 41 | Collocation mesh size for GEKKO |
| `ocp_max_iter` | count | 200 | Optimizer iteration cap |
| `slsqp_pieces` | count | 10 | Piecewise-constant control intervals for the SLSQP fallback |
| `static_alpha_max_k` | 1 / unit \(u_W\) | 2.0 | How fast welfare-campaign effort can raise the high-welfare share in the 2050 snapshot NLP: \(\alpha \le 1-e^{-k u_W}\) |

## Demand and headcount

Standing animals \(N\) are a poultry-like stock (broilers), not slaughtered birds.

| Key | Units | Value | Meaning |
|---|---|---|---|
| `N0` | animals | 1.01e10 | Standing animals at \(t_0\) |
| `pi0` | kg edible / standing-animal-year | 12.1 | Edible output per standing animal-year at quality \(Q=0\) |
| `kappa_pi` | dimensionless | 0.288 | How much productivity falls as quality rises: \(\pi(Q) = \pi_0/(1+\kappa_\pi Q)\) |
| `r` | 1 / year | 0.011 | Business-as-usual demand growth |
| `epsilon` | dimensionless | 0.6 | Price elasticity of demand (higher price → fewer kilograms) |
| `s_coeff` | dimensionless | 0.2 | Species-replacement slope: a 20% price rise → 20% more small-bodied headcount. **Not a species-pair matrix** — v1 treats one aggregate small-bodied composite, so \(S(P)\) is a single scalar here, not the disaggregated \(S_s(P)\) of the model doc |

## Quality and suffering

| Key | Units | Value | Meaning |
|---|---|---|---|
| `Q0` | dimensionless (0–1) | 0.10 | Starting average quality of life (conventional-dominant) |
| `Q_max` | dimensionless (0–1) | 1.0 | Industrial-scale welfare ceiling |
| `Q_ecc` | dimensionless (0–1) | 0.50 | ECC-like mid reform (not a "good life") |
| `omega` | dimensionless (chicken-equivalent = 1) | 1.0 | Welfare-range weight; v1 is broiler-only so SADs are measured in chicken-equivalent units |
| `phi_conv` | SAD / animal-year | 1.0 | SAD intensity per conventional animal-year (index) |
| `phi_hw` | SAD / animal-year | 0.6 | SAD intensity per high-welfare animal-year (index; midpoint of the 0.4–0.8 sensitivity band) |
| `rho` | 1 / year | 0.0 | Discount rate on future SADs (0 = undiscounted) |

## Prices and willingness to pay

| Key | Units | Value | Meaning |
|---|---|---|---|
| `P0` | price index | 1.0 | Price index at \(t_0\) |
| `P_lim` | price index (ratio to \(P_0\)) | 1.15 | Mass-market willingness-to-pay ceiling (~10–15% above today) |
| `h_exp` | dimensionless | 0.347 | Cost-markup rate: \(h(Q) = P_0 \exp(h_{\mathrm{exp}} Q)\); ECC at \(Q_{\mathrm{ecc}}\) ≈ +19% |
| `h_ecc` | dimensionless (ratio) | 1.19 | ECC cost multiplier used in the static 2050 NLP |
| `psi` | dimensionless | 12.0 | How fast welfare standards collapse once price exceeds `P_lim` |
| `smooth_eps` | dimensionless | 1e-6 | Numerical smoothing epsilon for the "price above ceiling" switch |

## Biophysical pressure

\(E\) is livestock pressure as a share of the livestock allocation of the EAT-Lancet 2025 food-system boundary; \(E=1\) is that allocation, not "today's impact."

| Key | Units | Value | Meaning |
|---|---|---|---|
| `E0` | dimensionless (ratio to allocation) | 2.0 | Starting pressure / allocation (>1 = already past the cap) |
| `E_lim` | dimensionless (ratio) | 1.0 | Livestock share of the 2050 food-system ceiling |
| `kappa` | dimensionless | 0.144 | Extra land/feed footprint per unit of quality (~+14.4% per kg at ECC) |
| `alpha_E` | 1 / (animal-year) | 1.952e-10 | Pressure generated per standing animal-year |
| `delta_E` | 1 / year | 1.0 | How fast \(E\) tracks headcount (flow-like; land-conversion lag omitted in v1) |
| `beta` | dimensionless | 0.20 | Scarcity-markup exponent in the price ODE: \(\exp(\beta (E-E_0)/E_{\lim})\) |
| `gamma` | 1 / year | 0.50 | How fast retail price adjusts toward cost |
| `N_rho_over_N0` | dimensionless (ratio) | 0.85 | Density-relief threshold \(N_\rho/N_0\) |
| `eta_rho` | 1 / year | 0.08 | Density-relief speed (**calibration**, not a measured rate) |
| `N_delta_over_N0` | dimensionless (ratio) | 0.70 | Delicacy-premium threshold \(N_\delta/N_0\) |
| `nu_P` | dimensionless | 0.25 | Delicacy-premium quantity exponent |

## Labor / operational ceiling

| Key | Units | Value | Meaning |
|---|---|---|---|
| `L0` | FTE index | 1.0 | Farm labor at \(t_0\) |
| `xi_lim` | animals / FTE-index | 1.2625e10 | Maximum animals per FTE-index before operational failure (1.25 × \(N_0\)) |
| `xi_star` | animals / FTE-index | 1.515e10 | Midpoint of the failure Hill function (1.5 × \(N_0\), **calibration**) |
| `sigma0` | 1 / year | 0.35 | Maximum quality drain when staffing is overloaded (**calibration**) |
| `sigma_p` | dimensionless | 6 | Steepness of the overload switch (Hill exponent) |
| `delta_L` | 1 / year | 0.02 | Background decline of high-income agricultural labor |
| `theta_L` | FTE-index / (animal-year) | 2.0e-13 | Weak hiring response to headcount (**calibration**) |

## Campaign controls and budget

`u_W` and `u_D` share **one unit annual advocacy budget**: \(c_W u_W + c_D u_D \le B\), with \(B\equiv 1\) fixed by normalization (not swept). This is what makes the model actually weigh welfare-campaign effort against demand-reduction effort — spending more on one lever leaves strictly less budget for the other, so \((u_W,u_D)=(1,1)\) is **not feasible** under the default equal-cost weights.

| Key | Units | Value | Meaning |
|---|---|---|---|
| `lambda_D` | 1 / year | 0.04 | Extra demand decay at \(u_D=1\) (**calibration**, not measured) |
| `eta_W` | 1 / year | 0.25 | Speed of quality improvement at \(u_W=1\) (**calibration**, not measured) |
| `c_W` | budget units / unit \(u_W\) | 1.0 | Cost of welfare-campaign effort (equal-cost default) |
| `c_D` | budget units / unit \(u_D\) | 1.0 | Cost of demand-reduction effort (equal-cost default) |
| `B` | budget units / year | 1.0 | The one unit annual advocacy budget; fixed by normalization — do not sweep this, sweep `c_D`/`c_W` instead if a real relative cost is ever found |
