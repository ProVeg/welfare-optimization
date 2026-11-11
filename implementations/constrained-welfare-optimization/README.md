# Constrained welfare optimization

Python implementation of the aggregate 2026–2050 model in [`models/constrained-welfare-optimization.md`](../../models/constrained-welfare-optimization.md).

The only objective is **less total suffering** (Suffering-Adjusted Days, SADs). Environmental pressure, meat price, and animals-per-worker are **hard ceilings**: they may sit below the limit; they must not be forced onto the limit. Welfare-standard campaigns (`u_W`) and demand-reduction campaigns (`u_D`) draw on **one shared unit annual advocacy budget** — that trade-off is the question this model answers.

Unknown campaign rates (`lambda_D`, `eta_W`) are **calibrated**, not measured. Change them in YAML or with `--set`.

## Setup (virtual environment)

From this folder, PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

If script activation is blocked:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

Unix:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

After install, `python -m cwo` and the `cwo` console script both work from this folder.

## How to run simulations

There are three commands. Each writes a new folder under `outputs/`.

```powershell
python -m cwo scenarios --config configs/default.yaml
python -m cwo optimize  --config configs/default.yaml
python -m cwo sensitivity --config configs/default.yaml
```

Thin wrappers do the same thing: `scripts/run_scenarios.py`, `run_optimize.py`, `run_sensitivity.py`.

### Commands

| Command | What it does |
| --- | --- |
| `scenarios` | Integrates four **open-loop** strategies with constant campaign intensity. Ceilings are **monitored**, not enforced. |
| `optimize` | Minimizes cumulative SADs with inequality path constraints. Also plots the four open-loop strategies for comparison. |
| `sensitivity` | One-at-a-time tornado around the joint diagnostic. Does **not** re-optimize the policy. |

The four open-loop strategies live in `configs/scenarios/*.yaml`. `u_W` and `u_D` are campaign intensities on a 0–1 scale that share **one unit annual advocacy budget** (`c_W*u_W + c_D*u_D <= 1`): spending more on one lever leaves strictly less for the other, so `(u_W,u_D)=(1,1)` is not feasible. Full table (colors, linestyles) in [`configs/parameters/scenarios.md`](configs/parameters/scenarios.md).

### Common flags

| Flag | Default | Meaning |
| --- | --- | --- |
| `--config PATH` | `configs/default.yaml` | Parameter file |
| `--set key=value` | none | Override a parameter without editing YAML. Repeatable. Dotted keys work (`horizon.T=2100`). |
| `--run-id NAME` | timestamp + command | Folder name under `outputs/` |

`optimize` also accepts:

| Flag | Default | Meaning |
| --- | --- | --- |
| `--solver gekko` | GEKKO + IPOPT collocation | Preferred dynamic solver |
| `--solver slsqp` | SciPy SLSQP, piecewise-constant controls | Use if GEKKO/IPOPT is unavailable |

`sensitivity` also accepts:

| Flag | Default | Meaning |
| --- | --- | --- |
| `--spec PATH` | `configs/sensitivity.yaml` | Low/high pairs for the tornado plot |

### Examples

Override campaign rates and the price ceiling:

```powershell
python -m cwo scenarios --config configs/default.yaml --set lambda_D=0.02 --set P_lim=1.10
```

Run a century path (the food-system allocation still binds from 2050):

```powershell
python -m cwo optimize --config configs/default.yaml --set horizon.T=2100 --run-id century-optimize
```

Force the SLSQP fallback and a stable output folder:

```powershell
python -m cwo optimize --config configs/default.yaml --solver slsqp --run-id eat-lancet-overshoot-opt
```

Custom tornado ranges:

```powershell
python -m cwo sensitivity --config configs/default.yaml --spec configs/sensitivity.yaml --run-id sanity-sensitivity
```

