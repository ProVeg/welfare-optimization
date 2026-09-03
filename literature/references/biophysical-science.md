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

## 2026-09-03 — SADs formula and its 2.0 revision

- **Task:** research the most respected EA sources for SADs per species and how the metric is defined, for `literature/sads-and-welfare-campaigns.md`
- **Source:** Charity Entrepreneurship. SADs (Suffering-Adjusted Days): An improved animal welfare measurement tool.
- **ID:** none found (organizational blog post); URL `https://www.charityentrepreneurship.com/post/sads-suffering-adjusted-days-an-improved-animal-welfare-measurement-tool`
- **Quote:** "SADs are adjusted to 'disabling' levels of pain on the Welfare Footprint pain scale. So 1 day spent in disabling pain for 1 human would be equal to 1 SAD."
- **Use:** basis for the SADs formula (SADs = Sentience × Welfare range × Welfare footprint × Moral weight) written up in §1 of the new literature note, and for flagging that the metric has no universal per-species-per-year point estimate

## 2026-09-03 — SADs 2.0 moved from a composite score to disaggregated pain-intensity results

- **Task:** same as above — characterize the current state/uncertainty of the SADs methodology
- **Source:** Ambitious Impact. Growth Research, a Methods Site, and SADs 2.0 (AIM Research Update).
- **ID:** none found; URL `https://forum.effectivealtruism.org/posts/oqo7oPEqBoufHHzeN/growth-research-a-methods-site-and-sads-2-0-aim-research`
- **Quote:** the original approach "convert[ed] all pain estimates into Disabling Pain Equivalents using point estimates of scaling ratios," now kept only "as a legacy approach... for information only," because of a "high degree of uncertainty over our pain scaling ratios."
- **Use:** justified treating any single composite SADs figure as provisional, and reporting disaggregated pain-intensity results where available in the new literature note

## 2026-09-03 — broiler pain-hours averted by the Better Chicken Commitment / slower-growing breeds

- **Task:** find quantified SAD/time-in-pain estimates for broilers under conventional vs high-welfare systems, for the model's φ_hw/φ_conv sensitivity band
- **Source:** Schuck-Paim and Alonso (2022). Quantifying Pain in Broiler Chickens: Impact of the Better Chicken Commitment and Adoption of Slower-Growing Breeds on Broiler Welfare (Welfare Footprint Institute).
- **ID:** none found (book/institute publication); URL `https://welfarefootprint.org/broilers/`
- **Quote:** BCC adoption prevents "at least 33 [13 to 53] hours of Disabling pain" and "79 [-99 to 260] hours of Hurtful" pain per bird; fast-growing-strain breeder hens experience "at least 2,000 hours of Disabling pain and 4,170 hours in Hurtful pain as a result of hunger."
- **Use:** confirmed the existing φ_hw/φ_conv ∈ [0.4, 0.8] sensitivity band is compatible with (if somewhat more conservative than) the BCC disabling/excruciating-pain reduction figures, and flagged breeder-hen suffering as a welfare cost the broiler-only φ does not currently capture

## 2026-09-03 — slower-growing breeds: pain reduction by intensity, cross-checked

- **Task:** cross-check the Welfare Footprint broiler figures against a secondary summary
- **Source:** Our World in Data (2025). Adopting slower-growing breeds of chicken would reduce animal suffering significantly.
- **ID:** none found; URL `https://ourworldindata.org/adopting-slower-growing-breeds-of-chicken-would-reduce-animal-suffering-significantly`
- **Quote:** "Excruciating pain is reduced by 80%, disabling pain by 67%, and hurtful pain by 25%" when switching to slower-growing breeds.
- **Use:** independent confirmation (percentage terms) of the Welfare Footprint hour-based figures above, used side by side in the literature note's broiler parameter block

## 2026-09-03 — laying hen pain-hours averted by cage-free aviaries

- **Task:** find quantified SAD/time-in-pain estimates for laying hens under conventional cage, furnished cage, and cage-free systems
- **Source:** Welfare Footprint Institute. Transition to cage-free systems (Laying Hens research page).
- **ID:** none found; URL `https://welfarefootprint.org/laying-hens/`
- **Quote:** aviaries avert "at least 275 hours of disabling pain, 2,313 hours of hurtful pain and 4,645 hours of annoying pain" per hen vs conventional cages, and "1,410 hours of hurtful pain and 4,065 hours of annoying pain" vs furnished cages; "approximately 2,000 hours of excruciating pain are expected for every flock of 50,000 laying hens (1-3 hours per individual affected)," mostly during depopulation/transport.
- **Use:** basis for the layer parameter block in the new literature note; the depopulation/transport pain figure was flagged as system-independent (does not discriminate φ_conv from φ_hw)

