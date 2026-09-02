# Second-order parameters

These are the parameters §7.1 of [`constrained-welfare-optimization-v2.md`](../constrained-welfare-optimization-v2.md) flags as shaping secondary behavior (timing, magnitude of side effects) rather than the headline conclusion. Full sourcing and caveats are in [§7.2](../constrained-welfare-optimization-v2.md#72-parameter-blocks); this table is for scanning, not citing.

| Parameter | Symbol | Units | Point estimate | Range | Confidence |
|---|---|---|---|---|---|
| Species welfare-range weights | \(\omega_s\) | dimensionless (human = 1) — a **vector**, one weight per species \(s\) | pigs 0.515, chickens 0.332, octopus 0.213, carp 0.089, salmon 0.056, shrimp 0.031, black soldier flies 0.013 | chickens 0.002–0.869 (5th–95th) | low (absolute); needed once species are disaggregated |
| Welfare-campaign effectiveness | \(\eta_W\) | 1 / year | **unknown as a rate**; calibrate so \(u_W\equiv1, u_D=0\) reaches ECC-like \(Q\) in 5–10 yr before ceilings bind | cage-free fulfillment 85–90%; ECC fulfillment much worse (ChickenTrack) | low (rate); high (effectiveness collapses near \(P^{\lim}\)) |
| Density-relief threshold | \(N_\rho,\ \eta_\rho\) | animals (\(N_\rho\)); 1 / year (\(\eta_\rho\)) | \(N_\rho = 0.85 N_0\); \(\eta_\rho = 0.08\)/yr (calibration, not measured) | \(N_\rho/N_0 \in [0.7, 1.0]\) | high (very high density harms welfare); low (\(\eta_\rho\)) |
| Delicacy / residual-luxury exponent | \(N_\delta,\ \nu\) | animals (\(N_\delta\)); dimensionless (\(\nu\)) | \(N_\delta = 0.70 N_0\); \(\nu = 0.25\) (a 50% headcount cut marks up price ~9%) | \(\nu \in [0, 0.5]\) | high (supply shocks raise price); low (\(\nu\)) |
| Operational labor ceiling | \(\xi^{\lim} = (N/L)^{\lim}\) | animals / FTE | **unknown numeric value**; qualitative EU evidence of inspection failure (footpad dermatitis 38%, hock burns 20%, breast blisters 6.5%) | treat as a sensitivity parameter, identified so BAU already sits near failure | high (constraint is real); low (numeric value) |
| Advocacy budget | \(c_W,\ c_D\); \(B\equiv1\) | dimensionless (\(B\), fixed by normalization); dimensionless budget-share per unit control (\(c_W, c_D\)) | \(B=1\) always; \(c_W=c_D=1\) (equal-cost default) | \(c_D/c_W\) unknown — sweep this, not \(B\) | n/a for \(B\) (definitional); low for \(c_W,c_D\) |
| Discount rate | \(\rho\) | 1 / year | 0 (default) | 0–0.04 | n/a (value judgment) |
