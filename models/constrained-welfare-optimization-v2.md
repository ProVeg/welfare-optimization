# Constrained optimization of farmed-animal welfare

### VERSION 2

A single-objective model: minimize cumulative Suffering-Adjusted Days (SADs), subject to the three ceilings in _Limits to Welfare_ (biophysical, socio-economic, operational). This is the ε-constraint reduction of the four-objective problem in `literature/best-models-welfare-problem.md`. Planetary pressure, retail cost, and labor are **hard constraints**, not competing objectives.

Joint output of applied-mathematician (architecture, well-posedness, algorithm) and welfare-specialist (named inputs, sourced values, uncertainty). Not a simulation: hand off to `model-engineer`.

---

## 1. Decision problem

**Planner.** An EA-style funder/advocate who, over a finite horizon, splits effort and funds between (i) raising per-animal welfare standards and (ii) reducing (or preventing growth of) demand for animal-source food.

**Objective (unique).** Minimize total farmed-animal SADs on \([t_0, T]\). Equivalently, maximize animal welfare defined as \(W := -J\).

**Unit.** The project literature uses Suffer Adjusted Days (SADs); _Limits to Welfare_ §6 asks for total SADs under welfare-only, reduction-only, and joint strategies.

We do **not** maximize \(N \times Q\), under the assumption that the quality of life $Q$ of an animal is optimal when its life contains $0$ SADs. As a consequence, larger herds cause an increase in SADs by definition.

**Horizon.** \(t_0 = 2026\), \(T = 2050\) (FAO/EAT-Lancet planning year). Report 2033 as a checkpoint (Rethink Priorities headcount forecasts).

**Decisions.** Time-varying controls

- \(u_W(t)\): intensity of welfare-standard campaigns (cage-free, ECC, enforcement);
- \(u_D(t)\): intensity of demand reduction / demand-growth prevention (alt proteins, institutional defaults, policy).

**Constraints.** At every \(t \in [t_0,T]\):

1. Biophysical: livestock impacts stay inside the food-system planetary allocation.
2. Socio-economic: retail price stays below the mass-market willingness-to-pay (WTP) ceiling (else backsliding).
3. Operational: animal-to-staff ratios stay inside the regime where individual care is feasible.
4. Budget and box bounds on controls.

**Why this is the right question.** Welfare improvements and demand reduction are not independent interventions. Higher \(Q\) raises land, feed, GHG, and cost per kilogram; without a fall in kilograms demanded, the three ceilings bind and either block further \(Q\) or inflate headcount (and SADs) via slower growth and small-bodied substitution.

---

## 2. Modeling family and alternatives

| Family                                           | Role here                                                                                                                             |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **ε-constraint optimal control** (this document) | Single SAD objective; former objectives 1, 3, 4 become path inequalities. Matches “limits,” avoids pricing 1 SAD in dollars or tCO₂e. |
| EMOO + IAM (NSGA-III / GLOBIOM)                  | Keep for later Pareto mapping. Not needed once the decision-maker has chosen welfare as the sole target.                              |
| Weighted-sum scalarization                       | Rejected: requires conversion rates; misses nonconvex front segments (Manoja et al., arXiv:2607.02803).                               |
| IMAP-IGS (Timp et al., arXiv:2607.17304)         | Use only if multiple _stakeholder preference functions_ must be aggregated. Here the preference is already scalar (SADs).             |
| Sheaf / TDA                                      | Later, for North–South leakage and discrete species jumps. Not required for the first global NLP.                                     |
| cLCA-MDP                                         | Stochastic/substitution extension once the deterministic control problem is coded.                                                    |

**Static snapshot** (§3) is an NLP: 2050 end-state, algebraic constraints. Use it to see the ceilings and to recover the three scenarios in _Limits to Welfare_ §6.

**Dynamic problem** (§4) is an ODE-constrained Bolza program extending `literature/welfare-differential-equations.md`. Use it for trajectories, backsliding, and timing of \(u_W\) vs \(u_D\).

The static problem is a restriction of the dynamic one (constant controls, ignore transients, enforce constraints only at \(T\)).

---

## 3. Static NLP (2050 snapshot)

### 3.1 Variables

| Symbol               | Meaning                                                       | Domain               | Units            |
| -------------------- | ------------------------------------------------------------- | -------------------- | ---------------- |
| \(Y_s\)              | Animal-source **output** of species \(s\) in 2050             | \(\mathbb{R}\_{>0}\) | kg edible / year |
| \(\alpha_s\)         | Share of \(Y_s\) produced under a high-welfare protocol       | \([0,1]\)            | dimensionless    |
| \(u_{W,s}, u_{D,s}\) | Campaign effort (optional; or use \(Y,\alpha\) as primitives) | \([0,1]\)            | dimensionless    |

Species index \(s \in \mathcal{S} = \{\text{broiler},\ \text{layer},\ \text{pig},\ \text{cattle},\ \text{finfish}\}\). Shrimp and farmed insects are an extension (§8).

Headcount is **derived**, not chosen. Demand is for kilograms, not animals:

\[
N_s \;=\; Y_s \left( \frac{1-\alpha_s}{\pi_{s,\mathrm{conv}}} + \frac{\alpha_s}{\pi_{s,\mathrm{hw}}} \right),
\]

where \(\pi_{s,\cdot}\) is edible kilograms per animal-year (or per animal slaughtered, consistently). Because \(\pi_{s,\mathrm{hw}} < \pi\_{s,\mathrm{conv}}\) (slower growth, lower density, higher layer mortality), raising \(\alpha_s\) at fixed \(Y_s\) **increases** \(N_s\). This is the productivity trade-off in _Limits to Welfare_ §5 and Martinic et al. (2026).

### 3.2 Single objective

Let \(\varphi_{s,\mathrm{conv}}, \varphi_{s,\mathrm{hw}}\) be SAD rates per animal-year (or per slaughtered animal × lifespan, consistently). Total SADs in the snapshot year:

\[
J_{\mathrm{static}}(Y,\alpha)
\;=\;
\sum_{s\in\mathcal{S}}
\omega_s\, N_s
\bigl[(1-\alpha_s)\,\varphi_{s,\mathrm{conv}} + \alpha_s\,\varphi_{s,\mathrm{hw}}\bigr].
\]

\(\omega_s\) is a species welfare-range weight (Rethink Priorities mixture; chicken 50th percentile \(0.332\) relative to human \(=1\)). If \(\varphi\) is already in SADs, \(\omega_s\) is absorbed in \(\varphi\).

**Minimize** \(J\_{\mathrm{static}}\). Optional signed-welfare variant (not the default): replace \(\varphi\) by \(\varphi - \varphi^\dagger\) with a neutrality threshold; default is that conventional and ECC/cage-free lives remain net-negative (_Limits to Welfare_ §8).

### 3.3 Constraints

**Biophysical (vector).** For impact \(k \in \{\mathrm{GHG},\ \mathrm{land},\ \mathrm{P},\ \mathrm{N},\ \mathrm{water}\}\):

\[
\sum_{s\in\mathcal{S}} Y_s
\bigl[(1-\alpha_s)\, e_{s,k}^{\mathrm{conv}} + \alpha_s\, e_{s,k}^{\mathrm{hw}}\bigr]
\;\le\;
E_k^{\lim}.
\]

Here \(e\_{s,k}\) is impact per kilogram (Poore & Nemecek 2018 baseline; Wageningen 2025 / Martinic 2026 welfare markups). \(E_k^{\lim}\) is the livestock share of the EAT-Lancet 2025 food-system boundary.

