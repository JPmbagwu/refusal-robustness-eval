"""Tests for the metrics module (the one fully-implemented component of the scaffold)."""
import math

from refusal_robustness.metrics import (
    compliance_rate,
    degradation_by_operator,
    rank_operators,
    judge_human_agreement,
    strength_response_curve,
)


def test_compliance_rate():
    assert compliance_rate([True, True, False, False]) == 0.5
    assert compliance_rate([False, False]) == 0.0
    assert compliance_rate([True]) == 1.0


def test_degradation_and_ranking():
    baseline = [False] * 10  # 0% compliance when phrased plainly
    by_op = {
        "persona": [True] * 6 + [False] * 4,   # +0.6
        "translate": [True] * 2 + [False] * 8,  # +0.2
    }
    deg = degradation_by_operator(baseline, by_op)
    assert math.isclose(deg["persona"], 0.6)
    assert math.isclose(deg["translate"], 0.2)
    assert [op for op, _ in rank_operators(deg)] == ["persona", "translate"]


def test_judge_human_agreement_perfect():
    labels = ["refusal", "compliance", "refusal"]
    out = judge_human_agreement(labels, labels)
    assert out["raw_agreement"] == 1.0
    assert out["cohens_kappa"] == 1.0
    assert out["n"] == 3.0


def test_judge_human_agreement_kappa_below_raw():
    # Judge always says "refusal"; humans mostly agree by base rate, so kappa < raw agreement.
    judge = ["refusal"] * 9 + ["refusal"]
    human = ["refusal"] * 9 + ["compliance"]
    out = judge_human_agreement(judge, human)
    assert math.isclose(out["raw_agreement"], 0.9)
    assert out["cohens_kappa"] < out["raw_agreement"]


def test_strength_curve_is_sorted():
    curve = strength_response_curve({0.5: [True], 0.0: [False], 1.0: [True, True]})
    assert [s for s, _ in curve] == [0.0, 0.5, 1.0]
