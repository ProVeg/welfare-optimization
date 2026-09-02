"""One-at-a-time sensitivity of the joint diagnostic's cumulative SADs."""

from __future__ import annotations

import copy
from pathlib import Path

from cwo.parameters import Params, load_yaml, params_from_mapping
from cwo.simulate import constant_control, simulate


def run_tornado(base_raw: dict, p: Params, spec_path: Path) -> tuple[list[dict], float]:
    spec = load_yaml(spec_path)
    joint = simulate(p, constant_control(0.5, 0.5), label="Joint (constant)")
    baseline = joint.J
    rows = []
    for key, item in spec["parameters"].items():
        raw_low = copy.deepcopy(base_raw)
        raw_high = copy.deepcopy(base_raw)
        raw_low[key] = item["low"]
        raw_high[key] = item["high"]
        p_low = params_from_mapping(raw_low)
        p_high = params_from_mapping(raw_high)
        j_low = simulate(p_low, constant_control(0.5, 0.5), label="low").J
        j_high = simulate(p_high, constant_control(0.5, 0.5), label="high").J
        rows.append(
            {
                "key": key,
                "label": item["label"],
                "low": item["low"],
                "high": item["high"],
                "low_j": j_low,
                "high_j": j_high,
                "span": abs(j_high - j_low),
            }
        )
    rows.sort(key=lambda r: r["span"], reverse=True)
    return rows, baseline
