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


def _env_sentence(tr: Trajectory, p: Params) -> str:
    sl = min_slacks(tr)
    e0_over = float(tr.E[0] - p.E_lim)
    eT_over = float(tr.E[-1] - p.E_lim)
    if e0_over > 0:
        end = (
            f"ended {eT_over:.2f} above it"
            if eT_over > 0
            else f"ended {-eT_over:.2f} below it"
        )
        return (
            f"Environmental pressure started {e0_over:.2f} above the livestock food-system allocation "
            f"and {end} (worst overshoot in the run {max(0.0, -sl['E']):.2f})."
        )
    return _slack_sentence("Environmental pressure", sl["E"])


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
        "This run asks: over "
        f"{p.t0:.0f}–{p.T:.0f}, "
        "how should effort be split between raising farmed-animal "
        "welfare standards and reducing demand, if the only goal is less total suffering "
        "(Suffering-Adjusted Days), while environmental pressure, meat prices, and animals-per-worker "
        "must stay at or below hard ceilings — they may fall below those ceilings. "
        "Livestock **starts already past** its share of the EAT-Lancet 2025 food-system ceiling "
        f"(about {p.E0/p.E_lim:.1f} times the allocation). That is the empirical overshoot, not a bug. "
        "Open-loop runs may stay over the environmental line. The optimizer must not raise pressure further "
        f"and should be at or under the allocation from {p.fsb_year:.0f} onward.",
        "",
        "## What the numbers are",
        "",
        f"- Horizon: {p.t0:.0f}–{p.T:.0f}"
        + (
            f". The livestock food-system allocation still binds from {p.fsb_year:.0f}."
            if p.T > p.fsb_year + 0.5
            else "."
        ),
        f"- Animals are a poultry-like standing population starting at {p.N0/1e9:.2f} billion.",
        f"- Biophysical pressure starts at {p.E0:.2f} times the livestock allocation of the EAT-Lancet 2025 "
        "food-system ceiling (composite of climate, land, N, and P vs Rockström / Steffen / Richardson boundaries). "
        "The dotted line at 1.0 is that allocation, not 'today's impact'.",
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
        lines.append(f"- {_env_sentence(tr, p)}")
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
        lines.append(f"- {_env_sentence(opt.trajectory, p)}")
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

    lines += ["", f"## {p.T:.0f} snapshot check (separate static NLP)", ""]
    lines.append(
        f"| Case | High-welfare share | Demand-reduction effort | {p.T:.0f} suffering index | Feasible? |"
    )
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