**Socio-economic.** Relative retail price of species \(s\):

\[
\frac{P_s}{P_{s,0}}
\;=\;
(1-\alpha_s) + \alpha_s\, h_s
\;\le\;
P_s^{\lim}/P_{s,0},
\]

with \(h_s > 1\) the high-welfare cost multiplier (ECC \(\approx 1.19\)). If a single meat-basket price is preferred:

\[
P \;=\; \sum_s \nu_s P_s \;\le\; P^{\lim},
\]

\(\nu_s\) expenditure shares. Crossing \(P^{\lim}\) is modeled as infeasible in the static NLP (voluntary campaigns cannot hold \(\alpha\) there). The dynamic model makes this a backsliding ODE instead of a hard cut.

**Operational.**

\[
\sum_s \ell_s(\alpha_s)\, N_s \;\le\; L^{\mathrm{cap}},
\]

\(\ell_s(\alpha)\) labor hours per animal-year, increasing in \(\alpha\) (individual inspection, slower slaughter lines).

**Demand and budget.**

\[
Y_s \;=\; Y_{s,\mathrm{BAU}} \left(1 - \delta_s(u_D)\right)
\left(1 - \varepsilon_s \frac{P_s - P_{s,0}}{P\_{s,0}}\right)
S_s(P),
\]

\[
\sum_s \bigl( c_{W,s} u_{W,s} + c_{D,s} u_{D,s} \bigr) \;\le\; B,
\quad
0 \le u_{W,s}, u\_{D,s} \le 1.
\]

\(S_s(P)\) is a species-replacement map, sign and magnitude **species-pair- and region-specific, not a universal "large-bodied up ⇒ poultry up" rule**: cut-level US choice data show ground beef and pork chop demand roughly \(2\times\) more cross-price-sensitive to a poultry-price change than the reverse, shrinking near \(P^{\lim}\) (Lusk and Tonsor 2016); but a national AIDS demand system for Canada finds beef–poultry and beef–pork are net **complements** (negative cross-price elasticity) even though some provinces show substitution (Diakité, arXiv:2402.13439, Table 8). Treat \(S(P)\) as an asymmetric, sign-uncertain matrix to be swept, not a monotone map assumed from _Limits to Welfare_ §4 alone. \(\delta_s(u_D)\) is demand reduced (Global North) or growth prevented (Global South) as a function of effort.

**Attainable welfare share.** \(\alpha_s \le a_s(u_{W,s})\), with \(a_s\) concave (diminishing campaign returns).

### 3.4 Compact form

\[
\begin{aligned}
\min_{Y,\alpha,u}\quad
& J_{\mathrm{static}}(Y,\alpha) \\
\text{s.t.}\quad
& g_k(Y,\alpha) \le 0, \quad k \in \mathcal{K} \quad \text{(biophysical, price, labor, budget)}, \\
& Y = \Gamma(u_D, P(\alpha)), \quad
\alpha \le a(u_W), \quad
(Y,\alpha,u) \in \mathcal{X}.
\end{aligned}
\]

\(\mathcal{X}\) is a compact box, \(J_{\mathrm{static}}\) is continuous, constraint set closed. A minimizer exists if the feasible set is nonempty (Weierstrass). Feasibility can fail if \(Y_{\mathrm{BAU}}\) already violates \(E^{\lim}\) at \(\alpha = 0\); then some \(u_D > 0\) is **necessary** for existence, which is the static form of the stability criterion in the ODE note.

### 3.5 Diagnostic: three scenarios (_Limits to Welfare_ §6)

These are **not** optima; they are feasible-set probes.

| Scenario       | Controls                   | Typical binding constraints                                                                           |
| -------------- | -------------------------- | ----------------------------------------------------------------------------------------------------- |
| Welfare-only   | \(u_D = 0\), \(u_W\) large | \(P \le P^{\lim}\) and/or \(E \le E^{\lim}\) cap \(\alpha\); \(N\) follows BAU (plus \(\pi\) penalty) |
| Reduction-only | \(u_W = 0\), \(u_D\) large | \(\alpha\) stuck at baseline; \(E,P\) slack                                                           |
| Joint          | both free                  | \(\alpha\) can rise because \(Y\) (hence \(E,P,N/L\)) has been lowered                                |

The Gemini sketch in `literature/pdf/` is this diagnostic with a scalar \(\alpha\), scalar \(H\), and \(\bar s = 1 - 0.40\alpha\). Keep it as a communication device; do not use its blended \(r\_{\mathrm{hw}} = 1.345\) as a scientific point estimate (that number is not in Wageningen or Martinic).

---

## 4. Dynamic optimal control (ODE-constrained)

Extend the state \(\mathbf{x}(t) = \bigl(Y(t), Q(t), E(t), P(t), L(t)\bigr)\) of `literature/welfare-differential-equations.md`. Headcount is algebraic:

\[
N(t) \;=\; \frac{Y(t)}{\pi\bigl(Q(t)\bigr)}\, S\bigl(P(t)\bigr).
\]

For a first implementation, treat one aggregate “small-bodied” composite (poultry + finfish dominate SADs). Species-disaggregated copies of the same ODE are the v1.1 extension.

### 4.1 Controls and objective

Controls \(u(t) = \bigl(u_W(t), u_D(t)\bigr) \in \mathcal{U} = [0,1]^2\), measurable.

SAD rate per animal-year \(\phi\bigl(Q\bigr)\), strictly decreasing, \(\phi(0) = \varphi_{\mathrm{conv}}\), \(\phi(Q_{\mathrm{ECC}}) = \varphi\_{\mathrm{hw}}\). Default interpolant: linear in \(Q\). Cumulative objective (Bolza):

\[
J[u]
\;=\;
\int\_{t_0}^{T} e^{-\rho t}\, \omega\, N(t)\, \phi\bigl(Q(t)\bigr)\, dt
\;+\;
e^{-\rho T}\, \Psi\bigl(\mathbf{x}(T)\bigr).
\]

Default \(\rho = 0\) (undiscounted SADs, matching “total SADs to 2050”). Terminal \(\Psi\) optional (e.g. penalize remaining \(N\phi\) after 2050 if lock-in is a concern; _Limits to Welfare_ §7). **Minimize** \(J\).

### 4.2 Dynamics

Let \(A_W(t) = u_W(t)\, \exp\bigl(-\psi (P(t) - P^{\lim})_+\bigr)\) (advocacy collapses past the WTP ceiling).

\[
\begin{aligned}
\dot Y
&=
\left[
r(t)\left(1 - \varepsilon \frac{P-P_0}{P_0}\right) S(P)
\;-\;
\lambda_D u_D
\right] Y, \\
\dot Q
&=
\eta_W A_W \,(Q_{\max} - Q)
\;+\;
\eta_{\rho}\, \bigl(1 - N/N_{\rho}\bigr)_+ (Q_{\max} - Q)
\;-\;
\sigma\!\left(\frac{N}{L}\right) Q, \\
\dot E
&=
\alpha_E\, N \bigl(1 + \kappa Q\bigr)
\;-\;
\delta_E E, \\
\dot P
&=
\gamma \bigl[ h(Q)\, e^{\beta (E-E_0)/E^{\lim}}\, \bigl(N_{\delta}/\min\{N,N\_{\delta}\}\bigr)^{\nu} - P \bigr], \\
\dot L
&=
\theta_L A_W N - \delta_L L.
\end{aligned}
\]

