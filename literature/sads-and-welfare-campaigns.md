# SADs per species, and welfare-campaign effectiveness

Welfare-specialist research note. Answers three questions for the model's \(\varphi_{\mathrm{conv}}, \varphi_{\mathrm{hw}}\) (SAD rates), \(\omega_s\) (welfare-range weights), \(\eta_W\) (welfare-campaign effectiveness), \(\lambda_D\) (demand-reduction effectiveness), and \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}, \kappa_\pi\) (productivity penalty) parameter blocks in `models/constrained-welfare-optimization-v2.md` §7.2:

1. Who are the most respected EA-aligned sources for SADs (Suffering-Adjusted Days) per species?
2. What do those sources say about how much traditional welfare campaigns, and newer welfare-tech propositions, actually move SADs?
3. How do welfare improvements (e.g. slower-growing breeds, cage-free housing, crate-free sow housing) affect productivity in kg edible output per animal-year, i.e. the \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) ratio the model uses to convert output \(Y\) into headcount \(N\)?

Read alongside [literature/limits-to-welfare.md](limits-to-welfare.md) (existing corporate-campaign cost-effectiveness citations) and [models/parameters/first-order-parameters.md](../models/parameters/first-order-parameters.md) / [second-order-parameters.md](../models/parameters/second-order-parameters.md) (where these feed the model). Every empirical claim below is also logged in [literature/references/biophysical-science.md](references/biophysical-science.md) per the project's citation rule.

---

## 1. The most respected EA sources for SADs

There is no single authoritative SADs table. Four organizations, in a division of labor, together produce the inputs the metric needs:

| Organization | Role | What they own |
|---|---|---|
| **Charity Entrepreneurship / Ambitious Impact (AIM)** | Defined the metric | The SADs formula itself and its "SADs 2.0" revision |
| **Welfare Footprint Institute** (Cynthia Schuck-Paim & Wladimir Alonso) | Measures the pain | The empirical "time in pain" data (Cumulative Pain Framework) that SADs' *welfare footprint* term is built from |
| **Rethink Priorities** | Weighs the species | The *welfare range* estimates (Moral Weight Project) that convert one species' pain into human-equivalent units |
| **Animal Charity Evaluators (ACE)** | Applies it to charities | SADs-averted-per-dollar cost-effectiveness reviews of specific programs |

### SADs methodology (definition)