## 2026-09-03 — rainbow trout air-asphyxia slaughter pain and electrical-stunning cost-effectiveness

- **Task:** find quantified pain and cost-effectiveness data for farmed-fish slaughter methods, an under-covered species group in the model's current aggregate-composite treatment
- **Source:** Welfare Footprint Institute / Scientific Reports. Quantifying the welfare impact of air asphyxia in rainbow trout slaughter for policy and practice (2025).
- **ID:** URL `https://www.nature.com/articles/s41598-025-04272-1`
- **Quote:** air asphyxia causes "an average of 10 minutes of intense pain" (range 2-22 minutes); "electrical stunning can prevent 60-1,200 minutes of pain per US dollar invested."
- **Use:** first quantified finfish-specific pain/cost-effectiveness figure logged for this project; used to caution against treating the model's single aggregate small-bodied composite as representative of finfish specifically

## 2026-09-03 — electrical stunning evidence is species-specific, not general to all finfish

- **Task:** check whether the rainbow trout stunning result generalizes to other farmed finfish
- **Source:** Rethink Priorities. Review: Electrical Stunning Does Not Yet Ensure Prolonged Insensibility In Several European Finfish Species.
- **ID:** none found; URL `https://rethinkpriorities.org/research-area/review-electrical-stunning-european-finfish/`
- **Quote:** electrical stunners "plausibly offer counterfactual welfare improvements for rainbow trout, but the case is much weaker for seabream and seabass," based on a review of "19 papers with 76 experiments."
- **Use:** explicit caution added to the literature note against generalizing a species-specific welfare-tech result to "finfish" as a class

## 2026-09-03 — species welfare-range point estimates (full percentile table)

- **Task:** restate ω_s with a direct-source percentile table rather than a secondary citation
- **Source:** Rethink Priorities. Welfare Range Estimates.
- **ID:** none found; URL `https://rethinkpriorities.org/research-area/welfare-range-estimates/`
- **Quote:** "these estimates are, essentially, estimates of the differences in the possible intensities of these animals' pleasures and pains relative to humans' pleasures and pains," conditioned on hedonism and sentience assumptions.
- **Use:** reproduced the 5th/50th/95th percentile welfare-range table for all 11 species directly from the source page in the new literature note

## 2026-09-03 — corporate campaign cost-effectiveness, exact percentile breakdown

- **Task:** get the exact broiler-only vs combined cost-effectiveness range behind the "9 to 120 years of chicken life per dollar" headline already cited in `literature/limits-to-welfare.md`
- **Source:** Šimčikas (2019). Corporate campaigns affect 9 to 120 years of chicken life per dollar spent (Rethink Priorities).
- **ID:** none found; URL `https://rethinkpriorities.org/publications/corporate-campaigns-affect-9-to-120-years-of-chicken-life-per-dollar-spent`
- **Quote:** "for every dollar spent, 9 to 120 years of chicken life will be affected" (90% CI, 2005-2018, cage-free and broiler combined); broiler-only ≈0.2-90 years/\$, from 1.7-720 broilers affected/\$ × 43-48 day lifespan; explicitly "this is cost-effectiveness of past campaigns... not an estimate of what an additional donated dollar would achieve."
- **Use:** first formal reference-log entry for this figure (previously cited only in `literature/limits-to-welfare.md` prose); used in the new note's campaign-effectiveness comparison table, with the past-vs-marginal caveat carried forward

## 2026-09-03 — corporate campaigns vs GiveWell top charities, cross-cause comparison

- **Task:** find an EA cross-cause cost-effectiveness comparison for corporate welfare campaigns
- **Source:** Rethink Priorities. Cross-Cause Cost-Effectiveness Model: Introduction and Overview.
- **ID:** none found; URL `https://forum.effectivealtruism.org/posts/pniDWyjc9vY5sjGre/rethink-priorities-cross-cause-cost-effectiveness-model`
- **Quote:** "corporate campaigns for broiler welfare were estimated to be 1.71 thousand times as cost-effective as the lowest cost to save a life among GiveWell's top charities."
- **Use:** logged alongside a second, differently-scoped Open Philanthropy estimate (68.9%/12.4% "as cost-effective as GiveWell's top charities") with an explicit warning in the note not to average the two, since they use different denominators

## 2026-09-03 — shrimp humane-slaughter and pond water-quality cost-effectiveness, in SADs/\$