This is the existing five-equation system with two corrections:

1. **Demand \(Y\) vs headcount \(N\).** \(N = Y\, S(P)/\pi(Q)\). The old \(\dot N\) equation mixed demand growth with substitution; those now sit in \(\dot Y\) and in the map \(N(Y,Q,P)\).
2. **Controls are explicit.** \(\lambda\_{\mathrm{DR}}(t) = \lambda_D u_D(t)\), \(A_W(t)\) as above. The planner chooses \(u\), not the exogenous paths.
3. **Density relief (threshold).** \(\bigl(1-N/N_{\rho}\bigr)_+\) is zero at today's headcount. It turns on only after \(N\) falls far enough that leftover housing/land is used as lower stocking density rather than mothballed sheds (Dawkins et al. 2004: density bites mainly at very high kg/m²; Buijs et al. 2009: no single density cliff; Waterhouse 1996: cutting stock without keeping care inputs does not raise performance). This is _enabling_ space for \(Q\), not an automatic good life. Labor failure \(\sigma(N/L)\) still dominates if staff are cut with the herd.
4. **Delicacy / residual-luxury price.** \(\bigl(N_{\delta}/\min\{N,N_{\delta}\}\bigr)^{\nu}\) is 1 until \(N<N\_{\delta}\). Below that, remaining meat carries a quantity premium (inverse-demand / selection of high-WTP buyers; Lusk and Tonsor 2016: meat demand more inelastic at higher prices; livestock price tracking demand–supply imbalance, Dieci et al. arXiv:1803.05404). This is **not** the shift of the demand curve from \(u_D\): a pure demand campaign would \_lower_ \(P\). The extra factor is farm exit plus remaining consumption as a luxury. Keep \(\nu \ll 1/\varepsilon\) so a 50% headcount cut is a modest premium, not a \(2^{1/\varepsilon}\) spike.

