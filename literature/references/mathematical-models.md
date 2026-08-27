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

## 2026-08-20 — S(P) must be an asymmetric, sign-uncertain substitution map, not a monotone one

- **Task:** tighten the species-replacement map \(S_s(P)\) in §3.3/§4.2 of the v2 model, which previously just asserted "large-bodied price up ⇒ poultry/finfish demand up"
- **Source:** Lusk and Tonsor (2016). How Meat Demand Elasticities Vary with Price, Income, and Product Category.
- **ID:** DOI `10.1093/aepp/ppv050`
- **Quote:** "Ground beef, steak, and pork chop demands are more sensitive to changes in chicken breast price than the reverse... cross-price elasticities between disaggregate meat products shrink as prices rise." Table 3 (middle income): ground-beef cross-elasticity w.r.t. chicken-breast price = 0.603; chicken-breast cross-elasticity w.r.t. ground-beef price = 0.286.
- **Use:** built \(S(P)\) as an asymmetric matrix (large-bodied cuts ~2x more cross-sensitive to poultry price than the reverse) that weakens near \(P^{\lim}\), rather than a single symmetric substitution rate

## 2026-08-20 — beef and poultry can be net complements, not substitutes

- **Task:** check whether "meat price up ⇒ substitution toward small-bodied species" is a safe default sign for \(S(P)\)
- **Source:** Diakité, Z.R. Estimating Demand for Lamb, Beef, Pork, and Poultry in Canada.
- **ID:** arXiv `2402.13439`
- **Quote:** Table 8 (national AIDS demand system, Marshallian uncompensated elasticities): beef cross-price elasticity w.r.t. poultry price = -0.043; poultry cross-price elasticity w.r.t. beef price = -0.392; pork cross-price elasticity w.r.t. beef price = -0.214. "Beef and poultry are substitute good in QC and MS at the opposite of the other provinces where they are complementary goods."
- **Use:** rejected hard-coding \(S_s(P)\) as monotonically increasing for small-bodied species when a large-bodied price rises; the model now flags the sign as uncertain and to be swept