- **Task:** find EA-vetted SADs-per-dollar figures for a "welfare tech" (electrical stunning) vs a more traditional husbandry intervention (water quality), to compare tech vs traditional campaign cost-effectiveness
- **Source:** Animal Charity Evaluators. Shrimp Welfare Project Review (2025 Recommended Charity).
- **ID:** none found; URL `https://animalcharityevaluators.org/charity-review/shrimp-welfare-project/`
- **Quote:** "48 Suffering-Adjusted Days (SADs) averted per dollar for the Humane Slaughter Initiative program, and 729 SADs averted per dollar for the Sustainable Shrimp Farmers of India program," with the caveat that these estimates "have limited explanatory power... because of the difficulty in estimating the suffering averted."
- **Use:** central evidence for the note's conclusion that welfare-tech is not inherently more cost-effective than traditional husbandry interventions — here a water-quality program outperforms a stunning-device program by ACE's own numbers, by the same charity

## 2026-09-03 — independent shrimp-stunning cost-effectiveness estimate, a different unit than ACE's SADs

- **Task:** cross-check the ACE shrimp figure against an independent analysis
- **Source:** EA Forum. Cost-effectiveness of Shrimp Welfare Project's Humane Slaughter Initiative.
- **ID:** none found; URL `https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane`
- **Quote:** air asphyxiation stunning estimated at "671 DALY/\$" vs ice slurry at "31.9 DALY/\$," air asphyxiation being "21.0 times" more cost-effective; each stunner "costs us \$55k" and producers commit to "stunning a minimum of 120 million shrimps per annum."
- **Use:** flagged explicitly in the note as a different, DALY-based unit that must not be merged with ACE's SADs/\$ figure for the same charity, since a same-looking number from two sources can silently mean two different things

## 2026-09-03 — fish farm dissolved-oxygen intervention cost-effectiveness

- **Task:** find a cost-effectiveness figure for the Fish Welfare Initiative's core water-quality intervention
- **Source:** Ambitious Impact estimate, cited in: Cost-effectiveness of the fish welfare interventions recommended by Ambitious Impact, and Fish Welfare Initiative's farm program (EA Forum).
- **ID:** none found; URL `https://forum.effectivealtruism.org/posts/yoDTsrR95YRnBW6fk/cost-effectiveness-of-the-fish-welfare-interventions`
- **Quote:** "14.75 welfare points gained per fish-year improved" for water-quality/dissolved-oxygen corrections; "nearly 1,300 instances of improved water quality, with successful implementation in 90% of cases."
- **Use:** logged as a third, again non-comparable ("welfare points," not SADs) unit; used to illustrate the units problem flagged in the note's handoff section

## 2026-09-03 — scale and adoption of in-ovo sexing against male chick culling

- **Task:** find scale and adoption data for in-ovo sexing as a welfare-tech intervention against a specific, large-scale, well-defined harm (male chick culling)
- **Source:** EA Forum. Nearly 8 billion male chicks culled per year: a transparent, tractable welfare problem.
- **ID:** none found; URL `https://forum.effectivealtruism.org/posts/r36kWhhLLJzj6ChwA/nearly-8-billion-male-chicks-culled-per-year-a-transparent`
- **Quote:** global male chick culling estimated at "7.83 billion in 2024"; in-ovo sexing is "commercially proven, adds under one cent per egg, and already covers about 40% of E.U. production"; "roughly 70% of culling — and nearly all the growth — is in Asia, where in-ovo sexing adoption is close to zero."
- **Use:** logged as a scale/adoption data point for the model's extensions list (§8, shrimp/insects/other taxa) and as an example of a welfare-tech intervention with no SADs-per-dollar figure yet available — flagged as a research gap rather than filled with a guess

## 2026-09-03 — controlled atmosphere stunning welfare trade-offs (broilers)

- **Task:** assess a named alternative slaughter technology (CAS) against the electrical waterbath method already discussed in `literature/limits-to-welfare.md` §5
- **Source:** Grandin (2019, updated). Animal Welfare Evaluation of Gas Stunning (Controlled Atmosphere Stunning) of Chickens and other Poultry.
- **ID:** none found; URL `https://www.grandin.com/gas.stunning.poultry.eval.html`
- **Quote:** "rapid gas introduction causes pain, convulsions, and breathlessness"; overall bird welfare would likely be "improved with gas stunning even if there is some discomfort before the bird loses consciousness," because it removes live shackling.
- **Use:** logged as a qualitative (direction-only, not hours-quantified) welfare-tech comparison, explicitly distinguished in the note from the quantified Welfare Footprint figures elsewhere in the same table

## 2026-09-03 — eyestalk-ablation-free shrimp broodstock, industry phase-out timeline