**Regularity (required for the NLP transcription).** Replace \((x)_+\) by a smooth plus \(\frac12\bigl(x + \sqrt{x^2+\epsilon}\bigr)\), \(\epsilon \sim 10^{-6}\). Take \(\sigma(\xi) = \sigma_0 \xi^p / (\xi_\star^p + \xi^p)\) (smooth saturating failure rate), \(p \ge 2\). Take \(h \in C^2\), \(h' > 0\), \(h'' \ge 0\), \(h(0) = P_0\). Take \(\pi(Q) = \pi_0 / (1 + \kappa_\pi Q)\) with \(\kappa\_\pi > 0\). Then the vector field is \(C^1\) on a neighborhood of the positive orthant, hence locally Lipschitz: IVPs are unique.

**Initial conditions** \(\mathbf{x}(t_0) = \mathbf{x}\_0\) from the parameter block (§7).

**Invariants / bounds.** \(Y,Q,E,P,L > 0\), \(Q(t) \in [0, Q_{\max}]\). The \((Q_{\max}-Q)\) factor and \(\sigma \ge 0\) keep \(Q\) in range if \(Q(t_0) \in [0,Q_{\max}]\).

### 4.3 Path and control constraints

\[
\begin{aligned}
E(t) &\le \max\{E^{\lim},\, 1.05\, E(t_0)\}
\quad\text{(never worsen an already-transgressed allocation)}, \\
E(T) &\le E^{\lim}
\quad\text{(restore the livestock FSB by 2050, if \(E\) is flow-like)}, \\
P(t) &\le P^{\lim}, \\
N(t)/L(t) &\le \xi^{\lim}
\quad\text{or equivalently}\quad
\sigma(N/L) \le \sigma^{\lim}, \\
c_W u_W(t) + c_D u_D(t) &\le B(t), \\
0 \le u_W(t), u_D(t) &\le 1.
\end{aligned}
\]

These are **state-inequality path constraints**. Open-loop diagnostics may start with \(E(t_0) > E^{\lim}\) (current food systems already transgress the EAT-Lancet 2025 FSBs and Richardson et al. 2023 planetary boundaries). Requiring \(E(t)\le E^{\lim}\) at every \(t\) is then empty. When the 2050 restoration constraint is active, the control (typically \(u_D\)) must cut headcount so the flow-like pressure \(E\) falls through \(E^{\lim}\). The price scarcity factor is \(e^{\beta(E-E_0)/E^{\lim}}\), so \(P_0\) matches today's already-overshot state.

**Stability criterion (necessary for a high-\(Q\) equilibrium inside the ceilings).** From \(\dot Y = 0\) and \(E \le E^{\lim}\):

\[
\lambda_D u_D
\;\ge\;
r(t)\left(1 - \varepsilon \frac{P-P_0}{P_0}\right) S(P)
\quad\text{and}\quad
\frac{Y}{\pi(Q)} (1+\kappa Q) \;\lesssim\; E^{\lim}.
\]

If \(u_D \equiv 0\) and \(r > 0\), no interior steady state with both high \(Q\) and \(E \le E^{\lim}\) exists. That is the ODE form of “demand reduction is a prerequisite.”

### 4.4 Well-posedness of the OCP

Assume the smoothed dynamics, compact \(\mathcal{U}\), continuous running cost, and a nonempty feasible set (path constraints compatible with some \(u \in L^\infty([t_0,T];\mathcal{U})\)). Filippov-type existence of an optimal control holds. Uniqueness is not expected: the problem is **nonconvex** (bilinear \(N\phi(Q)\), convex-increasing \(h(Q)\), exponential scarcity, species map \(S\)). Report local minima from multi-start, not a single “the” optimum.

LICQ may fail at corners where several ceilings activate together (Ipopt is then less reliable; see §5).

---

## 5. Algorithm class

**Primary (v1).** Direct transcription of §4 to a sparse NLP:

1. Discretize \([t_0,T]\) with \(N_t \sim 50\)--\(100\) collocation intervals (trapezoidal or Radau).
2. Decision vector: \(\{Y_i, Q_i, E_i, P_i, L_i, u_{W,i}, u_{D,i}\}_{i=0}^{N_t}\).
3. Defect constraints for the ODEs; inequality constraints for path and budget at nodes.
4. Solve with an interior-point NLP solver (**Ipopt**), from several initial guesses (welfare-only, reduction-only, joint, BAU).

This matches the repo stack (`literature/welfare-models-architecture.md`): **GEKKO** (orthogonal collocation on finite elements + Ipopt) or **Pyomo** + `pyomo.dae` + Ipopt. Conventional wisdom for a cold-start NLP is to try Ipopt first (Guffroy, Eltved & Diamond, arXiv:2606.02896).

**Validity.** Smooth \(C^2\) transcription; scaling so that states are \(O(1)\); path constraints enforced at collocation points (and, if they chatter, with a slack / barrier). Not valid as a global solver: nonconvex, so multi-start is mandatory.

**If collocation oscillates on the \(E\) or \(P\) boundary.** Integrated-residual regularized direct collocation (IRR-DC; Peng et al., arXiv:2503.09123) or a simple \(L^2\) penalty on \(\dot u\). If the active-set structure of \(E \le E^{\lim}\) is the story, SPOC-style domain splitting (adaptive Radau with tangency conditions) is the specialized method; it is overkill until GEKKO fails.

**Static NLP (§3).** Same Ipopt path, no DAE. Use as (i) a sanity check, (ii) a generator of terminal targets, (iii) the three-scenario table.

**Do not use for v1.** NSGA-III (no second objective), Mesa ABM (labor microfoundation can wait), sheaf cohomology.

**Sensitivity.** After a local optimum, finite-difference or Ipopt adjoints on first-order parameters (§7.2). If the sign of “joint beats welfare-only” flips inside the uncertainty ranges, that is the result, not a bug.

---

## 6. Numerical caveats

- **Nonconvexity / multi-modality.** Welfare-only can look locally good on a short horizon (SADs fall while \(\alpha\) rises) and then hit \(P^{\lim}\) and collapse \(Q\) (simulation figure in `literature/welfare-simulation.png`).
- **Stiffness.** \(\sigma(N/L)\) and the exponential scarcity \(e^{\beta (E-E_0)/E^{\lim}}\) can be stiff near ceilings. Implicit collocation, not explicit RK, in the loop.
- **Scaling.** \(N\) is \(10^{10}\)--\(10^{11}\); \(Q \in [0,1]\); \(P/P_0 \sim 1\). Nondimensionalize (\(Y/Y_0\), \(E/E^{\lim}\), \(P/P_0\), \(L/L_0\)).
- **Units of \(N\).** Pick either standing population or animals slaughtered per year and stay there. SADs \(\times\) standing \(\times\) \(\phi\) (per year) equals SADs \(\times\) slaughtered \(\times\) \(\phi\) (per life) only if \(\phi\) is converted by lifespan.
- **Smoothing.** The plus function in \(A_W\) and any \(\max\) in \(\sigma\) destroy classical derivatives if left unsmoothed.
- **Index of path constraints.** On \(E = E^{\lim}\), control appears only after differentiating \(\dot E\); naive collocation can chatter. Start with a slightly softened constraint \(E(t) \le E^{\lim}\) plus a slack penalty.
- **Species jumps.** \(S(P)\) should be \(C^1\). A step from beef to broiler is a discrete jump; if that channel dominates, move to mixed-integer or to the sheaf/TDA layer.
- **Infeasibility of BAU.** If BAU already exceeds \(E^{\lim}\), the solver must be allowed to use \(u_D > 0\). Do not initialize at BAU with tight ceilings and no reduction.

---

## 7. Parameters (welfare-specialist)

Values are **point estimate / range / trajectory / unknown**, never a single unexplained number. Gemini-document figures that are not in primary sources are not used as point estimates.

### 7.1 Which parameters move the answer

**First-order.** BAU demand path \(r(t)\) and its Global South share; initial headcount/output \(N_0,Y_0\) by species; SAD rates \(\varphi_{\mathrm{conv}}, \varphi_{\mathrm{hw}}\); welfare-impact markups \(e^{\mathrm{hw}}/e^{\mathrm{conv}}\) and \(\pi_{\mathrm{hw}}/\pi\_{\mathrm{conv}}\); own-price elasticity \(\varepsilon\); WTP ceiling \(P^{\lim}\); planetary allocation \(E^{\lim}\); species replacement \(S(P)\); how much demand \(u_D\) can actually shift (\(\lambda_D\)).

**Second-order.** Discount \(\rho\); environmental recovery \(\delta_E\); labor depreciation \(\delta_L\); density-relief rate \(\eta_{\rho}\) and delicacy exponent \(\nu\) (sweep; they change \(Q\) and \(P\) on deep demand cuts); advocacy cost \(c_W\) vs \(c_D\) except when the budget is very tight; shrimp/insects (huge \(N\), low \(\omega\), weak current campaign lever); AI substituting for \(L\); feed-tech decoupling of \(\kappa\).

### 7.2 Parameter blocks

### BAU growth rate of animal-source output

- **Symbol:** \(r(t)\)
- **Definition:** Instantaneous growth rate of edible animal-source kilograms under no extra demand-side intervention and constant real prices.
- **Units:** 1/year
- **Point estimate:** \(\approx 0.010\)--\(0.012\) globally for meat tonnage (OECD-FAO _Agricultural Outlook 2025–2034_: production \(365 \rightarrow 406\) Mt carcass-weight equivalent by 2034, about \(+13\%\) in a decade; _Limits to Welfare_ cites FAO/OWID \(\approx +25\%\) meat to 2050, consistent with \(\sim 0.9\)--\(1.1\%\)/year over 24 years).
- **Uncertainty / range:** \(0.007\)--\(0.018\). Headcount of **small-bodied** animals grows faster than aggregate tonnage.
- **Time development:** Positive through 2050; poultry is \(62\%\) of additional meat in the next OECD-FAO decade; growth concentrated in upper-middle-income countries.
- **Scope:** Global meat; fish/aquaculture additional.
- **Source:** OECD-FAO 2025–2034; Our World in Data “Global meat projections to 2050”; FAO long-run outlooks.
- **Confidence:** medium for tonnage; lower for 2050 headcount.

### Broiler numbers (baseline)

- **Symbol:** \(N\_{\mathrm{br}}(t_0)\), slaughter and standing
- **Definition:** Broilers slaughtered per year and alive at a given time.
- **Units:** animals / year and animals
- **Point estimate:** Slaughter \(76.2 \times 10^9\) (2023) \(\rightarrow\) \(87.3 \times 10^9\) (2033), \(+14.6\%\). Standing \(10.1 \times 10^9 \rightarrow 11.6 \times 10^9\).
- **Uncertainty / range:** Rethink Priorities treat this as a rough forecast; use \(\pm 15\%\) as a sensitivity band unless they publish CIs for broilers.
- **Time development:** \(\approx 1.4\%\)/year 2023–2033; do not blindly extend at that rate to 2050 (saturation possible).
- **Scope:** Global broilers.
- **Source:** McKay (Moulange) & Shah, Rethink Priorities (2025), _Forecasting farmed animal numbers in 2033_.
- **Confidence:** medium (transparent but “rough-and-ready”).

### Finfish numbers (baseline)

- **Symbol:** \(N\_{\mathrm{ff}}(t_0)\)
- **Definition:** Farmed finfish slaughtered per year and standing.
- **Units:** animals / year and animals
- **Point estimate:** Slaughter \(133.6 \times 10^9\) \([86.0,\ 181.2] \times 10^9\) (2023) \(\rightarrow\) \(155.1 \times 10^9\) \([99.8,\ 210.4] \times 10^9\) (2033), \(+16.1\%\). Standing \(222.6 \times 10^9 \rightarrow 258.6 \times 10^9\).
- **Uncertainty / range:** 90% subjective CI as quoted.
- **Time development:** \(\approx 1.5\%\)/year on the midpoint.
- **Scope:** Farmed finfish globally.
- **Source:** McKay & Shah (2025), Rethink Priorities.
- **Confidence:** low–medium (wide CI).

### Price elasticity of meat demand

- **Symbol:** \(\varepsilon\) (model uses \(\varepsilon > 0\) in \(1 - \varepsilon (P-P_0)/P_0\); literature quotes negative own-price elasticities)
- **Definition:** Percent drop in quantity demanded for a 1% rise in own price, other prices fixed.
- **Units:** dimensionless
- **Point estimate:** \(0.6\) as a central meat/poultry figure (Andreyeva et al. 2010: poultry \(0.68\), 95% CI \(0.44\)--\(0.92\); beef \(0.75\), pork \(0.72\)). _Limits to Welfare_ band \(0.4\)--\(0.7\).
- **Uncertainty / range:** \(0.3\)--\(0.9\) (Gallet 2010b; Gellman et al. 2023 _Food Policy_ meta-analysis: mostly inelastic, regional spread).
- **Time development:** Treat as constant; Global South may be more elastic (income and budget shares).
- **Scope:** High-income own-price elasticities are better measured than Global South.
- **Source:** Andreyeva, Long & Brownell, _AJPH_ (2010); Gallet, _AJAE_ (2010b); Gellman et al., _Food Policy_ (2023).
- **Confidence:** medium. Cross-price elasticities (beef \(\to\) chicken) are **first-order for SADs** and less well identified: use a sensitivity range on \(S(P)\) rather than a single matrix.

### Cross-price elasticities / species-replacement map S(P)

- **Symbol:** \(S_s(P)\), or the cross-price elasticity \(\eta_{s,s'} = \partial \ln Q_s/\partial \ln P_{s'}\)
- **Definition:** How demand for species \(s\) responds to a price change in species \(s'\); the mechanism behind \(S_s(P)\) in §3.3 and §4.2.
- **Units:** dimensionless
- **Point estimate:** **No single global matrix exists; sign is not universal.** Two disjoint estimates: (i) US cut-level choice-experiment arc elasticities (middle income, price increase): ground beef demand w.r.t. chicken-breast price \(+0.60\), pork chop w.r.t. chicken-breast \(+0.62\), vs chicken breast w.r.t. ground-beef price only \(+0.29\) and w.r.t. pork-chop price \(+0.18\) — large-bodied cuts are \(\sim 2\times\) more cross-sensitive to poultry price than the reverse. (ii) Canada national AIDS demand system (Marshallian, uncompensated): beef w.r.t. poultry price \(-0.043\), poultry w.r.t. beef price \(-0.392\), pork w.r.t. beef price \(-0.214\) — beef–poultry and beef–pork are **complements**, not substitutes, at the country level (though poultry–pork and lamb–pork are substitutes, and some provinces flip beef–poultry to substitutes).
- **Uncertainty / range:** Sign itself is uncertain for the beef/pork \(\leftrightarrow\) poultry pair (the pair that matters most for SADs, since it governs whether cutting large-bodied output pushes headcount toward small-bodied animals). Magnitude of any single cross-elasticity is \(\lesssim 0.6\) in both studies — an order of magnitude below the \(N\_\delta/\min\{N,N\_\delta\})^\nu\) delicacy term's intended effect, so do not let \(S(P)\) alone drive large headcount swings.
- **Time development:** Both cross- and own-price elasticities **shrink as the price level rises** (Lusk and Tonsor 2016: comparing their Table 3 vs Table 4, every cross-price entry is larger for a price _decrease_ than for the matched _increase_) — substitution weakens near \(P^{\lim}\), consistent with the existing \(\nu \ll 1/\varepsilon\) choice for the delicacy term.
- **Scope:** (i) US retail, cut-level (ground beef, steak, pork chop, deli ham, chicken breast/wing), single-market choice experiment, 2014–2015 high-price episode. (ii) Canada, national and provincial, species-aggregate, weekly retail data 2019–2022.
- **Source:** Lusk and Tonsor, _Applied Economic Perspectives and Policy_ (2016), doi:10.1093/aepp/ppv050, Tables 3–4; Diakité, _Estimating Demand for Lamb, Beef, Pork, and Poultry in Canada_, arXiv:2402.13439, Table 8.
- **Confidence:** low on sign for beef/pork \(\leftrightarrow\) poultry (two credible studies disagree); medium that substitution (whatever its sign) weakens at higher prices. Do not hard-code \(S_s(P)\) as monotonically increasing for small-bodied species; sweep both a substitutes-case and a complements-case.

### High-welfare cost multiplier (broilers, ECC)

- **Symbol:** \(h_{\mathrm{ECC}}\) or \(h(Q_{\mathrm{ECC}})\)
- **Definition:** Production cost relative to conventional at farm / after processing.
- **Units:** dimensionless (\(P/P_0\))
- **Point estimate:** \(+19\%\) farm, \(+16\%\) after slaughter, \(+19\%\) after processing (average of PL, DE, ES, FR, IT, NL).
- **Uncertainty / range:** Country spread roughly \(+17\%\) to \(+21\%\) at farm in that study; more ambitious systems (organic, pasture) are substantially higher (not quantified here as a single number).
- **Time development:** Level shift at conversion; capex is front-loaded.
- **Scope:** ECC broilers, six EU states, 2025.
- **Source:** van Horne et al., Wageningen Social & Economic Research report 2025-138.
- **Confidence:** high for EU ECC; low for Global South and for beyond-ECC.

### High-welfare biophysical markups (broilers, ECC)

- **Symbol:** \(e^{\mathrm{hw}}/e^{\mathrm{conv}}\), \(\kappa\)
- **Definition:** Extra impact per kg meat vs conventional.
- **Units:** dimensionless ratios
- **Point estimate:** GHG \(+11\%\) per kg meat after processing (\(+6\%\) farm, live weight); land \(+14.4\%\); phosphorus excretion \(+36.7\%\) per kg meat.
- **Uncertainty / range:** Indicator-dependent; do not blend into one \(1.345\). Use the vector \((1.11,\ 1.144,\ 1.367)\) or a worst-case \(\kappa\) equal to the P ratio if the binding planetary bound is nutrient.
- **Time development:** Level shift with breed/density; feed-tech could lower \(\kappa\) (unknown).
- **Scope:** ECC vs conventional, NL environmental module of Wageningen 2025.
- **Source:** Wageningen 2025-138; Faunalytics summary.
- **Confidence:** high for that comparison; medium as a global \(\kappa\).

### High-welfare markups (layers, cage-free)

- **Symbol:** \(e^{\mathrm{hw}}_{\mathrm{layer}}/e^{\mathrm{conv}}_{\mathrm{layer}}\), \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\)
- **Definition:** Extra GHG/land per tonne eggs, and extra hens per tonne, vs enriched cage.
- **Units:** ratios
- **Point estimate (project text):** enriched cage \(\to\) barn: GHG \(+56\%\), land \(+13\%\) per tonne eggs (Martinic et al. 2026, as cited in _Limits to Welfare_). Organic free-range vs BAU: GHG \(\sim +60\%\), land nearly \(\times 2\) (same paper, UK, constant egg output).
- **Uncertainty / range:** Underlying LCA data are partly 2009–2010; authors flag this. Mortality and hen numbers are higher in non-cage systems, so \(N\) rises at fixed \(Y\).
- **Time development:** UK/EU legal cage phase-outs move \(\alpha\_{\mathrm{layer}}\) independent of EA campaigns.
- **Scope:** UK egg systems; not Global South.
- **Source:** Martinic, Bartlett et al., _Royal Society Open Science_ (2026), doi:10.1098/rsos.251830.
- **Confidence:** medium (old inventory, UK-specific).