- **Symbol:** SADs, \(\varphi\), \(\phi(Q)\)
- **Definition:** "SADs are adjusted to 'disabling' levels of pain on the Welfare Footprint pain scale. So 1 day spent in disabling pain for 1 human would be equal to 1 SAD." Composed as \(\mathrm{SADs} = S \times WR \times WF \times MW\): sentience probability (\(S\)) × welfare range (\(WR\)) × welfare footprint / time-in-pain on a 0–4 scale where 0 = no pain, 1 = annoying, 2 = hurtful, 3 = disabling, 4 = excruciating (\(WF\)) × moral weight converting each pain category to disabling-pain-equivalent (\(MW\)). A secondary mortality-based estimate, \(\mathrm{SADs}_2 = S \times WR \times \Delta MR \times PD_0\), is also used.
- **Units:** SAD / animal (dimensionless days, human-disabling-pain-day = 1)
- **Point estimate:** No universal per-species-per-year number exists; SADs are computed per intervention, from the underlying Welfare Footprint time-in-pain tables (§2 below).
- **Uncertainty / range:** Charity Entrepreneurship describes the model as "work-in-progress" and "still ironing out some bugs and errors." "SADs 2.0" (Ambitious Impact, 2025) moved away from a single composite score built on "point estimates of scaling ratios" between pain intensities, toward disaggregated results by pain intensity (annoying/hurtful/disabling/excruciating reported separately) specifically because of "high degree of uncertainty over our pain scaling ratios."
- **Time development:** Actively revised; treat any single-number SADs figure as provisional.
- **Scope:** General method, applied per species/system by whoever computes it (AIM, ACE, independent EA Forum analysts).
- **Source:** Charity Entrepreneurship, *SADs (Suffering-Adjusted Days): An improved animal welfare measurement tool* (blog); Ambitious Impact, *Growth Research, a Methods Site, and SADs 2.0* (EA Forum, 2025), https://forum.effectivealtruism.org/posts/oqo7oPEqBoufHHzeN/growth-research-a-methods-site-and-sads-2-0-aim-research.
- **Confidence:** Low on absolute numbers (by the method's own admission); the ordinal logic (more time in worse pain ⇒ more SADs) is more robust than any point estimate.

---

## 2. SAD / time-in-pain estimates per species and system

All from the Welfare Footprint Institute's Cumulative Pain Framework, which is the empirical backbone most EA cost-effectiveness models (ACE, AIM, Rethink Priorities) draw their pain-intensity inputs from.

### Broilers: conventional vs Better Chicken Commitment (BCC) / slower-growing breeds

- **Symbol:** \(\varphi_{\mathrm{conv}}, \varphi_{\mathrm{hw}}\) (broiler)
- **Definition:** Hours of pain, by intensity, over a broiler's life, comparing a fast-growing conventional bird (~61 g/day growth, 42-day slaughter) to a BCC-compliant slower-growing bird (~45–46 g/day growth, 56-day slaughter).
- **Units:** hours / bird-life, by pain intensity (annoying / hurtful / disabling / excruciating)
- **Point estimate:** BCC adoption prevents "at least 33 [13 to 53] hours of Disabling pain" (≈66% reduction), "79 [-99 to 260] hours of Hurtful" pain (≈24–25% reduction), and "25 [5 to 45] seconds of Excruciating pain" (≈78–80% reduction) per bird. Separately, Our World in Data's summary of the same Welfare Footprint book gives 80% less excruciating pain, 67% less disabling pain, 25% less hurtful pain for slower-growing vs fast-growing breeds.
- **Uncertainty / range:** Wide, asymmetric intervals given above (e.g. hurtful-pain interval crosses zero); the book's authors call these figures conservative, "excluding additional welfare challenges with higher prevalence in fast-growing birds."
- **Time development:** Level shift at breed/system conversion, not a rate.
- **Scope:** Broiler grow-out only. A related, separate finding: fast-growing-strain **breeder** hens (kept alive far longer, feed-restricted) experience "at least 2,000 hours of Disabling pain and 4,170 hours in Hurtful pain as a result of hunger" — a distinct and larger welfare cost the model's broiler-only \(\varphi\) does not currently capture.
- **Source:** Schuck-Paim & Alonso, *Quantifying Pain in Broiler Chickens: Impact of the Better Chicken Commitment and Adoption of Slower-Growing Breeds on Broiler Welfare* (Welfare Footprint Institute book); welfarefootprint.org/broilers/; Our World in Data, *Adopting slower-growing breeds of chicken would reduce animal suffering significantly* (2025), https://ourworldindata.org/adopting-slower-growing-breeds-of-chicken-would-reduce-animal-suffering-significantly.
- **Confidence:** Medium-high for the ordinal claim (slower growth reduces pain across all four intensities); low-medium on the exact hour counts (wide, sometimes zero-crossing intervals).

### Laying hens: conventional cage vs furnished cage vs cage-free aviary

- **Symbol:** \(\varphi_{\mathrm{conv}}, \varphi_{\mathrm{hw}}\) (layer)
- **Definition:** Hours of pain, by intensity, over a hen's laying cycle, comparing conventional cages (CC), furnished/enriched cages (FC), and cage-free aviaries.
- **Units:** hours / hen laying-cycle, by pain intensity
- **Point estimate:** Aviaries vs conventional cages: "at least 275 hours of disabling pain, 2,313 hours of hurtful pain and 4,645 hours of annoying pain" prevented per hen. Aviaries vs furnished cages (a smaller gap): "1,410 hours of hurtful pain and 4,065 hours of annoying pain" prevented per hen.
- **Uncertainty / range:** Presented as minimum estimates; authors note several factors suggest actual benefits may exceed these. A separate, system-independent finding: "approximately 2,000 hours of excruciating pain are expected for every flock of 50,000 laying hens (1–3 hours per individual affected)," mostly during depopulation/transport — this occurs in **all** systems, so it does not discriminate \(\varphi_{\mathrm{conv}}\) from \(\varphi_{\mathrm{hw}}\).
- **Time development:** Level shift at system conversion. Keel-bone fractures are flagged as "the most important welfare concern in cage-free aviaries" — a cost of the reform itself, not just a residual conventional-system harm.
- **Scope:** Laying hens; production-system comparison only (not genetics/breed).
- **Source:** Welfare Footprint Institute, welfarefootprint.org/laying-hens/; cross-referenced by Our World in Data, *Do better cages or cage-free environments really improve the lives of hens?*, https://ourworldindata.org/do-better-cages-or-cage-free-environments-really-improve-the-lives-of-hens.
- **Confidence:** Medium — same caveats as broilers (Welfare Footprint's own partly-2009–2010 LCA inventory issue noted in `models/parameters/first-order-parameters.md` is about environmental data, not this pain data, but both come from thin, non-updated evidence bases).

### Farmed fish: slaughter-stage pain (rainbow trout)

- **Symbol:** \(\varphi_{\mathrm{conv}}, \varphi_{\mathrm{hw}}\) (finfish, slaughter stage only)
- **Definition:** Minutes of intense pain during air-asphyxia slaughter (the conventional method for most farmed finfish) vs electrical stunning.
- **Units:** minutes / fish, at slaughter
- **Point estimate:** Air asphyxia causes "an average of 10 minutes of intense pain" (range 2–22 minutes depending on fish size and water temperature). Electrical stunning "can prevent 60–1,200 minutes of pain per US dollar invested."
- **Uncertainty / range:** Rethink Priorities' independent review of 19 papers / 76 experiments found electrical stunning "plausibly offer[s] counterfactual welfare improvements for rainbow trout, but the case is much weaker for seabream and seabass" — do not generalize the trout result to all finfish. Commercial conditions (space, power, maintenance) likely underperform the lab studies cited.
- **Time development:** One-off, at the moment of slaughter; does not capture on-farm/rearing-stage pain (separate Welfare Footprint salmon work covers water quality, stocking density, fasting).
- **Scope:** Slaughter-stage only; species-specific (strong evidence: rainbow trout; weak: seabream, seabass).
- **Source:** Welfare Footprint Institute / *Scientific Reports*, *Quantifying the welfare impact of air asphyxia in rainbow trout slaughter for policy and practice* (2025), https://www.nature.com/articles/s41598-025-04272-1; Rethink Priorities, *Review: Electrical Stunning Does Not Yet Ensure Prolonged Insensibility In Several European Finfish Species*, https://rethinkpriorities.org/research-area/review-electrical-stunning-european-finfish/.
- **Confidence:** Medium for trout; low for seabream/seabass; low for external validity of lab conditions to commercial farms.

### Species welfare-range weights (\(\omega_s\))

Restated here with the exact percentile table (already summarized in `models/parameters/second-order-parameters.md`), sourced directly from Rethink Priorities' page rather than secondary citation:

| Species | 5th pct | 50th pct (point estimate) | 95th pct |
|---|---|---|---|
| Pigs | 0.005 | 0.515 | 1.031 |
| Chickens | 0.002 | 0.332 | 0.869 |
| Octopuses | 0.004 | 0.213 | 1.471 |
| Carp | 0 | 0.089 | 0.568 |
| Bees | 0 | 0.071 | 0.461 |
| Salmon | 0 | 0.056 | 0.513 |
| Crayfish | 0 | 0.038 | 0.491 |
| Shrimp | 0 | 0.031 | 1.149 |
| Crabs | 0 | 0.023 | 0.414 |
| Black soldier flies | 0 | 0.013 | 0.196 |
| Silkworms | 0 | 0.002 | 0.073 |

- **Source:** Rethink Priorities, *Welfare Range Estimates*, https://rethinkpriorities.org/research-area/welfare-range-estimates/.
- **Confidence:** Low in absolute terms (conditioned on hedonism + sentience assumptions the page itself flags); the *relative ordering* is the more defensible part of the estimate.

---

## 3. Traditional welfare-campaign effectiveness (SADs, or years-of-life, per dollar)

| Intervention | Effectiveness estimate | Source | Confidence |
|---|---|---|---|
| Corporate cage-free + broiler campaigns, combined, 2005–2018 | 9–120 chicken-years affected per \$ (90% CI); broiler-only ≈0.2–90 years/\$, driven by 1.7–720 broilers affected/\$ × 43–48 day lifespan | Šimčikas (2019), Rethink Priorities, https://rethinkpriorities.org/publications/corporate-campaigns-affect-9-to-120-years-of-chicken-life-per-dollar-spent | Low–medium: explicitly "cost-effectiveness of **past** campaigns," not a forecast of the next marginal dollar; follow-through rates ranged 48–84% (cage-free) and 1–94% (broiler) |
| Same campaigns, current marginal dollar | ≈1/5 of Šimčikas' 2019 estimate | Oehlsen (2024), comment on EA Forum | Low (single practitioner estimate, not a full model) |
| Corporate campaigns vs GiveWell top charities | Broiler campaigns ≈1,710× as cost-effective as the least-cost GiveWell top charity (per Rethink Priorities' Cross-Cause Cost-Effectiveness Model); a separate estimate: broiler welfare ≈68.9% and cage-free ≈12.4% "as cost-effective as GiveWell's top charities" once target-beneficiary and "soil animal" accounting is applied | Rethink Priorities, *Cross-Cause Cost-Effectiveness Model*; Open Philanthropy (secondary citation via search) | Low: these two figures use different denominators/assumptions and are not directly comparable to each other — sweep, don't average |
| Retailer plant-based commitments vs welfare programmes | Within an order of magnitude of most welfare programmes on animal-years-affected/\$, at the lower end; "at least seven times higher if wild-caught fishes were included" | Šimčikas (2025), EA Forum, https://forum.effectivealtruism.org/posts/sLYSa7MyuDKxreN5h/cost-effectiveness-of-anima-international-poland-1 | Low: author himself flags all estimates as "highly speculative" |
| Institutional demand reduction (School Plates) | 19.4% of cage-free corporate-campaign cost-effectiveness | Grilo (2025), EA Forum | Low |
| Consumer demand reduction (Veganuary) | 1.20% of cage-free corporate-campaign cost-effectiveness | Grilo (2025), EA Forum | Low |

(Šimčikas 2019/2025, Oehlsen 2024, and Grilo 2025 are already logged in `literature/limits-to-welfare.md`'s reference list; restated here for direct comparison to the tech-based interventions below.)

---

## 4. Innovative welfare-tech propositions

Split by how directly EA orgs have evaluated them (first three rows have EA-native cost-effectiveness numbers; the rest are general animal-science literature not yet run through an EA cost-effectiveness model — useful for the model's \(\eta_W\) sensitivity band, not as point estimates).

### Evaluated by EA orgs (SADs or an analogous unit, per dollar)

| Technology | What it does | Effectiveness | Source | Confidence |
|---|---|---|---|---|
| **Shrimp electrical stunning** (Shrimp Welfare Project Humane Slaughter Initiative) | Stuns shrimp in 1–2 seconds before slaughter instead of ice-slurry asphyxiation; stunner costs \$55k, producers commit to ≥120M shrimp/year | ACE: 48 SADs averted per \$ (range 43–53). An independent EA Forum cost-effectiveness post, using a different DALY-analogous metric, found air asphyxiation stunning ≈21× more cost-effective than ice-slurry stunning specifically, at 671 vs 31.9 "DALY/\$" — **not the same unit as ACE's SADs/\$, do not merge the two figures** | ACE, *Shrimp Welfare Project Review*, https://animalcharityevaluators.org/charity-review/shrimp-welfare-project/; EA Forum, https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane | Low: ACE itself cautions the estimate "should be interpreted with caution because of the difficulty in estimating the suffering averted... and the uncertainty around the correct implementation of the technologies" |
| **Shrimp pond water-quality/sludge management** (Sustainable Shrimp Farmers of India program) | Removes sludge, manages water quality in shrimp ponds | ACE: 729 SADs averted per \$ — **more cost-effective than the stunning program above**, by ACE's own estimate | ACE, *Shrimp Welfare Project Review* (same page) | Low, same caveat |
| **Fish farm dissolved-oxygen correction** (Fish Welfare Initiative) | On-farm water testing (dissolved oxygen, temperature, pH) with aerator interventions when out of range; ~90% successful implementation across ~1,300 instances | Ambitious Impact: 14.75 "welfare points" gained per fish-year improved (a different, non-SAD unit) | Ambitious Impact estimate, cited via EA Forum, https://forum.effectivealtruism.org/posts/yoDTsrR95YRnBW6fk/cost-effectiveness-of-the-fish-welfare-interventions | Low: FWI itself has "expressed significant doubts that their India model... has sufficient long-term cost-effectiveness and scalability" and is pivoting toward more scalable interventions |
| **Finfish electrical stunning** | Replaces air-asphyxia slaughter | 60–1,200 minutes of pain averted per \$ of capital expenditure for rainbow trout; weak/no evidence yet for seabream, seabass | Rethink Priorities, farmed-fish corporate-commitments cause area page, https://rethinkpriorities.org/research-area/farmed-fish-corporate-commitments/ | Low–medium, species-specific (see §2 above) |
| **In-ovo sexing** | Determines chick sex before hatching, ending live male-chick culling (grinding/gassing) | Scale: ~7.83 billion male chicks culled/year globally (2024); in-ovo sexing "commercially proven, adds under one cent per egg," already ~40% of EU production; bans in force in Germany, France, Austria (Italy from 2027) | EA Forum, *Nearly 8 billion male chicks culled per year*, https://forum.effectivealtruism.org/posts/r36kWhhLLJzj6ChwA/nearly-8-billion-male-chicks-culled-per-year-a-transparent | Medium on scale/adoption numbers; **~70% of culling — and nearly all the growth — is in Asia, where adoption is "close to zero"**; no SADs-per-\$ figure located for this specific tech, treat as unquantified pending a dedicated CEA |

### Not yet run through an EA cost-effectiveness model (general animal-science literature — useful for sensitivity bands, not point estimates)

- **Controlled atmosphere stunning (CAS) vs electrical waterbath stunning (broilers).** CAS eliminates live shackling and handling before stunning (a source of stress/injury under electrical waterbath methods) but requires slow, controlled gas induction — "rapid gas introduction causes pain, convulsions, and breathlessness." Net welfare comparison is contested in the literature; Temple Grandin's review concludes overall bird welfare likely improves with gas stunning "even if there is some discomfort before the bird loses consciousness." *Source:* Grandin, *Animal Welfare Evaluation of Gas Stunning of Chickens and other Poultry*, https://www.grandin.com/gas.stunning.poultry.eval.html. *Confidence:* medium on direction, no quantified hours-of-pain comparison found equivalent to the Welfare Footprint broiler tables above.
- **Eyestalk-ablation-free shrimp broodstock.** Eyestalk ablation (removing/cauterizing a gland to trigger spawning) is being phased out: Global Seafood Alliance requires all BAP-certified producers to end the practice by 2030; several UK grocers (Tesco, Iceland, Morrisons, Co-op) already restrict it in their supply chains. Alternative (ablation-free) broodstock production has been piloted without the feared production collapse, though researchers warn it could raise hatchery costs. *Source:* Shrimp Welfare Project, *Eyestalk Ablation-Free*, https://www.shrimpwelfareproject.org/eyestalk-ablation-free; Global Seafood Alliance, https://www.globalseafood.org/blog/gsa-to-end-eyestalk-ablation-by-2030/. *Confidence:* medium on adoption trajectory, no SAD quantification located.
- **Infrared beak treatment vs hot-blade trimming (layer chicks).** Infrared cauterization of one-day-old chicks' beak tips is "considered more welfare-friendly" than conventional hot-blade trimming: fewer behavioral changes, better feather condition, less aggression, comparable egg production and body weight. *Source:* Poultry Science, https://academic.oup.com/ps/article/88/1/38/2962773 (and related follow-up studies). *Confidence:* medium (peer-reviewed, replicated), but not yet expressed as a pain-hours or SADs figure.
- **Precision livestock farming (PLF): sensor-based early disease/lameness detection.** Wearable and camera/audio sensors monitoring activity, gait, vocalization, and vital signs can flag welfare problems (lameness, respiratory disease) earlier than manual inspection, which is "time-consuming, subjective and at risk of delayed detection." *Source:* Frontiers in Animal Science, *Exploring the Potential of Precision Livestock Farming Technologies to Help Address Farm Animal Welfare*, https://www.frontiersin.org/journals/animal-science/articles/10.3389/fanim.2021.639678/full. *Confidence:* low-medium — the same review notes "precision livestock farming technologies with sufficient accuracy and ready for implementation on commercial farms are rare," i.e. mostly pre-commercial.
- **Ammonia-mitigating litter additives (broilers).** A zeolite–clay–rice-husk-ash bedding supplement cut in-house ammonia by ~50% and reduced footpad-lesion severity and serum cortisol (~30% reduction) versus standard litter. This is a direct, low-cost lever on the same footpad-dermatitis/hock-burn harms cited in `models/constrained-welfare-optimization-v2.md` §7.2 (De Jong et al. 2011/2012, via *Limits to Welfare*). *Source:* ScienceDirect / PMC, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12865563/. *Confidence:* medium (single commercial-scale trial), general animal science, not EA-vetted.
- **Gestation-crate-free group housing (sows).** Group housing removes the worst confinement harms of gestation crates (documented pressure sores, ulcers, depression-like behavior) but "pigs are more likely to be injured due to aggressive behavior from the other pregnant pigs" in group housing — a real, if smaller, residual welfare cost. *Source:* multiple secondary sources (Humane League, Farm Forward); primary quantification of hours-in-pain not located — flagged as a gap, not a confirmed number.

---

## 5. Productivity impact of welfare improvements (kg edible output / animal-year)

The model converts output \(Y\) into headcount \(N\) via \(N = Y/\pi(Q)\), \(\pi(Q) = \pi_0/(1+\kappa_\pi Q)\), so the productivity penalty \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) directly controls how much a welfare reform *inflates* headcount at fixed output — the mechanism behind "welfare-only" strategies increasing SADs rather than reducing them. This section checks that calibration against direct throughput/output data, not just the land-use proxy the model currently uses for \(\kappa_\pi\) (see note at the end).

### Broilers: slower-growing breeds, throughput basis

- **Symbol:** \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) (broiler)
- **Definition:** Edible/live output per bird-day of grow-out (final slaughter weight ÷ days to slaughter), conventional fast-growing breed vs named slower-growing breeds used in higher-welfare (ECC-compliant) schemes.
- **Units:** kg live weight / bird-day (a direct proxy for kg / animal-year, since the model's \(\pi_0\) is likewise an animal-year rate)
- **Point estimate:** Conventional Ross 308: 2.93 kg at 47 days = 0.0623 kg/bird-day. Three ECC-compliant slower-growing breeds: Ranger Classic 2.52 kg at 57 days = 0.0442 kg/bird-day (ratio to conventional **0.71**); Ranger Gold 2.27 kg at 57 days = 0.0398 kg/bird-day (ratio **0.64**); Rowan Ranger 2.43 kg at 59 days = 0.0412 kg/bird-day (ratio **0.66**). (Ratios are this note's own calculation from the paper's reported weights/days, not a quoted figure.) A separate industry dataset (Wageningen 2025) reports ECC broilers grow at "around 55 grams per bird per day," described as "medium-slow growing," reaching "37 days to reach the thinning stage, and 51 days to reach cull weight" — consistent in direction but not decomposed into a single kg/day figure comparable to the RSOS numbers above without the corresponding conventional-breed rate, which was not located in this pass.
- **Uncertainty / range:** **0.64–0.71** across three named commercial slower-growing breeds (throughput basis) — this sits at or below the *low end* of the model's current \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}} \in [0.75, 0.95]\) broiler sensitivity band. A separate feed-conversion-only comparison (Hubbard JA757 vs Ross 308/Cobb 500) found the faster-growing breeds "grew faster, ate less feed and had better FCR and ADG," direction-consistent but not decomposed into a single ratio; another study found a slower-growing hybrid's FCR at 2.9±0.1 kg feed/kg gain vs 2.6±0.1 for a fast-growing hybrid (FCR ≈12% worse, a distinct metric from output/day).
- **Time development:** Level shift at breed conversion; not a rate. Genetics could narrow this gap over time (flagged as "unknown" in the existing model doc's Productivity penalty block) but no trend data located.
- **Scope:** UK/EU commercial broiler breeds (Ross 308 as conventional baseline; Ranger Classic/Gold, Rowan Ranger as ECC-compliant alternatives). US-focused study (land-use framing), but breed genetics and growth curves are multinational commercial lines, not US-specific.
- **Source:** *The 'sustainability gap' of US broiler chicken production: trade-offs between welfare, land use and consumption*, Royal Society Open Science 9(6):210478 (2022), https://royalsocietypublishing.org/rsos/article/9/6/210478/96705/; Wageningen Social & Economic Research report 2025-138 (already cited for cost/environmental figures); feed-conversion comparison via Hubbard/Ross/Cobb studies (secondary, exact citation not confirmed in this pass).
- **Confidence:** Medium-high on the RSOS throughput ratios (peer-reviewed, named breeds, exact weights and days given); medium on generalizing beyond these three specific breeds to "slower-growing breeds" as a class.
- **Consequence for land use (same source):** to hold current US consumption constant with these slower breeds would need "44.6%–86.8% larger population" of birds, and housing them on pasture "would require 108,642–121,019 km², a 43.8–60.1% increase over current land use" — an independent confirmation, via a different pathway, of the same headcount-inflation mechanism the model's \(N=Y/\pi(Q)\) formalizes.

### Laying hens: productivity is contested and management-dependent, not a clean penalty

- **Symbol:** \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) (layer)
- **Definition:** Eggs per hen-day and mortality rate, conventional cage vs enriched/furnished cage vs cage-free (free-range/aviary).
- **Point estimate:** No single ratio. A 16-country meta-analysis found "hen day egg production was higher in free-range systems but similar in conventional cage and enriched cage systems" — i.e. on this metric cage-free is not worse, and may be better. The same literature also reports the opposite in less mature operations: "hens showed higher mortality (up to 25% at 90 weeks), increased feed intake (up to 11.8% higher than the genetic guide), and greater body weight (up to +142g)" in some alternative-system studies.
- **Uncertainty / range:** Time- and management-dependent. The meta-analysis found "each year of experience with cage-free aviaries was associated with a 0.35–0.65% average drop in cumulative mortality, with no differences in mortality between caged and cage-free systems in more recent years" — i.e. the productivity gap this model's default \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}} \in [0.70, 0.95]\) band assumes may be shrinking as an artifact of producer inexperience with newer systems, not a fixed biological penalty. Where mortality is elevated, "a primary cause was injurious pecking behavior," a management/genetics factor (brown hens bred for high egg production), not an inherent feature of cage-free housing.
- **Time development:** Narrowing over calendar time as cage-free operational experience accumulates (the 0.35–0.65%/year mortality-drop figure above is itself a time trend, not a level).
- **Scope:** Commercial laying hens, 16-country meta-analysis (mortality) plus separate single-country production studies (egg output); breed-dependent (brown vs white hens differ in pecking-related mortality).
- **Source:** *Laying hen mortality in different indoor housing systems: a meta-analysis of data from commercial farms in 16 countries*, Scientific Reports (2021), https://www.nature.com/articles/s41598-021-81868-3; *Egg production and welfare of laying hens kept in different housing systems*, Poultry Science, https://academic.oup.com/ps/article/95/7/1564/2563727.
- **Confidence:** Low-medium on any fixed point estimate — this is the clearest case in this research pass where "welfare improvement ⇒ lower productivity" does **not** hold as a simple law; recommend the model's layer productivity penalty be treated as more second-order/uncertain than the broiler one, or even bidirectional (\(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) could exceed 1 for mature, well-managed free-range operations).

### Pigs: crate-free / group housing — productivity effect is small and sometimes favorable

- **Symbol:** \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\) (pig, not currently in the model's species set but relevant to the extensions list, §8 of the model doc)
- **Definition:** Piglets born/weaned per litter and sow mortality, gestation crate vs group housing.
- **Point estimate:** A cross-country ecological comparison found "sow mortality is significantly higher, and annual pig production per sow significantly lower" in countries where gestation crates remain the norm, versus EU countries with restrictions — the **opposite direction** from the assumed welfare-productivity trade-off. A more controlled US comparison found group housing (hoop barns) produced "0.8 more pigs born per litter" and "0.4 more pigs weaned per litter" than gestation crates. A separate comparison between two group-housing variants found "16.8 piglets" born (large pens, deep litter straw) vs "15.4 piglets" (smaller group pens) — showing housing-system detail matters even within "crate-free."
- **Uncertainty / range:** The cross-country figure is ecological (confounded by country-level differences in genetics, veterinary access, and farm scale beyond crate policy alone) and the exact numeric values were only available in a chart the fetch could not read (F1000Research, https://f1000research.com/articles/11-564/v1) — reported here as a directional finding, not a precise ratio. At least one other study found "no differences in sow productive performance or reproductive performance between group housing systems and individual stalls," so do not treat the productivity-*gain* direction as universal either.
- **Time development:** Not established; EU-wide gestation-crate restrictions are already in force (since 2013 for most of gestation), so this is a legal baseline in the EU, not an emerging reform.
- **Scope:** Sows, gestation phase only (not farrowing crates, which remain a distinct, separately-debated welfare issue with their own productivity claims).
- **Source:** Welfare Footprint Institute summary, https://welfarefootprint.org/2022/05/26/sows/, of an F1000Research cross-country analysis; Pork Information Gateway, *Sow and Litter Performance for Individual Crate and Group Hoop Barn Gestation Housing Systems*; PMC, *A comparison of two systems for group housing of gestating sows*, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11706077/.
- **Confidence:** Low-medium: direction (crate-free is not clearly less productive, and may be more) is consistent across three independent comparisons, but no single, precise, non-confounded ratio was located.

### Modeling note: the throughput data disagrees with the model's land-use-proxy calibration of \(\kappa_\pi\)

`configs/default.yaml` keeps two separate symbols — `kappa_pi` (productivity, in \(\pi(Q)=\pi_0/(1+\kappa_\pi Q)\)) and `kappa` (biophysical pressure, in \(\dot E\)) — but calibrates **both from the same underlying number**: Wageningen's +14.4% ECC **land-use** markup. `kappa` uses it directly (correctly, since it *is* a land-use parameter); `kappa_pi` uses it as a stand-in, per the config comment: "ECC land +14.4% as a productivity proxy at Q=Q_ecc: 1 + kappa_pi Q_ecc = 1.144 → kappa_pi ≈ 0.288." That proxy is not what this note finds when productivity is measured directly. Using this note's broiler throughput ratios (0.64–0.71 at \(Q_{\mathrm{ecc}}=0.5\)) instead and solving \(\pi(Q_{\mathrm{ecc}})/\pi(0) = 1/(1+\kappa_\pi \cdot 0.5)\) for \(\kappa_\pi\) gives **≈0.82–1.13** — three to four times larger than the land-use-proxy value of 0.288. In words: land use rises ~14% at ECC-level welfare, but *direct output per bird-day* falls much further (29–36%), because slower growth costs more animal-days per kilogram than it costs square meters per kilogram. Recommend `kappa_pi` be recalibrated from the throughput ratios in this section rather than the land-use figure, which appears to systematically understate the productivity penalty (and therefore understate how much a welfare-only strategy inflates headcount \(N=Y/\pi(Q)\)). Flagged for `applied-mathematician`/`model-engineer`, not changed here (a calibration decision, but one with model-behavior consequences worth a deliberate call rather than a silent edit).

---

## 6. Handoff note: first-order vs second-order for the current model

**First-order** (would change which strategy the optimizer favors):

- The broiler and layer conventional-vs-reform pain-hour ratios in §2 (feeds \(\varphi_{\mathrm{hw}}/\varphi_{\mathrm{conv}} \in [0.4, 0.8]\), consistent with the existing sensitivity band in `models/constrained-welfare-optimization-v2.md` §7.2 — nothing above contradicts that band, but the BCC figures (66–80% reduction across disabling/excruciating pain) sit at the *aggressive* end of it, while the "hurtful pain" interval (24–25% reduction, crossing zero at its low end) sits well inside it. Recommend keeping the band as-is rather than narrowing it around the point estimate).
- **The broiler productivity penalty in §5 is first-order and probably mis-calibrated toward being too mild.** The model's current \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}} \in [0.75, 0.95]\) sensitivity band and its `kappa_pi` default (0.288, derived from a land-use proxy) both sit above the 0.64–0.71 throughput ratio this note found for three named commercial slower-growing breeds. Since \(N=Y/\pi(Q)\), understating the productivity penalty means the model understates how much a welfare-only strategy inflates headcount (and therefore SADs) at fixed output — exactly the mechanism `limits-to-welfare.md` argues is the whole point. Recommend widening the broiler band toward \([0.60, 0.95]\) or recalibrating `kappa_pi` from the throughput ratios (§5's modeling note) before trusting a "welfare-only" vs "joint" ranking from this model.
- The layer productivity penalty, by contrast, should probably be **demoted toward second-order or removed as a fixed penalty**: §5 found no clean evidence that cage-free housing reduces egg output or raises mortality once a producer has operational experience — the direction of the effect is contested and time-dependent, not a stable ratio like the broiler case.

**Second-order** (shapes which lever looks more promising, not the headline ranking): the campaign/tech cost-effectiveness numbers in §3–4. These cannot currently be swept into \(\eta_W\) or \(\lambda_D\) directly — they use incompatible units across sources (SADs/\$, DALY/\$, "welfare points"/fish-year, minutes-of-pain/\$) and mix past-campaign realized cost-effectiveness with prospective/marginal estimates. The clearest actionable finding for \(\eta_W\)'s calibration story: ACE's own numbers rank a *water-quality* intervention (729 SADs/\$) above a *stunning* intervention (48 SADs/\$) for the same charity, which cautions against assuming "welfare tech" is inherently more or less cost-effective than "traditional" campaigns — it is intervention-specific, not category-specific.

**Not usable as parameters at all, only as context:** the retailer plant-based / Veganuary / School Plates comparisons in §3, which bear on \(\lambda_D\)'s plausibility range but every source cited explicitly disclaims precision ("highly speculative," "not statistically significant" below an order of magnitude per Bruers 2025 in `literature/limits-to-welfare.md`).

**Still needed, not found in this pass:** a SADs-per-dollar or pain-hours-per-dollar figure for in-ovo sexing specifically (found scale and adoption data, no cost-effectiveness model); any EA-vetted cost-effectiveness figure for CAS-vs-waterbath stunning, infrared beak treatment, or gestation-crate-free housing (all three have welfare-direction evidence but no SADs quantification located); a precise, non-confounded piglets-per-sow-per-year ratio for crate vs group housing (the clearest cross-country figure is only available in a chart this pass could not read); and a conventional-breed throughput rate from the same Wageningen dataset that gave the ECC 55 g/day figure, which would let the RSOS-breed-based κ_π recalibration in §5 be cross-checked against a second, independent source.
