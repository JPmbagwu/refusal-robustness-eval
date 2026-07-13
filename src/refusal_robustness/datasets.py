"""Seed-prompt loaders.

Harmful requests are drawn ONLY from existing public benchmarks. This module defines the seed
representation and the loader interface; it does not vendor or re-host any harmful strings. A loader
is expected to read from a locally-provided copy of a public dataset that the user has obtained
under that dataset's own terms.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence


@dataclass(frozen=True)
class SeedPrompt:
    """A single harmful request from a public benchmark, used as an evaluation seed."""

    id: str
    text: str
    source: str  # e.g. "harmbench", "strongreject"
    category: str = "unspecified"
    tags: tuple[str, ...] = field(default_factory=tuple)


# Public benchmarks the harness is designed to consume. Values are references, not embedded data.
KNOWN_SOURCES = {
    "harmbench": "https://arxiv.org/abs/2402.04249",
    "strongreject": "https://arxiv.org/abs/2402.10260",
}


def load_seed_set(source: str, path: str) -> Sequence[SeedPrompt]:
    """Load seeds from a locally-provided copy of a public benchmark.

    Args:
        source: one of ``KNOWN_SOURCES``.
        path: local path to the user's own copy of that dataset.

    Returns:
        A sequence of ``SeedPrompt``.

    Not implemented in the public scaffold: each source needs a small adapter mapping its schema
    onto ``SeedPrompt``. Kept as a stub so the repo ships no harmful strings.
    """
    if source not in KNOWN_SOURCES:
        raise ValueError(f"unknown source {source!r}; expected one of {sorted(KNOWN_SOURCES)}")
    raise NotImplementedError(
        "Provide a local adapter for the chosen public benchmark. "
        "See docs/ETHICS.md: this scaffold does not vendor harmful prompts."
    )


def iter_categories(seeds: Iterable[SeedPrompt]) -> set[str]:
    """Distinct categories present in a seed set (useful for stratified sampling)."""
    return {s.category for s in seeds}