### Planetary / food-system ceilings

- **Symbol:** \(E_k^{\lim}\)
- **Definition:** Food-system allocation of planetary boundaries; livestock must fit inside a share of these.
- **Units:** GtCO₂e / year; M km² agricultural land; Tg P / year; Tg N / year
- **Point estimate:** Food systems are **already past** the 2025 EAT-Lancet food-system boundaries (FSBs), which are the food allocation of the planetary boundaries (Rockström et al. 2009; Steffen et al. 2015; Richardson et al. 2023 — six of nine PBs transgressed; food drives five of those). Current / FSB: climate \(16\)–\(17.7\) GtCO₂e yr\(^{-1}\) vs \(5\) (\(\approx 3.2\)–\(3.5\)); agricultural land \(48\) M km² vs \(48\) (\(\approx 1.0\)–\(1.09\), 37% vs 34% of land area); N surplus \(119\) vs \(57\) Tg N (\(\approx 2.1\)); P to surface water from food \(7.2\) vs \(4.6\) Tg P (\(\approx 1.6\)). If livestock’s share of the FSB equals its share of current food impact (Poore & Nemecek: 56–58% of food emissions, 83% of farmland), livestock / livestock-allocation equals food / FSB. Composite (arithmetic mean of the four ratios) \(\approx 2.0\). The v1 scalar is therefore \(E_0/E_{\lim} = 2.0\), not \(0.25\).
- **Uncertainty / range:** \(1.1\) (land-only) to \(3.4\) (climate-only). FAO farm-gate livestock \(4.3\) GtCO₂e (enteric + manure, excluding land-use change and feed energy) vs a 57% slice of the \(5\) Gt FSB (\(\approx 2.85\) Gt) still gives \(\approx 1.5\).
- **Time development:** Ceilings are 2050 _targets_. Today is already over; BAU raises pressure further. Open-loop \(E(t)\) may stay \(> E_{\lim}\). The optimizer must not require \(E(t_0)\le E_{\lim}\) (infeasible); it should not worsen the overshoot and should restore \(E(T)\le E\_{\lim}\).
- **Scope:** Global food system, not livestock-only.
- **Source:** EAT-Lancet Commission 2025; Crona et al., _Nature Food_ (2025) food-system boundaries; Rockström et al. (2009); Steffen et al. (2015); Richardson et al., _Science Advances_ (2023); Poore & Nemecek, _Science_ 360:987 (2018); FAO agrifood emissions 2023.
- **Confidence:** high that livestock is already outside the safe operating space; medium on the exact composite \(2.0\) (climate-only \(\sim 3.3\), land-only \(\sim 1.1\)).

