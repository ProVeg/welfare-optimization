# First-order parameters

These are the parameters §7.1 of [`constrained-welfare-optimization-v2.md`](../constrained-welfare-optimization-v2.md) flags as moving the answer. Full sourcing and caveats are in [§7.2](../constrained-welfare-optimization-v2.md#72-parameter-blocks); this table is for scanning, not citing.

| Parameter | Symbol | Units | Point estimate | Range | Confidence |
|---|---|---|---|---|---|
| BAU output growth | \(r(t)\) | 1 / year | ≈0.010–0.012/yr | 0.007–0.018 | medium (tonnage); lower for headcount |
| Broiler numbers | \(N_{\mathrm{br}}(t_0)\) | animals / year (slaughter); animals (standing) | slaughter 76.2B→87.3B (2023→2033); standing 10.1B→11.6B | ±15% sensitivity band | medium |
| Finfish numbers | \(N_{\mathrm{ff}}(t_0)\) | animals / year (slaughter); animals (standing) | slaughter 133.6B→155.1B; standing 222.6B→258.6B | 90% CI [86.0,181.2]B → [99.8,210.4]B | low–medium |
| Own-price elasticity | \(\varepsilon\) | dimensionless | 0.6 (poultry central) | 0.3–0.9 | medium |
| Cross-price / species map | \(S_s(P)\), \(\eta_{s,s'}\) | dimensionless matrix, one cross-price elasticity per species pair | **sign not universal**: US cut-level data say beef/pork demand is ~2× more sensitive to poultry price than the reverse; a Canada AIDS demand system says beef–poultry and beef–pork are *complements* | magnitude ≲0.6 either way | low (sign); medium (weakens near \(P^{\lim}\)) |
| High-welfare cost multiplier (broiler ECC) | \(h_{\mathrm{ECC}}\) | dimensionless (price ratio \(P/P_0\)) | +19% farm, +16% post-slaughter, +19% post-processing | +17%–21% at farm (EU) | high (EU ECC); low (Global South, beyond-ECC) |
| Biophysical markup (broiler ECC) | \(e^{\mathrm{hw}}/e^{\mathrm{conv}}\), \(\kappa\) | dimensionless — a **vector of ratios**, one per impact category (GHG, land, P), each a unitless conv-vs-hw ratio | GHG +11%, land +14.4%, P excretion +36.7% | indicator-specific — don't blend into one number | high (comparison); medium (as a global \(\kappa\)) |
| Biophysical/productivity markup (layers, cage-free) | \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) | dimensionless ratio | enriched cage→barn: GHG +56%, land +13%; organic: GHG ~+60%, land ~×2 | based on partly 2009–10 LCA inventory | medium |
| Planetary/food-system ceiling | \(E_k^{\lim}\) | dimensionless composite ratio \(E_0/E^{\lim}\); the underlying \(E_k\) is a **vector with a different physical unit per impact** \(k\): GtCO₂e/yr (climate), M km² (agricultural land), Tg N/yr (nitrogen), Tg P/yr (phosphorus) | composite \(E_0/E^{\lim}\approx 2.0\) (already overshot) | 1.1 (land-only) – 3.4 (climate-only) | high (overshoot is real); medium (exact composite) |
| WTP price ceiling | \(P^{\lim}/P_0\) | dimensionless | 1.10–1.15 (mass market) | 1.08–1.30 high-income; ~1.00–1.08 Global South (unknown) | medium (EU/US kink); low (global scalar) |
| SAD rates | \(\varphi_{\mathrm{conv}}, \varphi_{\mathrm{hw}}, \phi(Q)\) | SAD / animal-year (or SAD / animal-life, if consistently converted) | **unknown as an absolute number**; ratio \(\varphi_{\mathrm{hw}}/\varphi_{\mathrm{conv}}\) is the usable quantity | 0.4–0.8 (sensitivity band, not a measurement) | low (absolute); medium (ordinal: ECC helps but not to zero) |
| Productivity penalty | \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) | dimensionless ratio | broilers 0.75–0.95; layers 0.70–0.95 | wide, unresolved without FCR/days-to-slaughter conversion | medium (direction); low (exact ratio) |
| Demand-reduction effectiveness | \(\lambda_D\) | 1 / year | **unknown** — calibrate to bound: (i) ~4%/yr decline, (ii) Global South demand freeze, (iii) near-zero (skepticism case) | must be swept, not fixed | low |
