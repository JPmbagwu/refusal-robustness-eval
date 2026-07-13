"""Refusal Robustness under Adversarial Reformulation.

A research harness for measuring how stable LLM refusal behavior is under meaning-preserving
reformulation of harmful requests drawn from public safety benchmarks.

This is a scaffold: operator transformation bodies are intentionally left as stubs. See docs/ETHICS.md.
"""

__version__ = "0.0.1"

from .operators import Operator, OPERATOR_REGISTRY, Reformulation
from .datasets import SeedPrompt, load_seed_set
from .judge import ComplianceJudge, Verdict
from .metrics import degradation_by_operator, judge_human_agreement

__all__ = [
    "Operator",
    "OPERATOR_REGISTRY",
    "Reformulation",
    "SeedPrompt",
    "load_seed_set",
    "ComplianceJudge",
    "Verdict",
    "degradation_by_operator",
    "judge_human_agreement",
]
