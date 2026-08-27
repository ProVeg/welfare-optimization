# Literature reference log

When this agent uses a paper, preprint, book, or scientific report as the basis for a claim, model, algorithm, parameter, or implementation choice, append an entry to the matching file under `literature/references/` before finishing the turn.

Do not skip this because the source was already in `literature/` or in training data. Do not invent DOIs, arXiv IDs, or quotes.

## Files

| Topic | File |
| --- | --- |
| Formulations, theorems, model architectures | `literature/references/mathematical-models.md` |
| Solvers, numerical methods, optimization algorithms | `literature/references/algorithms.md` |
| Climate, agriculture, welfare, ecology, empirical science | `literature/references/biophysical-science.md` |

If one source spans two topics, log it once in the primary file and add a one-line pointer in the other.

## When to log

- Log: any scientific or mathematical source that actually changed what you wrote (equation, solver, parameter, interpretation).
- Skip: pure engineering with no literature (git, tests, file moves) and user instructions that are not literature.
- Same source, new quote or new use: new entry. Same quote for the same claim: skip.

## Entry format

Append after the last entry. Copy this block:

```markdown
## YYYY-MM-DD — short claim or choice

- **Task:** one sentence on what the agent was doing
- **Source:** Author (Year). Title.
- **ID:** DOI `10.…` and/or arXiv `YYMM.NNNNN` (both if both exist). If neither exists, URL. If none, write `none found`.
- **Quote:** verbatim 1–3 sentences the agent relied on (page or section if known)
- **Use:** how that quote justified the claim or choice
```

Example:

```markdown
## 2026-08-18 — NSGA-III for many-objective Pareto search

- **Task:** choose a solver family for four welfare/planetary objectives
- **Source:** Deb and Jain (2014). An Evolutionary Many-Objective Optimization Algorithm Using Reference-Point-Based Nondominated Sorting Approach, Part I: Solving Problems With Box Constraints.
- **ID:** DOI `10.1109/TEVC.2013.2281535`
- **Quote:** "NSGA-III uses a set of reference points to maintain diversity among population members in a many-objective problem."
- **Use:** selected NSGA-III rather than a weighted-sum scalarization
```
