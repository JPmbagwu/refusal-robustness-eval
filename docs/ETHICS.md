# Ethics, scope, and responsible disclosure

This is defensive safety-evaluation research. Its purpose is to **measure** how reliably models
refuse, so that safety teams can detect regressions in robustness (not just regressions in
memorization). The following constraints are load-bearing, not boilerplate.

## What this project does

- Draws harmful requests **only** from existing, already-public benchmarks
  ([HarmBench](https://arxiv.org/abs/2402.04249), [StrongREJECT](https://arxiv.org/abs/2402.10260)).
- Applies meaning-preserving *transformations* and measures whether refusal behavior holds.
- Grades responses for compliance and reports **aggregate** degradation metrics.

## What this project does not do

- **Does not author new harmful content.** No new harmful requests, targets, or payloads are written.
- **Does not ship working jailbreaks.** The operator transformation bodies in this public repository
  are stubs and typed interfaces. The repo is a research harness skeleton, not an attack toolkit.
- **Does not amplify harmful outputs.** Model completions are consumed by the judge and reduced to
  labels/metrics. They are never published verbatim or optimized for harmfulness.
- **Does not target a single deployed product for exploitation.** Findings are about classes of
  transformation across model families, framed as a robustness measurement.

## Responsible disclosure

If the work surfaces a reformulation class that reliably defeats a **deployed** model's safeguards,
we notify the relevant provider and allow a remediation window before any publication that could
increase real-world risk. Aggregate, cross-model findings that do not constitute a usable exploit
may be published normally.

## Released artifacts

The public benchmark consists of:

- the **operator definitions** (transformation types and strength axes),
- **references** to the public seed datasets (not re-hosted harmful strings), and
- the **evaluation harness** and metrics.

It does not include a corpus of novel harmful prompts.
