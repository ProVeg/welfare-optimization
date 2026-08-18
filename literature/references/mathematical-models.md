# Mathematical models — literature log

Append-only record of sources used when an agent chose or wrote a **formulation, theorem, or model architecture**. Newest entries go at the bottom.

Required fields per entry: Task, Source, ID (DOI and/or arXiv), Quote, Use. See `.cursor/rules/literature-references.mdc`.

## 2026-08-18 — residual-luxury markup instead of full inverse demand

- **Task:** add a meat-price term that rises when headcount is far below today, without treating u_D as a supply shock
- **Source:** Lusk and Tonsor (2016). How Meat Demand Elasticities Vary with Price, Income, and Product Category.
- **ID:** DOI `10.1093/aepp/ppv050`
- **Quote:** "Our findings reveal nonlinear demands for meat products, with demand being more inelastic at higher prices."
- **Use:** convex inverse demand at the remaining-luxury end; set ν = 0.25 ≪ 1/ε so a 50% herd cut is about +9%, not a 2^{1/ε} spike

## 2026-08-18 — livestock price tracks demand–supply imbalance

- **Task:** justify a quantity premium on P when N is scarce
- **Source:** Dieci, Mignot and Westerhoff (2018). Coupling the Yoccoz-Birkeland population model with price dynamics: chaotic livestock commodities market cycles.
- **ID:** arXiv `1803.05404`
- **Quote:** "the logarithmic derivative of the price is determined by the unbalance between the demand and supply of the meat."
- **Use:** P target includes a scarcity-of-quantity factor below N_δ, on top of cost-push h(Q) and environmental markup

Pointer (welfare/density): see `literature/references/biophysical-science.md` 2026-08-18 density-relief entries (Dawkins 2004; Buijs 2009; Estevez 2007; Yang et al. arXiv:2602.00111).
