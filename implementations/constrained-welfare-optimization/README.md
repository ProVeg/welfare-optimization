# Constrained welfare optimization

Python implementation of the aggregate 2026–2050 model in [`models/constrained-welfare-optimization.md`](../../models/constrained-welfare-optimization.md).

The only objective is **less total suffering** (Suffering-Adjusted Days). Environmental pressure, meat price, and animals-per-worker are **inequality ceilings**: they may sit below the limit; they must not be forced onto the limit.

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

## Run

```powershell
python -m cwo scenarios --config configs/default.yaml
python -m cwo optimize  --config configs/default.yaml
python -m cwo sensitivity --config configs/default.yaml
```

Override any parameter without editing files:

```powershell
python -m cwo scenarios --config configs/default.yaml --set lambda_D=0.02 --set P_lim=1.10
```

Use `--solver slsqp` if GEKKO/IPOPT is unavailable. Each run writes `outputs/<run_id>/` with frozen `params.yaml`, CSV trajectories, `summary.json`, `report.md`, and `figures/`.

Thin wrappers: `scripts/run_scenarios.py`, `run_optimize.py`, `run_sensitivity.py`.

## What the figures mean

| File | Question it answers |
| --- | --- |
| `trajectories.png` | How animals, quality of life, environmental pressure, price, and suffering move through 2050 |
| `controls.png` | How hard each strategy pushes welfare campaigns vs demand reduction |
| `slack.png` | How much room is left under each ceiling (negative = already broken) |
| `sad_bars.png` | Which strategy has less total suffering |
| `tornado.png` | Which input assumptions move that total the most |

Dotted horizontal lines on the trajectory plot are ceilings, not targets.

## Tests

```powershell
python -m unittest discover -s tests
```