- **Task:** document an emerging welfare-tech/practice-change with a concrete industry commitment date
- **Source:** Global Seafood Alliance. GSA to End Eyestalk Ablation by 2030.
- **ID:** none found; URL `https://www.globalseafood.org/blog/gsa-to-end-eyestalk-ablation-by-2030/`
- **Quote:** GSA "will require all Best Aquaculture Practices (BAP)-certified shrimp producers worldwide to discontinue the practice of eyestalk ablation by the end of 2030."
- **Use:** logged as an industry-driven (not EA-driven) welfare-tech timeline, cross-referenced with the Shrimp Welfare Project's own eyestalk-ablation-free page; no SAD quantification available

## 2026-09-03 — infrared beak treatment as a lower-pain alternative to hot-blade trimming

- **Task:** document a chick-hatchery-stage welfare-tech alternative
- **Source:** Poultry Science. Infrared beak treatment method compared with conventional hot-blade trimming in laying hens.
- **ID:** DOI via `https://academic.oup.com/ps/article/88/1/38/2962773`
- **Quote:** infrared treatment shows "fewer behavioral changes, improve[d] feather cover, reduce[d] aggression, and limit[ed] tissue damage that could cause acute and/or chronic pain," with "no difference in egg production or bird body weight" vs hot-blade trimming.
- **Use:** logged as a peer-reviewed, replicated welfare-tech finding with a clear welfare-direction result but no SADs/pain-hours quantification located

## 2026-09-03 — precision livestock farming: early-detection welfare technology, mostly pre-commercial

- **Task:** assess sensor/AI-based welfare monitoring as a candidate "innovative welfare tech" category
- **Source:** Frontiers in Animal Science. Exploring the Potential of Precision Livestock Farming Technologies to Help Address Farm Animal Welfare (2021).
- **ID:** DOI via `https://www.frontiersin.org/journals/animal-science/articles/10.3389/fanim.2021.639678/full`
- **Quote:** direct observation is "time-consuming, subjective and at risk of delayed detection"; despite this, "precision livestock farming technologies with sufficient accuracy and ready for implementation on commercial farms are rare."
- **Use:** logged as a category with plausible but currently unquantified and largely pre-commercial welfare benefit — explicitly not given a point estimate in the note

## 2026-09-03 — ammonia-mitigating litter additive reduces footpad dermatitis

- **Task:** find a direct, low-cost technological lever on the footpad-dermatitis/hock-burn harms already cited from De Jong et al. via `literature/limits-to-welfare.md`
- **Source:** (journal article, via PMC). Ammonia mitigation and welfare enhancement in broilers using zeolite-clay-rice husk ash bedding supplement.
- **ID:** none found; URL `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12865563/`
- **Quote:** the 40% zeolite-clay-rice-husk-ash bedding treatment showed "reduced serum cortisol concentrations (approximately 30% reduction), and decreased footpad lesion severity," and "maintained lower in-house NH₃ concentrations, reaching 50% lower levels than the control."
- **Use:** logged as a concrete, quantified litter-management technology directly relevant to the operational/labor-adjacent welfare harms already in the model's parameter blocks; general animal science, not EA-vetted, flagged as such in the note

## 2026-09-03 — named-breed throughput ratio for slower-growing broilers (productivity penalty)

