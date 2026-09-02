# Config parameter reference

Scannable tables of the actual numbers each YAML file in `configs/` feeds into the simulation — as opposed to [`models/parameters/`](../../../../models/parameters/), which tables the literature point estimates and ranges behind those choices.

- [default.md](default.md) — every key in `configs/default.yaml`, the central calibration.
- [sensitivity.md](sensitivity.md) — the low/high sweep in `configs/sensitivity.yaml`.
- [scenarios.md](scenarios.md) — the four constant-control diagnostics in `configs/scenarios/*.yaml`.

These tables mirror the YAML at time of writing, not a live query of it. If a config value changes, update the matching table in the same change.
