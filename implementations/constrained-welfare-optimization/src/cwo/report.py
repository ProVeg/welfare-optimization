"""Short narrative a non-mathematician can read after a run."""

from __future__ import annotations

from pathlib import Path

from cwo.optimize import OptResult
from cwo.parameters import Params
from cwo.simulate import Trajectory, min_slacks
from cwo.static_nlp import StaticResult


def _slack_sentence(name: str, value: float) -> str:
    if value >= 0:
        return f"{name} stayed at or below its ceiling (tightest remaining room {value:.3g})."
    return f"{name} broke its ceiling (worst overshoot {-value:.3g})."


def write_report(
    path: Path,
    p: Params,
    trajs: list[Trajectory],
    opt: OptResult | None,
    static_rows: list[StaticResult],
    notes: list[str],
) -> None:
    lines = [
        "# Simulation report",
        "",
        "This run asks: over 2026–2050, how should effort be split between raising farmed-animal "
        "welfare standards and reducing demand, if the only goal is less total suffering "
        "(Suffering-Adjusted Days), while environmental pressure, meat prices, and animals-per-worker "
        "must stay at or below hard ceilings — they may fall below those ceilings.",
        "",
        "## What the numbers are",
        "",
        f"- Horizon: {p.t0:.0f}–{p.T:.0f}.",
        f"- Animals are a poultry-like standing population starting at {p.N0/1e9:.2f} billion.",
        f"- Suffering is an index (chicken-equivalent). Absolute billions are not a census of global SADs.",
        f"- Demand-reduction rate λ_D = {p.lambda_D} /year and welfare-campaign speed η_W = {p.eta_W} /year "
        "are **calibrated unknowns**, not measured campaign productivities. Do not read them as cost-effectiveness.",
        "",
        "## Open-loop strategies (ceilings monitored, not forced)",
        "",
    ]
    ranked = sorted(trajs, key=lambda tr: tr.J)
    for tr in trajs:
        sl = min_slacks(tr)
        lines.append(f"### {tr.label}")
        lines.append("")
        lines.append(f"- Cumulative suffering index: **{tr.J/1e9:.2f} billion**.")
        lines.append(f"- Final standing animals: {tr.N[-1]/1e9:.2f} billion; final quality: {tr.Q[-1]:.2f}.")
        lines.append(f"- {_slack_sentence('Environmental pressure', sl['E'])}")
        lines.append(f"- {_slack_sentence('Price', sl['P'])}")
        lines.append(f"- {_slack_sentence('Animals-per-worker', sl['labor'])}")
        lines.append("")

    lines += [
        f"**Lowest open-loop suffering:** {ranked[0].label}.",
        "",
        "## Optimized policy (ceilings enforced as inequalities)",
        "",
    ]
    if opt is None:
        lines.append("Optimizer was not run.")
    else:
        sl = min_slacks(opt.trajectory)
        lines.append(
            f"Solver: **{opt.solver}** ({'succeeded' if opt.success else 'did not fully succeed'}). "
            f"{opt.message}"
        )
        lines.append("")
        lines.append(f"- Cumulative suffering index: **{opt.trajectory.J/1e9:.2f} billion**.")
        lines.append(
            f"- Mean welfare-campaign intensity: {opt.trajectory.u_W.mean():.2f}; "
            f"mean demand-reduction intensity: {opt.trajectory.u_D.mean():.2f}."
        )
        lines.append(f"- {_slack_sentence('Environmental pressure', sl['E'])}")
        lines.append(f"- {_slack_sentence('Price', sl['P'])}")
        lines.append(f"- {_slack_sentence('Animals-per-worker', sl['labor'])}")
        q = opt.trajectory.Q
        stall = None
        for i in range(1, len(q)):
            if q[i] < q[i - 1] - 1e-3:
                stall = i
                break
        if stall is not None:
            year = opt.trajectory.t[stall]
            lines.append(
                f"- Quality starts falling around {year:.0f}. Check the slack figure to see which ceiling is tight then."
            )
        lines.append("")
        lines.append("Starts tried: " + ", ".join(opt.starts_tried))
        lines.append("")
        lines.append(
            "This is a **local** minimum of a non-convex problem. Another start could do better."
        )

    lines += ["", "## 2050 snapshot check (separate static NLP)", ""]
    lines.append("| Case | High-welfare share | Demand-reduction effort | 2050 suffering index | Feasible? |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in static_rows:
        feasible = "yes" if row.success else "no"
        lines.append(
            f"| {row.label} | {row.alpha:.2f} | {row.u_D:.2f} | {row.J/1e9:.2f} billion | {feasible} |"
        )
    lines += [
        "",
        "## What this does not show",
        "",
        "- It does not price suffering in dollars or tonnes of CO2.",
        "- It does not split species or Global North vs South (those are listed extensions).",
        "- Ranking can flip if λ_D, the price ceiling, or the high-welfare SAD ratio is moved; see the tornado plot.",
        "",
    ]
    if notes:
        lines += ["## Run notes", ""]
        lines.extend(f"- {n}" for n in notes)
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