- **Task:** find a direct kg-output/animal-year (or bird-day) productivity comparison for slower-growing broiler breeds, to check the model's π_hw/π_conv and κ_π calibration for `literature/sads-and-welfare-campaigns.md` §5
- **Source:** (2022). The 'sustainability gap' of US broiler chicken production: trade-offs between welfare, land use and consumption. Royal Society Open Science.
- **ID:** DOI `10.1098/rsos.210478`
- **Quote:** conventional Ross 308 reaches "2.93 kg" live weight at "47 days"; slower-growing Ranger Classic, Ranger Gold, and Rowan Ranger reach "2.52", "2.27", and "2.43 kg" respectively at "57", "57", and "59 days"; to hold current consumption constant would need a "44.6%-86.8% larger population" of birds, and pasture housing "would require 108,642-121,019 km², a 43.8-60.1% increase over current land use."
- **Use:** computed (this note's own arithmetic, not a quoted ratio) a throughput-basis π_hw/π_conv of 0.64-0.71 for these three named breeds, below the model's current [0.75, 0.95] broiler band; used to argue the model's κ_π (calibrated from a land-use proxy) understates the true productivity penalty by a factor of ~3-4×

## 2026-09-03 — ECC broiler growth rate and days-to-slaughter, industry dataset

- **Task:** cross-check the RSOS breed-level throughput figures against the Wageningen dataset already used elsewhere in the model's parameter blocks
- **Source:** Wageningen Social & Economic Research (2025). Impact of the European Chicken Commitment (ECC) broiler production system on economics, the environment and food safety. Report 2025-138.
- **ID:** none found; URL `https://edepot.wur.nl/698861`
- **Quote:** ECC broiler growth rate is "around 55 grams per bird per day," classified as "medium-slow growing"; ECC broilers take "37 days to reach the thinning stage, and 51 days to reach cull weight."
- **Use:** logged as a second, industry-commissioned data point in the same direction as the RSOS figures; flagged that the matching conventional-breed growth rate needed to compute a directly comparable ratio was not located in this pass, so the two sources' ratios are reported separately rather than combined

## 2026-09-03 — laying hen productivity gap narrows with cage-free operational experience

- **Task:** check whether the model's assumed layer productivity penalty (mortality/output) is a stable biological effect or an artifact of production-system maturity
- **Source:** (2021). Laying hen mortality in different indoor housing systems: a meta-analysis of data from commercial farms in 16 countries. Scientific Reports.
- **ID:** DOI `10.1038/s41598-021-81868-3`
- **Quote:** "hen day egg production was higher in free-range systems but similar in conventional cage and enriched cage systems"; "each year of experience with cage-free aviaries was associated with a 0.35-0.65% average drop in cumulative mortality, with no differences in mortality between caged and cage-free systems in more recent years"; where mortality was high, "a primary cause was injurious pecking behavior."
- **Use:** basis for recommending the model demote the layer productivity penalty toward second-order/uncertain rather than a fixed ratio, since the direction of the effect is contested and appears to shrink with producer experience rather than being a stable biological penalty

## 2026-09-03 — sow productivity and mortality, crate vs group housing

- **Task:** find a productivity comparison for pigs under crate vs crate-free housing, relevant to the model's species-extension list (§8)
- **Source:** Welfare Footprint Institute (2022), summarizing an F1000Research cross-country analysis. Productivity and mortality of sows are worse in gestation crates.
- **ID:** none found; URL `https://welfarefootprint.org/2022/05/26/sows/` (underlying data: `https://f1000research.com/articles/11-564/v1`)
- **Quote:** "sow mortality is significantly higher, and annual pig production per sow significantly lower" in countries where gestation crates are the norm, compared to countries where crates are restricted.
- **Use:** logged as evidence against a universal "welfare improvement lowers productivity" assumption — for sows the cross-country direction runs the opposite way; flagged as ecological/confounded and not a precise ratio, since the underlying numeric chart could not be read in this pass

## 2026-09-03 — a more controlled crate-vs-group-housing litter comparison, smaller effect size

- **Task:** find a less-confounded (non-cross-country) productivity comparison to cross-check the ecological sow finding above
- **Source:** Pork Information Gateway. Sow and Litter Performance for Individual Crate and Group Hoop Barn Gestation Housing Systems: Progress Report III.
- **ID:** none found; URL via search, `https://porkgateway.org/resource/sow-and-litter-performance-for-individual-crate-and-group-hoop-barn-gestation-housing-systems-progress-report-iii/`
- **Quote:** group housing (hoop barns) resulted in "0.8 more pigs born per litter" and sows "weaned 0.4 more pigs per litter" compared to gestation crates.
- **Use:** a smaller, farm-trial-scale effect in the same (pro-group-housing) direction as the cross-country finding, used to note that even a controlled comparison does not show group housing as less productive

## 2026-09-03 — faster-growing broiler breeds have better feed conversion, a distinct metric from throughput ratio

- **Task:** check whether a feed-conversion-ratio (FCR) comparison of named breeds agrees in direction with the RSOS throughput-ratio finding
- **Source:** (breed comparison study, exact citation not confirmed in this pass — reported via secondary aggregation). Feed efficiency, growth performance, and carcass characteristics of a fast- and a slower-growing broiler hybrid.
- **ID:** none found (citation needs verification against the original journal article before use as a point estimate)
- **Quote:** a fast-growing hybrid had "a better feed conversion ratio (2.6 ± 0.1 versus 2.9 ± 0.1 kg feed per kg gain)" than the slower-growing hybrid; separately, Hubbard JA757 vs Ross 308/Cobb 500: the faster-growing breeds "grew faster, ate less feed and had better FCR and ADG."
- **Use:** direction-consistent secondary evidence (worse FCR for slower-growing breeds) cited in the note alongside the primary RSOS throughput ratios; **not** used as a standalone point estimate because the citation trail for the exact FCR numbers was not independently verified in this pass
