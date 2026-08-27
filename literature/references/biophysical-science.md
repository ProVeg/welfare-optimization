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

## 2026-08-24 — labor/management explains more welfare variance than stocking density itself

- **Task:** compare the relative importance of the operational (labor, σ(N/L)) ceiling against the density-relief channel in `models/constrained-welfare-optimization-v2.md` for the welfare-specialist review of weak assumptions
- **Source:** Dawkins, Donnelly and Jones (2004). Chicken welfare is influenced more by housing conditions than by stocking density.
- **ID:** DOI `10.1038/nature02226`
- **Quote:** "Our results show that differences among producers in the environment that they provide for chickens have more impact on welfare than has stocking density itself." And: "although very high stocking densities do affect chicken welfare, stocking density per se is, within limits, less important than other factors in the birds' environment."
- **Use:** the same finding used for the density-relief threshold also implies management/labor quality is a larger driver of realized Q than raw N or N/L alone — flagged as a reason the model's σ(N/L) (ratio-only) may be under-specified relative to stockperson skill/attitude

## 2026-08-24 — stockperson skill and turnover as a welfare driver distinct from headcount ratio

- **Task:** source evidence on labor overload / stockmanship effects on farmed-animal welfare for the operational-ceiling parameter block
- **Source:** Daigle and Ridge (2018). Investing in stockpeople is an investment in animal welfare and agricultural sustainability.
- **ID:** DOI `10.1093/af/vfy015`
- **Quote:** "Turnover rates reached 50% over 6 months in Australian swine operations and 60% in U.S. laying hen facilities" and stockperson behavior "can elicit a fear response in livestock," with negative attitudes correlated with increased electric prod use and reduced milk yield (citing Coleman et al. 2003; Breuer et al. 2000).
- **Use:** evidence that welfare failure from labor scarcity operates through skill/attitude/turnover, not only the raw animals-per-worker ratio σ(N/L) models; flagged as a missing channel in the dynamic model

## 2026-08-24 — stockmanship ranks among top-tier welfare issues across species, alongside genetics and housing

- **Task:** compare labor/stockmanship's importance to other named welfare risk factors (genetics, housing, disease) for the same review
- **Source:** Rioja-Lang, Connor, Bacon, Lawrence and Dwyer (2020). Prioritization of Farm Animal Welfare Issues Using Expert Consensus.
- **ID:** DOI `10.3389/fvets.2019.00495`
- **Quote:** "Inability of stockpeople to recognize and/or treat welfare issues (such as pain or behavioral problems)" appears among the common top-ranked issues across species; for pigs "inadequate stockperson skills" ranked #3 for severity/duration.
- **Use:** supports treating labor/stockmanship as a first-order welfare ceiling (consistent with the model's choice to make it a hard constraint), not a second-order refinement
- **Confidence:** Not a fully stratified quantitative ranking; the paper does not give a single ordinal list across all factors, so treat "top-tier" as qualitative.

## 2026-08-24 — quantitative link between workers-per-headcount and catching injury

- **Task:** find a quantitative dose-response between a labor ratio and a welfare outcome, to check the σ(N/L) functional form
- **Source:** Mönch, Rauch, Hartmannsgruber, Erhard, Wolff, Schmidt, Schug and Louton (2020). The welfare impacts of mechanical and manual broiler catching and of circumstances at loading under field conditions.
- **ID:** DOI `10.1016/j.psj.2020.08.030`
- **Quote:** "The involvement of more working people per 10,000 broilers during manual loading was associated with a lower occurrence of hematomas."
- **Use:** confirms a real, measured animals-per-worker → injury channel, but at the catching/loading stage specifically (person-hours per 10,000 birds loaded), not the daily-care stage the model's ξ (animals per FTE-index) is calibrated against — flagged as a stage-mixing weak assumption
