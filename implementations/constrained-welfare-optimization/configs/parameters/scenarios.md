# `scenarios/*.yaml` — open-loop strategy definitions

Four constant-control diagnostics in `configs/scenarios/`, loaded by `python -m cwo scenarios` and plotted for comparison by `python -m cwo optimize`. `u_W` and `u_D` are campaign intensities on a dimensionless 0–1 scale (0 = no extra campaign that year, 1 = full intensity) that share **one unit annual advocacy budget**: \(c_W u_W + c_D u_D \le 1\). BAU, welfare-only, and reduction-only sit at corners of that budget (0, or all of it on one lever); joint splits it evenly.

| File | Label | \(u_W\) | \(u_D\) | Color | Linestyle | Meaning |
|---|---|---|---|---|---|---|
| `bau.yaml` | BAU | 0.0 | 0.0 | `#4d4d4d` | solid | No extra welfare campaigns, no extra demand reduction |
| `welfare_only.yaml` | Welfare-only | 1.0 | 0.0 | `#d95f02` | dashed | Whole unit budget on welfare-standard campaigns, none on demand reduction |
| `reduction_only.yaml` | Reduction-only | 0.0 | 1.0 | `#7570b3` | dotted | Whole unit budget on demand reduction, none on welfare campaigns |
| `joint.yaml` | Joint (constant) | 0.5 | 0.5 | `#1b9e77` | solid | Even 50/50 split of the unit budget — a diagnostic, not the optimizer's answer |
