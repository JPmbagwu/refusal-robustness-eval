"""Reformulation operators.

Each operator maps a seed harmful request to a *meaning-preserving* reformulation at a chosen
strength. Operators are the unit of evaluation, which is what makes the benchmark regenerable and
contamination-resistant.

The concrete transformation bodies are intentionally left unimplemented in this public scaffold
(see docs/ETHICS.md). What ships here is the taxonomy, the interface, and the strength contract, so
the design is legible without shipping a working attack toolkit.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import Random

from .datasets import SeedPrompt


@dataclass(frozen=True)
class Reformulation:
    """The output of applying an operator to a seed."""

    seed_id: str
    operator: str
    strength: float
    text: str
    #: True once a validator (judge + human spot-check) confirms meaning is preserved.
    meaning_preserved: bool | None = None


class Operator(ABC):
    """Base class for reformulation operators.

    Contract:
      * ``strength == 0`` returns (approximately) the plain request.
      * strength is monotone: higher strength is at least as aggressive as lower strength.
      * meaning is preserved: the underlying request must remain recoverable.
    """

    name: str

    @abstractmethod
    def apply(self, seed: SeedPrompt, strength: float, rng: Random) -> Reformulation:
        """Return a reformulation of ``seed`` at ``strength`` in [0, 1]."""

    def _check_strength(self, strength: float) -> None:
        if not 0.0 <= strength <= 1.0:
            raise ValueError(f"strength must be in [0, 1], got {strength}")


class _StubOperator(Operator):
    """Documented placeholder. Records intent without performing a transformation."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def apply(self, seed: SeedPrompt, strength: float, rng: Random) -> Reformulation:
        self._check_strength(strength)
        raise NotImplementedError(
            f"operator {self.name!r} is a scaffold stub ({self.description}); "
            "implement per docs/OPERATORS.md before running the matrix."
        )


#: The taxonomy from docs/OPERATORS.md, as named stubs.
OPERATOR_REGISTRY: dict[str, Operator] = {
    op.name: op
    for op in (
        _StubOperator("persona", "wrap the request in a role/character frame"),
        _StubOperator("fictionalize", "embed the request in a story, script, or hypothetical"),
        _StubOperator("decompose", "split into individually-innocuous sub-steps"),
        _StubOperator("translate", "translate (optionally round-trip) into another language"),
        _StubOperator("register_shift", "recast in technical jargon or an alternate register"),
        _StubOperator("domain_transpose", "move the request into an adjacent domain"),
    )
}


def get_operator(name: str) -> Operator:
    try:
        return OPERATOR_REGISTRY[name]
    except KeyError:
        raise ValueError(
            f"unknown operator {name!r}; known: {sorted(OPERATOR_REGISTRY)}"
        ) from None