Re-run a past scenario to 2100 without optimizing, plus its tornado. A run's own `params.yaml` can be passed back as `--config`, so later edits to `default.yaml` don't change it. `configs/sensitivity-slow-advocacy.yaml` adds `eta_W`, `kappa_pi` (productivity lost per unit of welfare quality) and `s_coeff` (shift to smaller animals when prices rise) to the default ranges. Those three ranges are illustrative, not taken from literature.

```powershell
python -m cwo scenarios --config outputs/eat-lancet-overshoot-opt-slow-advocacy/params.yaml --set horizon.T=2100 --run-id eat-lancet-slow-advocacy-2100
python -m cwo sensitivity --config outputs/eat-lancet-overshoot-opt-slow-advocacy/params.yaml --set horizon.T=2100 --spec configs/sensitivity-slow-advocacy.yaml --run-id eat-lancet-slow-advocacy-2100-sensitivity
```

## Parameters

All model numbers live in `configs/default.yaml`. Nested `horizon.*` keys can be overridden as `horizon.T=2100`; everything else is a top-level key (`N0=1.01e10`). Rates tagged as calibration in the YAML are **not measurements** — they are set so the open-loop diagnostics behave as described in the model document.

For the full, human-scannable table of every key (units, value, meaning), see [`configs/parameters/`](configs/parameters/):

- [default.md](configs/parameters/default.md) — every key in `configs/default.yaml`, grouped by horizon/solver, demand, quality, prices, biophysical pressure, labor, and controls/budget.
- [sensitivity.md](configs/parameters/sensitivity.md) — the low/high tornado sweep in `configs/sensitivity.yaml`.
- [scenarios.md](configs/parameters/scenarios.md) — the four open-loop strategy configs in `configs/scenarios/*.yaml`.

Suffering is an **index**, not a census of global SADs. Rankings and ratios are the usable output; absolute billions are not a headcount of real days of suffering. Do not read `lambda_D` or `eta_W` as measured cost-effectiveness — they are knobs; the tornado plot shows how much the ranking moves when they (and other assumptions) change.

## Output structure

Each run creates `outputs/<run_id>/`. If you omit `--run-id`, the folder is `YYYYMMDD-HHMMSS-scenarios` (or `-optimize` / `-sensitivity`).

```
outputs/<run_id>/
  params.yaml              frozen copy of the parameters actually used
  summary.json             headline numbers for every strategy
  report.md                short narrative for a non-mathematician
  trajectory_<strategy>.csv
  figures/
    trajectories.png
    controls.png           (scenarios and optimize)
    slack.png              (scenarios and optimize)
    sad_bars.png
    tornado.png            (sensitivity only)
```

CSV stems come from the strategy label, lowercased, with spaces turned into underscores: `trajectory_bau.csv`, `trajectory_welfare-only.csv`, `trajectory_reduction-only.csv`, `trajectory_joint_constant.csv`, and on optimize runs `trajectory_optimum_gekko.csv` or `trajectory_optimum_slsqp.csv`.

### `params.yaml`

Exact configuration after `--set` overrides. Use this file, not `configs/default.yaml`, when you need to reproduce a past run.

### `summary.json`

| Field | Meaning |
| --- | --- |
| `J` | Cumulative suffering index for each strategy (lower is better) |
| `final_N` | Standing animals at the last year |
| `final_Q` | Average quality of life at the last year (0–1) |
| `min_slack_E` | Tightest (most negative) environmental slack during the run |
| `min_slack_P` | Tightest price slack |
| `min_slack_labor` | Tightest animals-per-worker slack |
| `static_J` | 2050 snapshot NLP values (`scenarios` only) |
| `optimum_J`, `optimum_solver`, `optimum_success`, `starts_tried` | Optimizer metadata (`optimize` only) |
| `tornado`, `baseline_joint_J` | Sensitivity rows (`sensitivity` only) |

Slack in this file is the **minimum over the whole path**. Negative means the ceiling was broken at least once.

### Trajectory CSVs

One row per output sample (`horizon.n_points`). Columns:

| Column | Meaning |
| --- | --- |
| `year` | Calendar year |
| `Y_kg_per_year` | Edible animal-source output (kg/year) |
| `Q` | Average quality of life (0–1) |
| `E` | Biophysical pressure as a share of the livestock allocation |
| `P` | Retail price index (`P0 = 1` today) |
| `L` | Farm labor (FTE index) |
| `N_standing` | Standing animals |
| `u_W`, `u_D` | Campaign intensities that year |
| `sad_per_year` | New suffering that year (index) |
| `J_cumulative_SAD` | Suffering added up from \(t_0\) (index) |
| `slack_E`, `slack_P`, `slack_labor`, `slack_budget` | Room under each ceiling (see below) |

### Figures

| File | Question it answers |
| --- | --- |
| `trajectories.png` | How animals, quality of life, environmental pressure, price, and suffering move through the horizon |
| `controls.png` | How hard each strategy pushes welfare campaigns vs demand reduction |
| `slack.png` | How much room is left under each ceiling (negative = already broken) |
| `sad_bars.png` | Which strategy has less total suffering |
| `tornado.png` | Which input assumptions move that total the most |

Dotted horizontal lines on the trajectory plot are **ceilings, not targets**.

## How to interpret the output

Start with `report.md`. It ranks strategies, says which ceilings broke, and states what the run does **not** show. Then use the figures; use the CSVs only if you need a number the report omitted.

### What “better” means

- **Lower cumulative \(J\)** is the only objective. Compare bars in `sad_bars.png` or the `J` block in `summary.json`.
- Open-loop rankings can disagree with the optimizer. The joint diagnostic often has the lowest *unconstrained* suffering, but it may break the price ceiling. The optimizer may pick reduction-only because that path is feasible.
- The problem is non-convex. A “succeeded” SLSQP/GEKKO run is a **local** minimum. `starts_tried` lists the constant-control starts; another start could do better.

### How to read slack

Slack is “room under the ceiling”:

- **Positive** — still below the hard limit.
- **Zero** — sitting on the limit (allowed; not a target).
- **Negative** — already over that ceiling.

Environmental slack **starts negative** whenever \(E_0 > E_{\lim}\) (default: \(E_0=2\)). That is today’s overshoot. Open-loop scenarios may stay over the environmental line. The optimizer must not raise pressure further and should be at or under the allocation from `fsb_year` (2050) onward.

Price and labor slacks near zero late in the run are the usual reason quality \(Q\) stalls or falls: campaigns cannot hold higher standards once meat is too expensive or staffing is too thin.

### How to read the four strategies

| Strategy | Typical pattern |
| --- | --- |
| BAU | Headcount and pressure keep rising; quality drifts down; often breaks labor (and stays over the environmental line). Highest suffering. |
| Welfare-only | Quality rises at first, then ceilings bind; more animals per kilogram (lower productivity) can **increase** headcount and pressure. Often infeasible. |
| Reduction-only | Headcount falls; pressure can return toward the allocation; quality stays low. Often the feasible SAD-minimizer. |
| Joint (constant) | Mixes both campaigns at constant intensity. Frequently the lowest *open-loop* suffering, but may break price. Not the optimized policy. |
| Optimum | Time-varying \(u_W(t), u_D(t)\) with ceilings enforced. Compare mean intensities in `report.md` and the control plot. |

If quality starts falling on the optimum path, check `slack.png` for which ceiling is tight at that year.

### The 2050 snapshot table

`report.md` also solves a **static** NLP: a 2050 end-state with algebraic ceilings, ignoring transients. “Feasible?” is only for that snapshot. A dynamic path can break a ceiling in 2035 and still look fine in 2050, or the reverse. Treat the table as a check, not a substitute for the trajectories.

### What the numbers are not

- They are not a dollar value of suffering, nor tonnes of CO₂.
- They do not split species or Global North vs South.
- Absolute SAD billions are an index scaled so conventional poultry-like lives are 1 per animal-year. Do not quote them as a global census.
- Ranking can flip if `lambda_D`, `P_lim`, or `phi_hw` moves. That is what `tornado.png` is for.

## Tests

```powershell
python -m unittest discover -s tests
```
