"""Figures for non-mathematicians: titled axes, units, one-sentence captions."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from cwo.simulate import Trajectory

plt.rcParams.update(
    {
        "figure.dpi": 140,
        "savefig.dpi": 160,
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 8,
        "figure.facecolor": "white",
    }
)


def _caption(fig, text: str) -> None:
    fig.text(0.02, 0.01, text, ha="left", va="bottom", wrap=True, fontsize=8, color="#333333")
    fig.tight_layout(rect=(0, 0.06, 1, 1))


def plot_trajectories(trajs: list[Trajectory], p, path: Path) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(11, 10), sharex=True)
    series = [
        (axes[0, 0], "N", "Standing animals (billions)", lambda tr: tr.N / 1e9, None, None),
        (axes[0, 1], "Q", "Average quality of life (0–1)", lambda tr: tr.Q, p.Q_max, "Quality ceiling"),
        (axes[1, 0], "E", "Biophysical pressure (share of ceiling)", lambda tr: tr.E, p.E_lim, "Biophysical ceiling"),
        (axes[1, 1], "P", "Retail price (relative to today)", lambda tr: tr.P / p.P0, p.P_lim / p.P0, "Willingness-to-pay ceiling"),
        (axes[2, 0], "SAD", "Suffering per year (index)", lambda tr: tr.sad_rate / 1e9, None, None),
        (axes[2, 1], "J", "Cumulative suffering (index)", lambda tr: tr.J_cum / 1e9, None, None),
    ]
    for ax, _key, ylabel, getter, ceiling, clabel in series:
        for tr in trajs:
            ax.plot(tr.t, getter(tr), label=tr.label, color=tr.color, linestyle=tr.linestyle, linewidth=2)
        if ceiling is not None:
            ax.axhline(ceiling, color="black", linestyle=":", linewidth=1.2, label=clabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
    axes[2, 0].set_xlabel("Year")
    axes[2, 1].set_xlabel("Year")
    axes[0, 0].legend(loc="best")
    axes[0, 0].set_title("Animals alive")
    axes[0, 1].set_title("Quality of life")
    axes[1, 0].set_title("Environmental pressure")
    axes[1, 1].set_title("Meat price")
    axes[2, 0].set_title("New suffering each year")
    axes[2, 1].set_title("Suffering added up over time")
    _caption(
        fig,
        "Caption: Lines are strategies. Dotted lines are hard ceilings. Values above the "
        "biophysical line mean livestock is already past its EAT-Lancet food-system allocation. "
        "Open-loop diagnostics may stay over that line; the optimizer must not make the overshoot worse "
        f"and should be at or under the allocation from {p.fsb_year:.0f} onward. "
        "Quality can rise on its own only after the herd is well below today; remaining meat can get a small delicacy markup.",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def plot_controls(trajs: list[Trajectory], path: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    for tr in trajs:
        axes[0].plot(tr.t, tr.u_W, label=tr.label, color=tr.color, linestyle=tr.linestyle, linewidth=2)
        axes[1].plot(tr.t, tr.u_D, label=tr.label, color=tr.color, linestyle=tr.linestyle, linewidth=2)
    axes[0].set_ylabel("Welfare-campaign intensity (0–1)")
    axes[1].set_ylabel("Demand-reduction intensity (0–1)")
    axes[1].set_xlabel("Year")
    axes[0].set_title("Effort to raise welfare standards")
    axes[1].set_title("Effort to cut (or freeze) animal-product demand")
    axes[0].set_ylim(-0.05, 1.05)
    axes[1].set_ylim(-0.05, 1.05)
    axes[0].legend(loc="best")
    axes[0].grid(True, alpha=0.3)
    axes[1].grid(True, alpha=0.3)
    _caption(fig, "Caption: 0 means no extra campaign that year; 1 means full intensity.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def plot_slack(trajs: list[Trajectory], path: Path) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    specs = [
        (axes[0], "slack_E", "Room under the environmental ceiling"),
        (axes[1], "slack_P", "Room under the price / willingness-to-pay ceiling"),
        (axes[2], "slack_labor", "Room under the animals-per-worker ceiling"),
    ]
    for ax, attr, title in specs:
        for tr in trajs:
            ax.plot(tr.t, getattr(tr, attr), label=tr.label, color=tr.color, linestyle=tr.linestyle, linewidth=2)
        ax.axhline(0.0, color="black", linewidth=1)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
    axes[2].set_xlabel("Year")
    axes[0].legend(loc="best")
    _caption(
        fig,
        "Caption: Positive = still below the hard limit. Negative = already over that ceiling. "
        "The environmental panel starts negative because livestock is already past its food-system allocation.",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def plot_sad_bars(trajs: list[Trajectory], path: Path, p=None) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = [tr.label for tr in trajs]
    values = [tr.J / 1e9 for tr in trajs]
    colors = [tr.color for tr in trajs]
    ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.5)
    if p is None:
        period = "the whole period"
    else:
        period = f"{p.t0:.0f}–{p.T:.0f}"
    ax.set_ylabel(f"Cumulative suffering {period} (index, billions)")
    ax.set_title("Which strategy produces less suffering?")
    ax.grid(True, axis="y", alpha=0.3)
    ax.tick_params(axis="x", rotation=20)
    _caption(
        fig,
        "Caption: Lower bars are better. This is total suffering over the whole period, not a single year.",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def plot_tornado(rows: list[dict], baseline_j: float, path: Path) -> None:
    """rows: {label, low_j, high_j}."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = [r["label"] for r in rows]
    y = np.arange(len(labels))
    left = np.array([min(r["low_j"], r["high_j"]) for r in rows]) / 1e9
    width = np.abs(np.array([r["high_j"] - r["low_j"] for r in rows])) / 1e9
    ax.barh(y, width, left=left, color="#6baed6", edgecolor="black", linewidth=0.5)
    ax.axvline(baseline_j / 1e9, color="black", linestyle="--", label="Baseline joint strategy")
    ax.set_yticks(y, labels)
    ax.set_xlabel("Cumulative suffering (index, billions)")
    ax.set_title("Which assumptions move the answer the most?")
    ax.legend(loc="best")
    ax.grid(True, axis="x", alpha=0.3)
    _caption(
        fig,
        "Caption: Each bar is one parameter moved to a low and a high value. Longer bars mean more sensitivity.",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
