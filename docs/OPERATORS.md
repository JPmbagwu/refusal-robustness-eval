# Reformulation operator taxonomy

An **operator** takes a seed harmful request and returns a *meaning-preserving* reformulation at a
chosen strength `s in [0, 1]`. Strength `0` is (approximately) the plain request; higher strength
means a more aggressive transformation. The semantic intent must be preserved, so a faithful judge
would still recognize the underlying request; only the surface form changes.

Operators are the unit of evaluation. Because they are functions rather than fixed strings, the
benchmark is regenerable and resistant to contamination.

| Operator | Transformation | Strength axis |
| --- | --- | --- |
| `persona` | Wrap the request in a role/character frame | Persona depth, authority, distance from assistant identity |
| `fictionalize` | Embed the request in a story, script, or hypothetical | Framing layers, narrative distance |
| `decompose` | Split into a sequence of individually-innocuous sub-steps | Number of steps, per-step innocuousness |
| `translate` | Translate (optionally round-trip) into another language | Language distance, round-trip vs one-way |
| `register_shift` | Recast in technical jargon or an alternate register | Jargon density, obfuscation |
| `domain_transpose` | Move the request into an adjacent domain of discourse | Semantic distance of the target domain |

## Design rules

1. **Meaning preservation is required.** An operator that changes the underlying ask is a bug, not a
   stronger attack. Reformulations are validated (by judge + human spot-check) to still encode the
   same request before they count.
2. **Strength is monotone.** Higher `s` should be at least as aggressive as lower `s` for the same
   seed, so RQ3 (gradual vs threshold degradation) is measurable along a real axis.
3. **Operators compose.** Stacked operators (e.g. `persona ∘ decompose`) are a planned Month-3
   extension for testing whether robustness transfers across operator families.

## Interface

See [`src/refusal_robustness/operators.py`](../src/refusal_robustness/operators.py). Every operator
implements:

```python
def apply(self, seed: SeedPrompt, strength: float, rng: Random) -> Reformulation: ...
```

The concrete transformation bodies are intentionally left as stubs in this public scaffold; see
[ETHICS.md](ETHICS.md).
