# Refusal Robustness under Adversarial Reformulation

Measuring how stable LLM safety behavior is when a harmful request is **reformulated** (persona
framing, fictionalization, decomposition, translation, jargon, domain shifting) rather than restated.

> **Status:** research scaffold. This repository accompanies a proposed
> [SPAR](https://sparai.org) Fall 2026 project. The harness is a documented skeleton with typed
> interfaces and stubs; it does **not** ship working jailbreak generators. See
> [`docs/ETHICS.md`](docs/ETHICS.md).

## The question

Safety training generalizes imperfectly. A model that refuses a harmful request stated plainly may
comply when the **same request** is reformulated in a meaning-preserving way. Static safety
benchmarks test fixed phrasings, so they measure **refusal accuracy** (does it refuse this exact
string?) and drift upward as those strings leak into training corpora. They do not measure
**refusal robustness** (does it still refuse when the request is transformed?).

This project treats *reformulation operators*, not fixed strings, as the unit of evaluation, so the
benchmark can be regenerated and resists contamination.

## Research questions

- **RQ1** — Which classes of meaning-preserving reformulation most degrade refusal behavior, and
  does the ranking hold across model families and sizes?
- **RQ2** — Are failures predictable from measurable properties of the transformation (distance from
  the training distribution, persona depth, decomposition granularity)?
- **RQ3** — Do safety behaviors degrade gradually as reformulation strength increases, or fail
  discretely at a threshold?
- **RQ4** — Can a small set of transformation primitives generate a contamination-resistant
  benchmark in which fresh test items are produced programmatically rather than fixed?

## How it works

```
seed prompts            operators                 models              judge
(public benchmarks) --> (reformulation ops) --> (target LLMs) --> (compliance grading) --> metrics
 HarmBench, StrongREJECT   persona, decomp, ...    via public APIs   LLM judge + human spot-checks   per-operator degradation
```

1. **Seed set** — harmful requests are drawn **only** from existing public benchmarks
   ([HarmBench](https://arxiv.org/abs/2402.04249),
   [StrongREJECT](https://arxiv.org/abs/2402.10260)). No new harmful content is authored.
2. **Operators** — each operator applies a meaning-preserving transformation at a chosen strength.
   See [`docs/OPERATORS.md`](docs/OPERATORS.md) for the taxonomy.
3. **Targets** — reformulated prompts are sent to several model families through public APIs.
4. **Judge** — an LLM judge grades each response for compliance, validated against human spot-checks
   before any headline number is reported.
5. **Metrics** — per-operator, per-model degradation relative to the plain-phrasing baseline.

## Layout

| Path | What it is |
| --- | --- |
| [`src/refusal_robustness/operators.py`](src/refusal_robustness/operators.py) | Operator taxonomy and interface (stubs) |
| [`src/refusal_robustness/datasets.py`](src/refusal_robustness/datasets.py) | Loaders for public seed benchmarks |
| [`src/refusal_robustness/judge.py`](src/refusal_robustness/judge.py) | Compliance-judge interface + reliability hooks |
| [`src/refusal_robustness/harness.py`](src/refusal_robustness/harness.py) | Runs the operator-by-model matrix |
| [`src/refusal_robustness/metrics.py`](src/refusal_robustness/metrics.py) | Degradation and agreement metrics |
| [`docs/OPERATORS.md`](docs/OPERATORS.md) | Reformulation operator taxonomy |
| [`docs/ETHICS.md`](docs/ETHICS.md) | Scope, safety norms, responsible disclosure |

## Plan (3 months)

- **Month 1 — Foundations.** Operator taxonomy, seed curation from public benchmarks, harness build,
  judge with human-reliability spot-checks.
- **Month 2 — Execution.** Full transformation-by-model matrix via public APIs; harden the judge
  against partial compliance, refusal-with-leakage, and over-refusal; measure judge–human agreement.
- **Month 3 — Analysis & release.** Degradation by operator, model, and strength; predictability
  (RQ2) and threshold behavior (RQ3); open-source release and write-up.

## Ethics

Uses public harmful-prompt datasets rather than authoring new harmful content. Model outputs are
graded for compliance and never amplified, published verbatim, or optimized for harmfulness. The
released benchmark consists of transformation operators and references to public datasets, not novel
harmful strings. Responsible disclosure applies to any deployed-model finding. Full policy in
[`docs/ETHICS.md`](docs/ETHICS.md).

## Related work

- Wei, Haghtalab, Steinhardt. *Jailbroken: How Does LLM Safety Training Fail?* (2023) — https://arxiv.org/abs/2307.02483
- Mazeika et al. *HarmBench* (2024) — https://arxiv.org/abs/2402.04249
- Souly et al. *StrongREJECT* (2024) — https://arxiv.org/abs/2402.10260

## License

MIT — see [LICENSE](LICENSE).