### WTP / socio-economic price ceiling

- **Symbol:** \(P^{\lim}/P_0\)
- **Definition:** Relative price at which mass-market purchase intent and voluntary corporate commitments collapse.
- **Units:** dimensionless
- **Point estimate:** \(1.10\)--\(1.15\) for the mass market (_Limits to Welfare_: intent drops sharply beyond \(+10\)--\(15\%\); \(\sim 10\)--\(15\%\) of high-income consumers will pay \(+30\%+\)). ECC’s \(+19\%\) already sits above that mass-market band, matching observed ECC delays. Clark et al. (2017) meta-analysis: small positive WTP (\(\sim 0.63\) SD), highly heterogeneous; stated WTP overstates revealed WTP.
- **Uncertainty / range:** \(1.08\)--\(1.30\) in high-income markets; closer to \(1.00\)--\(1.08\) for a large Global South mass market (unknown; proxy: food budget share).
- **Time development:** Can rise slowly with affluence (_Limits to Welfare_ §8 “future affluence”); do not assume it.
- **Scope:** Voluntary markets. Mandates can exceed WTP until political rollback.
- **Source:** _Limits to Welfare_ §4; Clark et al., _Food Policy_ 68:112–127 (2017); ECC backsliding / ChickenTrack (as cited in the essay).
- **Confidence:** medium for the EU/US \(10\)--\(15\%\) kink; low for a global scalar \(P^{\lim}\).

### Density-relief threshold (quality vs headcount)

- **Symbol:** \(N_{\rho}\), \(\eta_{\rho}\)
- **Definition:** Headcount below which leftover housing/land is used as lower stocking density (not mothballed), so \(Q\) can rise without extra \(u_W\). Rate \(\eta_{\rho}\) is the extra approach of \(Q\) to \(Q\_{\max}\).
- **Units:** animals; 1/year
- **Point estimate:** \(N_{\rho} = 0.85 N_0\) (about a 15% cut before density relief; Dawkins et al. 2004: welfare harm from density is clear mainly at very high kg/m², \(\ge 42\); Estevez 2007: health compromised below \(\sim 0.0625\)--\(0.07\) m²/bird \(\approx 34\)--\(38\) kg/m²). \(\eta_{\rho} = 0.08\)/year is **calibration**, not a measured campaign rate.
- **Uncertainty / range:** \(N\_{\rho}/N_0 \in [0.7, 1.0]\). At \(1.0\) any cut raises \(Q\); at \(0.7\) only a large contraction does. Buijs et al. 2009: no single density cliff — different indicators move at different kg/m². Yang et al. arXiv:2602.00111: calf play vs space is **non-monotone** (peak \(8\)--\(10\) m²). Waterhouse 1996: extensification without keeping inputs does **not** raise performance.
- **Time development:** Housing stock is sticky on a 5–15 year campaign scale, then sheds are mothballed (relief fades). v1 keeps \(N\_{\rho}\) constant.
- **Scope:** Indoor poultry-like systems; weaker for already-extensive ruminants.
- **Source:** Dawkins, Donnelly & Jones, _Nature_ 427:342–344 (2004); Estevez, _Poultry Science_ 86:1265 (2007); Buijs et al., _Poultry Science_ 88:1536–1543 (2009); Waterhouse et al. in _Extensification_ (1996); Yang et al. arXiv:2602.00111.
- **Confidence:** high that _very high_ density harms welfare; medium that global \(N\) cuts translate into lower kg/m² rather than fewer intensive farms; low on \(\eta\_{\rho}\).

### Delicacy / residual-luxury price exponent

- **Symbol:** \(N\_{\delta}\), \(\nu\)
- **Definition:** Below \(N_{\delta}\), remaining meat carries a quantity premium \(\bigl(N_{\delta}/\min\{N,N\_{\delta}\}\bigr)^{\nu}\) on top of production cost. Proxy for farm exit plus high-WTP residual demand, not for a leftward demand-curve shift.
- **Units:** animals; dimensionless
- **Point estimate:** \(N\_{\delta} = 0.70 N_0\); \(\nu = 0.25\). A 50% headcount cut then marks up price by \((0.70/0.50)^{0.25} \approx 9\%\), inside the mass-market WTP band. Full inverse demand \(\nu = 1/\varepsilon \approx 1.7\) would explode \(P\) and is **rejected** for demand-side \(u_D\).
- **Uncertainty / range:** \(\nu \in [0, 0.5]\). \(\nu = 0\) recovers cost-only pricing. Lusk and Tonsor (2016): meat demand more inelastic at higher prices (convex inverse demand). US cattle-herd tightness raises beef prices (supply shock). A pure \(u_D\) demand shift would \_lower_ \(P\); this term is the opposing residual-luxury channel.
- **Time development:** Stronger if remaining consumers are high-income (selection); weaker if alternatives cap the premium.
- **Scope:** High-income residual markets; weaker where meat is still a calorie staple.
- **Source:** Lusk and Tonsor, _Applied Economic Perspectives and Policy_ (2016), doi:10.1093/aepp/ppv050; Dieci, Mignot, Westerhoff, arXiv:1803.05404; Gallet, _AJAE_ (2010b) for \(\varepsilon\); _Limits to Welfare_ §4 (10–15% of consumers pay \(+30\%+\)).
- **Confidence:** high that supply shocks raise meat prices; medium that a _smaller remaining industry_ behaves like a luxury; low on \(\nu\).

