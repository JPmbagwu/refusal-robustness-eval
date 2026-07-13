"""Evaluation harness: runs the operator-by-model matrix.

Orchestrates seeds x operators x strengths x models -> responses -> judge -> records. Model and
judge backends are injected, so the harness itself contains no API keys or provider code. The
per-cell execution is a stub pending the operator and judge implementations.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from random import Random
from typing import Callable, Iterable, Sequence

from .datasets import SeedPrompt
from .operators import Operator
from .judge import ComplianceJudge, Verdict

#: A model backend: takes a prompt, returns the model's completion.
ModelFn = Callable[[str], str]


@dataclass(frozen=True)
class MatrixCell:
    seed_id: str
    operator: str
    strength: float
    model: str


@dataclass(frozen=True)
class Record:
    cell: MatrixCell
    verdict: Verdict


@dataclass
class MatrixSpec:
    seeds: Sequence[SeedPrompt]
    operators: Sequence[Operator]
    strengths: Sequence[float]
    models: dict[str, ModelFn]  # name -> backend
    seed_rng: int = 0

    def cells(self) -> Iterable[MatrixCell]:
        for s in self.seeds:
            for op in self.operators:
                for strength in self.strengths:
                    for model_name in self.models:
                        yield MatrixCell(s.id, op.name, strength, model_name)

    def size(self) -> int:
        return len(self.seeds) * len(self.operators) * len(self.strengths) * len(self.models)


def run_matrix(spec: MatrixSpec, judge: ComplianceJudge) -> list[Record]:
    """Execute the full matrix.

    Stub: iterate cells, apply the operator, query the model backend, grade with the judge, and emit
    a Record per cell. Left unimplemented until operators/judge are wired (see docs/ETHICS.md), but
    the shape is fixed so downstream metrics can be developed against synthetic Records.
    """
    raise NotImplementedError(
        "wire operator.apply -> model backend -> judge.grade per cell; "
        f"planned matrix size = {spec.size()} cells"
    )


def records_to_rows(records: Iterable[Record]) -> list[dict]:
    """Flatten Records to plain dicts for CSV/DataFrame export."""
    rows = []
    for r in records:
        row = asdict(r.cell)
        row["label"] = r.verdict.label.value
        row["confidence"] = r.verdict.confidence
        rows.append(row)
    return rows
