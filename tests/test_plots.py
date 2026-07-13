"""Smoke tests for the plotting helpers.

Skipped automatically if matplotlib is not installed (it is an optional extra).
"""
import pytest

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")

from refusal_robustness.plots import (
    plot_operator_degradation,
    plot_strength_curves,
    plot_operator_model_heatmap,
)


def test_degradation_figure_has_axes():
    fig = plot_operator_degradation({"persona": 0.3, "translate": 0.1})
    assert len(fig.axes) == 1


def test_strength_curves_figure_has_lines():
    curves = {"persona": [(0.0, 0.0), (0.5, 0.3), (1.0, 0.6)]}
    fig = plot_strength_curves(curves)
    assert len(fig.axes[0].lines) == 1


def test_heatmap_figure_renders():
    matrix = {"persona": {"m1": 0.2, "m2": 0.4}, "translate": {"m1": 0.05, "m2": 0.1}}
    fig = plot_operator_model_heatmap(matrix)
    # one axis for the heatmap + one for the colorbar
    assert len(fig.axes) == 2