### SAD rates (suffering intensity)

- **Symbol:** \(\varphi_{s,\mathrm{conv}}, \varphi_{s,\mathrm{hw}}\), \(\phi(Q)\)
- **Definition:** Disabling-pain-equivalent days per animal-year (SADs). One human-day of disabling pain \(= 1\) SAD (Ambitious Impact / Charity Entrepreneurship).
- **Units:** SAD / animal-year (or SAD / animal-life)
- **Point estimate:** **Unknown as a single global number.** Do not use Gemini’s \(s\_{\mathrm{hw}} = 0.60\) as data. Construct \(\phi\) by interpolating Welfare Footprint time-in-pain for named systems (conventional broiler vs ECC; cage vs aviary), then multiply by sentience \(\times\) welfare range.
- **Uncertainty / range:** Rethink Priorities chicken welfare range 5th--50th--95th: \(0.002,\ 0.332,\ 0.869\) (human \(=1\)). Pain inventories differ by metric (SADs vs DCDEs); Šimčikas (2025) shows ranking of cage-free vs broiler vs plant-based **flips** with the metric. Treat \(\varphi_{\mathrm{hw}}/\varphi_{\mathrm{conv}} \in [0.4,\ 0.8]\) as a sensitivity band for ECC-like reforms, not a measurement.
- **Time development:** \(\phi\) depends on \(Q(t)\), not on calendar time except via campaigns.
- **Scope:** Species- and system-specific.
- **Source:** Charity Entrepreneurship, _SADs_ (method); Welfare Footprint Project (pain times); Rethink Priorities welfare ranges; ACE charity reviews using SADs (illustrative CEAs, not global totals).
- **Confidence:** low for absolute global SADs; medium for **ordinal** “ECC reduces per-animal pain but not to near zero.”

### Species welfare-range weights

- **Symbol:** \(\omega_s\)
- **Definition:** Relative capacity for welfare vs a typical human, mixture estimate.
- **Units:** dimensionless (human \(= 1\))
- **Point estimate (50th percentile):** pigs \(0.515\); chickens \(0.332\); octopuses \(0.213\); carp \(0.089\); salmon \(0.056\); shrimp \(0.031\); black soldier flies \(0.013\).
- **Uncertainty / range:** 5th--95th spans orders of magnitude (chickens \(0.002\)--\(0.869\)).
- **Time development:** Constant (normative), unless the planner changes moral weights.
- **Scope:** Eleven farmed taxa in the RP report.
- **Source:** Rethink Priorities, _Welfare Range Estimates_.
- **Confidence:** low in absolute terms; necessary for adding species. For a broiler-only v1, set \(\omega = 1\) and measure SADs in chicken-equivalent units.

### Productivity penalty

- **Symbol:** \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\), \(\kappa\_\pi\)
- **Definition:** Edible output per animal-year, high-welfare vs conventional.
- **Units:** dimensionless ratio
- **Point estimate:** For ECC, slower-growing breeds and lower density imply more animal-days per kg; land \(+14.4\%\) per kg is a **proxy** for extra feed/animals, not a direct headcount ratio. For layers, non-cage systems need more hens and have higher mortality at constant egg output (Martinic et al. 2026).
- **Uncertainty / range:** Broilers: try \(0.75\)--\(0.95\). Layers: try \(0.70\)--\(0.95\). Unknown precisely without converting FCR and days-to-slaughter.
- **Time development:** Could improve if high-welfare genetics close the FCR gap (unknown).
- **Scope:** ECC broilers; UK layers.
- **Source:** Wageningen 2025; Martinic et al. 2026; ADAS/AVEC ECC study (industry-commissioned; use as an upper-bound sensitivity, not as the central case).
- **Confidence:** medium directionally (\(\pi_{\mathrm{hw}} < \pi_{\mathrm{conv}}\)); low on the exact ratio.

### Demand-reduction control effectiveness

- **Symbol:** \(\lambda_D\)
- **Definition:** Fractional extra decay (or avoided growth) of \(Y\) per unit of sustained \(u_D = 1\).
- **Units:** 1/year
- **Point estimate:** **Unknown.** EAT-Lancet full Planetary Health Diet is a _scenario_, not a campaign production function. School Plates / Veganuary CEAs (Grilo 2025) and alt-protein forecasts (Dullaghan 2022; Peacock; Mazzarella 2025) say demand-side work is slower and more uncertain than corporate welfare on a **marginal-dollar SAD** basis — which is exactly the comparison this model rejects as incomplete.
- **Uncertainty / range:** Calibrate so that \(u_D \equiv 1\) can produce, as bounding scenarios: (i) \(\sim 4\%\)/year decline (the joint-strategy curve in `literature/welfare-simulation.png`, illustrative); (ii) freeze Global South per-capita demand at \(t_0\) (prevention); (iii) near-zero effect (skepticism case).
- **Time development:** Adoption S-curves are more realistic than constant \(\lambda_D\); v1 can keep \(\lambda_D\) constant and put an S-curve in v1.1.
- **Scope:** Global; mechanism differs North (reduction) vs South (prevention).
- **Source:** No single causal estimate. Anchors: EAT-Lancet 2025 diet scenarios; Grilo 2025; Dullaghan 2022; Mazzarella 2025.
- **Confidence:** low. **Must be swept.**

### Welfare-campaign effectiveness

- **Symbol:** \(\eta_W\)
- **Definition:** Speed at which \(Q\) approaches \(Q\_{\max}\) per unit of \(A_W\).
- **Units:** 1/year
- **Point estimate:** **Unknown** as a continuous rate. Discrete evidence: cage-free fulfillment often \(85\)--\(90\%\) where the cost was \(1\)--\(2\) ¢/egg; ECC fulfillment much worse (ChickenTrack: \(>58\%\) of tracked EU commitments with zero public progress — _Limits to Welfare_). Coefficient Giving: current corporate-campaign CE \(\sim 1/5\) of Šimčikas (2019).
- **Uncertainty / range:** Calibrate \(\eta_W\) so that \(u_W \equiv 1\), \(u_D = 0\) can raise \(Q\) to ECC-like levels in \(5\)--\(10\) years **before** ceilings bind, then let ceilings do the rest (qualitative match to the simulation figure).
- **Time development:** Diminishing returns as \(\alpha\) saturates the WTP-feasible market.
- **Scope:** Corporate campaigns, high-income and some middle-income retailers.
- **Source:** Šimčikas 2019, 2025; Oehlsen 2024; _Limits to Welfare_ §1 and §4.
- **Confidence:** low as a rate; high that effectiveness collapses as \(P \to P^{\lim}\).

### Operational labor ceiling

- **Symbol:** \(\xi^{\lim} = (N/L)^{\lim}\), \(L^{\mathrm{cap}}\)
- **Definition:** Animal-to-staff ratio above which legally required individual inspection/care fails (\(\sigma\) rises).
- **Units:** animals per FTE
- **Point estimate:** **Unknown** globally. Qualitative: EU broiler law requires inspection at least twice daily and isolation of sick animals; Dutch data show widespread untreated injuries (footpad dermatitis \(38\%\), hock burns \(20\%\), breast blisters \(6.5\%\) — De Jong et al., cited in _Limits to Welfare_). High-income agricultural employment \(\lesssim 5\%\) of the workforce.
- **Uncertainty / range:** Treat \(\xi^{\lim}\) as a sensitivity parameter; identify it so that BAU \(N\) with current \(L\) already sits near failure (the essay’s claim).
- **Time development:** \(L\) can rise with wages or AI (_Limits to Welfare_ §8); default \(\delta_L > 0\) (workforce decline) in the West.
- **Scope:** Intensive poultry/slaughter in high-income countries; Global South labor is less scarce but cash-constrained (the \(P\) ceiling binds first).
- **Source:** EU Directive 2007/43/EC and related Dutch decrees, via Dier & Recht (2014) as quoted in the essay; De Jong et al. 2011/2012.
- **Confidence:** high that the constraint is real; low on a numerical \(\xi^{\lim}\).

