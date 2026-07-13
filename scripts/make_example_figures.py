"""Render illustrative example figures into docs/figures/.

IMPORTANT: the numbers here are SYNTHETIC and hand-specified to show what each figure looks like.
They are not measurements of any model. Real figures will be produced by the harness in Month 2-3.
The synthetic values are seeded and deterministic so the committed PNGs are reproducible.

Run:  python scripts/make_example_figures.py
"""
from __future__ import annotations

import os
from random import Random

import matplotlib
matplotlib.use("Agg")  # headless

from refusal_robustness.plots import (
    plot_operator_degradation,
    plot_strength_curves,
    plot_operator_model_heatmap,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "figures")
os.makedirs(OUT, exist_ok=True)

OPERATORS = ["persona", "fictionalize", "decompose", "translate", "register_shift", "domain_transpose"]
MODELS = ["model-A", "model-B", "model-C", "model-D"]

# Illustrative relative ordering only (synthetic).
DEGRADATION = {
    "decompose": 0.41,
    "persona": 0.34,
    "fictionalize": 0.27,
    "domain_transpose": 0.19,
    "register_shift": 0.12,
    "translate": 0.08,
}


def _curve(kind: str, rng: Random) -> list[tuple[float, float]]:
    xs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    out = []
    for x in xs:
        if kind == "threshold":
            base = 0.03 if x < 0.6 else 0.55 + 0.35 * (x - 0.6) / 0.4  # sharp jump near 0.6
        else:  # gradual
            base = 0.03 + 0.6 * x
        noise = (rng.random() - 0.5) * 0.04
        out.append((x, max(0.0, min(1.0, base + noise))))
    return out


def main() -> None:
    rng = Random(7)  # deterministic synthetic data

    fig1 = plot_operator_degradation(
        DEGRADATION, title="Refusal degradation by operator (illustrative, synthetic)"
    )
    fig1.savefig(os.path.join(OUT, "degradation_by_operator.png"), dpi=140)

    curves = {
        "decompose (threshold-like)": _curve("threshold", rng),
        "persona (gradual)": _curve("gradual", rng),
        "translate (gradual, weak)": [(x, y * 0.35) for x, y in _curve("gradual", rng)],
    }
    fig2 = plot_strength_curves(
        curves, title="Compliance vs reformulation strength (illustrative, synthetic)"
    )
    fig2.savefig(os.path.join(OUT, "strength_curves.png"), dpi=140)

    heat = {}
    for i, op in enumerate(OPERATORS):
        row = {}
        for j, m in enumerate(MODELS):
            base = DEGRADATION[op]
            row[m] = max(0.0, min(1.0, base + (j - 1.5) * 0.05 + (rng.random() - 0.5) * 0.04))
        heat[op] = row
    fig3 = plot_operator_model_heatmap(
        heat, title="Compliance rate by operator x model (illustrative, synthetic)"
    )
    fig3.savefig(os.path.join(OUT, "operator_model_heatmap.png"), dpi=140)

    print("wrote 3 figures to", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
