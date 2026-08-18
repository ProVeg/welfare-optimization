"""Command-line entry: scenarios, optimize, sensitivity."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from cwo.optimize import optimize
from cwo.parameters import dump_yaml, load_params, load_yaml
from cwo.plots import plot_controls, plot_sad_bars, plot_slack, plot_tornado, plot_trajectories
from cwo.report import write_report
from cwo.sensitivity import run_tornado
from cwo.simulate import constant_control, simulate
from cwo.static_nlp import diagnostics, solve_static

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "configs" / "default.yaml"
SCENARIO_DIR = ROOT / "configs" / "scenarios"
OUTPUT_ROOT = ROOT / "outputs"


def _run_id(name: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{name}"


def _outdir(run_id: str) -> Path:
    path = OUTPUT_ROOT / run_id
    path.mkdir(parents=True, exist_ok=True)
    (path / "figures").mkdir(exist_ok=True)
    return path


def _load_scenarios() -> list[dict]:
    rows = []
    for path in sorted(SCENARIO_DIR.glob("*.yaml")):
        data = load_yaml(path)
        data["id"] = path.stem
        rows.append(data)
    return rows


def _simulate_scenarios(p, scenarios: list[dict] | None = None):
    trajs = []
    for sc in scenarios or _load_scenarios():
        trajs.append(
            simulate(
                p,
                constant_control(float(sc["u_W"]), float(sc["u_D"])),
                label=str(sc["label"]),
                color=str(sc.get("color", "#333333")),
                linestyle=str(sc.get("linestyle", "-")),
            )
        )
    return trajs


def _write_common(out: Path, raw: dict, trajs, extra: dict | None = None) -> None:
    dump_yaml(raw, out / "params.yaml")
    for tr in trajs:
        stem = tr.label.lower().replace(" ", "_").replace("(", "").replace(")", "")
        tr.to_frame().to_csv(out / f"trajectory_{stem}.csv", index=False)
    summary = {
        "J": {tr.label: tr.J for tr in trajs},
        "final_N": {tr.label: float(tr.N[-1]) for tr in trajs},
        "final_Q": {tr.label: float(tr.Q[-1]) for tr in trajs},
        "min_slack_E": {tr.label: float(tr.slack_E.min()) for tr in trajs},
        "min_slack_P": {tr.label: float(tr.slack_P.min()) for tr in trajs},
        "min_slack_labor": {tr.label: float(tr.slack_labor.min()) for tr in trajs},
    }
    if extra:
        summary.update(extra)
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def cmd_scenarios(args: argparse.Namespace) -> Path:
    p, raw = load_params(Path(args.config), args.set)
    out = _outdir(args.run_id or _run_id("scenarios"))
    trajs = _simulate_scenarios(p)
    static_rows = diagnostics(p) + [solve_static(p)]
    _write_common(out, raw, trajs, {"static_J": {r.label: r.J for r in static_rows}})
    plot_trajectories(trajs, p, out / "figures" / "trajectories.png")
    plot_controls(trajs, out / "figures" / "controls.png")
    plot_slack(trajs, out / "figures" / "slack.png")
    plot_sad_bars(trajs, out / "figures" / "sad_bars.png", p)
    write_report(out / "report.md", p, trajs, None, static_rows, ["Open-loop scenarios only."])
    print(f"Wrote {out}")
    return out


def cmd_optimize(args: argparse.Namespace) -> Path:
    p, raw = load_params(Path(args.config), args.set)
    out = _outdir(args.run_id or _run_id("optimize"))
    trajs = _simulate_scenarios(p)
    opt = optimize(p, prefer=args.solver)
    all_trajs = trajs + [opt.trajectory]
    static_rows = diagnostics(p) + [solve_static(p)]
    extra = {
        "optimum_J": opt.J,
        "optimum_solver": opt.solver,
        "optimum_success": opt.success,
        "starts_tried": opt.starts_tried,
    }
    _write_common(out, raw, all_trajs, extra)
    plot_trajectories(all_trajs, p, out / "figures" / "trajectories.png")
    plot_controls(all_trajs, out / "figures" / "controls.png")
    plot_slack(all_trajs, out / "figures" / "slack.png")
    plot_sad_bars(all_trajs, out / "figures" / "sad_bars.png", p)
    notes = [
        f"Optimizer {opt.solver}: {opt.message}",
        "Path constraints are inequalities (states may sit below ceilings).",
    ]
    if p.T > p.fsb_year + 0.5:
        notes.append(
            f"Horizon extended to {p.T:.0f}; livestock must be at or under its food-system allocation from {p.fsb_year:.0f}."
        )
    write_report(out / "report.md", p, all_trajs, opt, static_rows, notes)
    print(f"Wrote {out}")
    return out


def cmd_sensitivity(args: argparse.Namespace) -> Path:
    p, raw = load_params(Path(args.config), args.set)
    out = _outdir(args.run_id or _run_id("sensitivity"))
    trajs = _simulate_scenarios(p)
    spec = Path(args.spec)
    rows, baseline = run_tornado(raw, p, spec)
    _write_common(out, raw, trajs, {"tornado": rows, "baseline_joint_J": baseline})
    plot_trajectories(trajs, p, out / "figures" / "trajectories.png")
    plot_sad_bars(trajs, out / "figures" / "sad_bars.png", p)
    plot_tornado(rows, baseline, out / "figures" / "tornado.png")
    static_rows = diagnostics(p)
    notes = [
        "Tornado uses the constant joint diagnostic, not a re-optimized policy.",
        "Bars for density-relief and delicacy parameters test the new quality/price channels.",
    ]
    write_report(out / "report.md", p, trajs, None, static_rows, notes)
    print(f"Wrote {out}")
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Constrained welfare optimization")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=str(DEFAULT_CONFIG), help="YAML parameter file")
    common.add_argument("--set", action="append", default=[], help="Override key=value (dotted keys OK)")
    common.add_argument("--run-id", default=None)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sc = sub.add_parser(
        "scenarios",
        parents=[common],
        help="Open-loop BAU / welfare-only / reduction-only / joint",
    )
    p_sc.set_defaults(func=cmd_scenarios)

    p_opt = sub.add_parser(
        "optimize",
        parents=[common],
        help="Minimize cumulative SADs with inequality path constraints",
    )
    p_opt.add_argument("--solver", choices=("gekko", "slsqp"), default="gekko")
    p_opt.set_defaults(func=cmd_optimize)

    p_sen = sub.add_parser(
        "sensitivity",
        parents=[common],
        help="One-at-a-time tornado around the joint diagnostic",
    )
    p_sen.add_argument("--spec", default=str(ROOT / "configs" / "sensitivity.yaml"))
    p_sen.set_defaults(func=cmd_sensitivity)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
