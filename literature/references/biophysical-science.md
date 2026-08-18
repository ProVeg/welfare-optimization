# Biophysical science — literature log

Append-only record of sources used when an agent chose or wrote a **climate, agriculture, welfare, ecology, or other empirical-science** claim or parameter. Newest entries go at the bottom.

Required fields per entry: Task, Source, ID (DOI and/or arXiv), Quote, Use. See `.cursor/rules/literature-references.mdc`.

## 2026-08-18 — density relief for Q only below a headcount threshold

- **Task:** decide whether quality of life should rise automatically as farmed headcount falls
- **Source:** Dawkins, Donnelly and Jones (2004). Chicken welfare is influenced more by housing conditions than by stocking density.
- **ID:** DOI `10.1038/nature02226`
- **Quote:** "Our results show that differences among producers in the environment that they provide for chickens have more impact on welfare than has stocking density itself." And: "although very high stocking densities do affect chicken welfare, stocking density per se is, within limits, less important than other factors in the birds' environment."
- **Use:** rejected a monotone Q(N) law; density relief is off at today's N and turns on only after a ~15% cut (very-high-density regime)

## 2026-08-18 — no single stocking-density cliff

- **Task:** choose a threshold form for density relief rather than a step at one kg/m²
- **Source:** Buijs, Keeling, Rettenbacher, Van Poucke and Tuyttens (2009). Stocking density effects on broiler welfare: Identifying sensitive ranges for different indicators.
- **ID:** DOI `10.3382/ps.2009-00007`
- **Quote:** "No threshold stocking density above which all aspects of welfare were suddenly altered was found in this study. Instead, different aspects of welfare were influenced at different densities or group sizes, or both."
- **Use:** used a smooth plus on (1 − N/N_ρ) rather than a single kg/m² cliff; N_ρ is a sensitivity parameter

## 2026-08-18 — space allowance vs welfare is not always monotone

- **Task:** check recent evidence that more space always raises welfare
- **Source:** Yang, Lesscher, Liu and Hostens (2026). From Manual Observation to Automated Monitoring: Space Allowance Effects on Play Behaviour in Group-Housed Dairy Calves.
- **ID:** arXiv `2602.00111`
- **Quote:** "The space-play relationship was non-linear, with highest play levels at 8-10 m² per calf (1.6% OP) and lowest at 6-8 m² and 12-14 m² (<0.6% OP)."
- **Use:** did not let Q run away with N → 0; kept the (Q_max − Q) cap and a threshold so extra space does not automatically mean a good life

## 2026-08-18 — commercial density band where health is compromised

- **Task:** set N_ρ near the commercial broiler density edge
- **Source:** Estevez (2007). Density Allowances for Broilers: Where to Set the Limits?
- **ID:** DOI `10.1093/ps/86.6.1265`
- **Quote:** "Published research consistently indicates that the health and welfare of broilers is compromised if space allowances drop below 0.0625 to 0.07 m2/bird (equivalent to about 34 to 38 kg/m2 depending on final BW)."
- **Use:** today's industry sits at that edge, so a modest global cut can move density into a less harmful band if housing is sticky; N_ρ/N0 = 0.85