### Advocacy budget

- **Symbol:** \(B(t)\), \(c_W\), \(c_D\)
- **Definition:** Annual spend and relative cost of the two controls.
- **Units:** USD / year; USD per unit control
- **Point estimate:** **Unknown** for “the” planner. Historical split: \(\sim 60\%\) of disclosed EA AW donations 2019–2021 to corporate welfare, \(\sim 9\%\) to alt proteins (JamesOz 2021). EAAWF 2026–2028 priorities exclude institutional meat reduction and alt-protein advocacy.
- **Uncertainty / range:** Run both an unconstrained-\(B\) problem (physical ceilings only) and a tight-\(B\) problem. The first answers “what mix is required”; the second “what mix is affordable.”
- **Time development:** Optional constant \(B\).
- **Scope:** EA farmed-animal funding, not global livestock subsidies.
- **Source:** JamesOz 2021; EAAWF 2025 priorities (as cited in _Limits to Welfare_).
- **Confidence:** medium on the historical split; the model should not assume that split is optimal.

### Discount rate

- **Symbol:** \(\rho\)
- **Definition:** Pure time preference on SADs.
- **Units:** 1/year
- **Point estimate:** \(0\) (default).
- **Uncertainty / range:** \(0\)--\(0.04\).
- **Time development:** Constant.
- **Scope:** Normative.
- **Source:** None empirical; short AI timelines (_Limits to Welfare_ §7) argue for not heavily discounting pre-2050 lock-in.
- **Confidence:** n/a (value judgment).

---

## 8. Extensions (ordered)

1. **Two regions** (Global North / South). Separate \(Y, Q, P, u_D\). South: \(u_D\) is growth prevention; \(P^{\lim}\) tighter; \(r\) larger. First extension, not optional conceptually.
2. **Species vector.** Copy the ODE per \(s \in \mathcal{S}\); couple through \(S(P)\) and a shared land/GHG budget.
3. **Shrimp and insects.** First-order for 2033 _headcount_ (Rethink Priorities: invertebrates could be \(\sim 95\%\) of slaughter). Include once \(\varphi\) and \(\omega\) are in the SAD objective; otherwise they wash out.
4. **Stochastic substitution (cLCA-MDP).** Replace \(S(P)\) by a Markov kernel over diets.
5. **Sheaf consistency.** Regional welfare laws vs trade leakage as \(H^1 \ne 0\).

---

## 9. What this model is not

- Not a claim that demand reduction is cheaper per marginal SAD today.
- Not a Pareto front over climate, cost, labor, and welfare (that is the EMOO companion).
- Not parameterized tightly enough to output a dollar split. First-order elasticities \(\lambda_D, \eta_W, \varphi, P^{\lim}\) must be swept.
- Not a Python implementation.

---

## Formulation handoff

**Objectives:** Minimize \(J = \int\_{t_0}^{T} e^{-\rho t}\, \omega\, N(t)\, \phi(Q(t))\, dt\) with \(\rho = 0\) by default. Welfare \(W = -J\). No other objectives.

**Decision / state variables:**

- Controls: \(u_W(t), u_D(t) \in [0,1]\) (welfare-campaign and demand-reduction intensity).
- States: \(Y\) (kg animal-source food / year), \(Q \in [0,Q_{\max}]\) (mean quality), \(E\) (biophysical pressure, nondimensional \(E/E^{\lim}\)), \(P\) (retail price index), \(L\) (welfare labor).
- Algebraic: \(N = Y\, S(P) / \pi(Q)\) (animals; pick standing _or_ slaughter and keep it).

**Constraints:**

- Path: if \(E(t_0)\le E^{\lim}\) then \(E(t)\le E^{\lim}\) for all \(t\); if already overshot, \(E(t)\le 1.05 E(t_0)\) and \(E(T)\le E^{\lim}\). Also \(P(t)\le P^{\lim}\), \(N(t)/L(t)\le \xi^{\lim}\).
- Control: \(c_W u_W + c_D u_D \le B(t)\), box bounds.
- Dynamics and \(\mathbf{x}(t_0) = \mathbf{x}\_0\) with \(E_0/E^{\lim}\approx 2\) (composite current / livestock FSB).
- Static NLP of §3 as a 2050 diagnostic (three scenarios + true min).

**Dynamics:** Smoothed five-ODE system in §4.2, including density-relief \(\eta_{\rho}(1-N/N_{\rho})_+(Q_{\max}-Q)\) and delicacy markup \((N_{\delta}/\min\{N,N_{\delta}\})^{\nu}\) on the price target.

**Suggested algorithm family:** GEKKO or Pyomo.dae collocation + Ipopt; multi-start from welfare-only, reduction-only, joint, and BAU. Static §3 with the same solver. Do not start with NSGA-III.

**Numerical caveats:** Nonconvex (multi-start); stiffness near ceilings (implicit collocation); scale states to \(O(1)\); smooth \((P-P^{\lim})\_+\); path-constraint chatter; BAU may be infeasible under tight \(E^{\lim}\).

**Parameters still needed (values in §7; sweep if confidence is low):** \(r(t)\), \(Y_0\)/\(N_0\) by species, \(\varepsilon\), \(S_s(P)\) cross-price elasticities (sign uncertain for beef/pork \(\leftrightarrow\) poultry — sweep both signs), \(h(Q)\) and \(e^{\mathrm{hw}}/e^{\mathrm{conv}}\), \(\pi_{\mathrm{hw}}/\pi_{\mathrm{conv}}\), \(E^{\lim}\) (livestock quota of EAT-Lancet), \(P^{\lim}\), \(\varphi_{\mathrm{conv}}, \varphi\_{\mathrm{hw}}\) (or Welfare Footprint tables), \(\omega_s\), \(\lambda_D\), \(\eta_W\), \(\xi^{\lim}\), \(B, c_W, c_D\), \(\rho\).

**Outputs for the first simulation (model-engineer):**

1. Optimal \(u_W^\star(t), u_D^\star(t)\) and state trajectories vs the three diagnostic scenarios.
2. Cumulative SADs \(J\) for each.
3. Which constraint is active when \(Q\) stalls.
4. Tornado sensitivity on \(\lambda_D\), \(P^{\lim}\), \(\varphi_{\mathrm{hw}}/\varphi\_{\mathrm{conv}}\), \(\kappa\), \(r\).
5. Plots a non-mathematician can read: headcount, quality, biophysical pressure, price, with ceiling lines — same layout as `literature/welfare-simulation.png`, plus a SAD time series.

### Implementation notes (stack)

Map to `literature/welfare-models-architecture.md`: GEKKO (or Pyomo + Ipopt) for the OCP; `scipy.optimize` only for tiny static checks; `matplotlib` for the five-panel figure. No Mesa, no pymoo, until this NLP is running.
