"""Figure helpers for the analysis outputs.

Pure functions from metrics -> matplotlib Figure, so they can be unit-tested and reused in
notebooks. matplotlib is an optional dependency (install the ``plot`` extra); it is imported lazily
so the core package stays dependency-free.

Nothing here fabricates results. Callers pass in real (or explicitly-synthetic) metrics; these
functions only render what they are given.
"""
from __future__ import annotations

from typing import Mapping, Sequence


def _mpl():
    try:
        import matplotlib.pyplot as plt  # noqa: WPS433 (lazy import is intentional)
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise ModuleNotFoundError(
            "plotting needs matplotlib; install with: pip install 'refusal-robustness-eval[plot]'"
        ) from exc
    return plt


def plot_operator_degradation(degradation: Mapping[str, float], title: str = "Refusal degradation by operator"):
    """Horizontal bar chart of compliance-rate increase per operator (RQ1).

    Higher bar = the operator made the model comply more often = worse refusal robustness.
    """
    plt = _mpl()
    items = sorted(degradation.items(), key=lambda kv: kv[1])
    names = [k for k, _ in items]
    vals = [v * 100 for _, v in items]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(names, vals, color="#c0392b")
    ax.set_xlabel("Compliance increase vs plain phrasing (percentage points)")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)
    for y, v in enumerate(vals):
        ax.text(v + 0.5, y, f"+{v:.0f}", va="center", fontsize=9)
    fig.tight_layout()
    return fig


def plot_strength_curves(
    curves: Mapping[str, Sequence[tuple[float, float]]],
    title: str = "Compliance vs reformulation strength",
):
    """One line per operator: compliance rate as a function of strength (RQ3).

    Distinguishes gradual degradation from a discrete threshold.
    """
    plt = _mpl()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for name, curve in curves.items():
        xs = [s for s, _ in curve]
        ys = [r * 100 for _, r in curve]
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_xlabel("Operator strength")
    ax.set_ylabel("Compliance rate (%)")
    ax.set_ylim(-2, 102)
    ax.set_title(title)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    return fig


def plot_operator_model_heatmap(
    matrix: Mapping[str, Mapping[str, float]],
    title: str = "Compliance rate by operator and model",
):
    """Heatmap of compliance rate (operators x models) for RQ1 cross-family comparison.

    ``matrix[operator][model] = compliance_rate in [0, 1]``.
    """
    plt = _mpl()
    operators = list(matrix.keys())
    models = list(next(iter(matrix.values())).keys())
    data = [[matrix[op][m] * 100 for m in models] for op in operators]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    im = ax.imshow(data, cmap="Reds", vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(len(models)), models, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(operators)), operators, fontsize=9)
    for i in range(len(operators)):
        for j in range(len(models)):
            ax.text(j, i, f"{data[i][j]:.0f}", ha="center", va="center", fontsize=8,
                    color="white" if data[i][j] > 55 else "black")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, label="Compliance rate (%)")
    fig.tight_layout()
    return fig
