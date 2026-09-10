# Day 26 — Build an eval harness — cheat sheet

## The one-sentence version

Harness = frozen test set (inputs + expectations + type tags) + one scoring fn per dimension +
a runner + a report (per-case, by-dimension, by-type) + a regression gate — kept outside the
system so it survives a swap.

## The test set

Tag each case with a **type**; each type stresses a different component:

| Type | Stresses | Expectation |
| ---- | -------- | ----------- |
| single_fact | basic retrieval + extraction | `fact` substring in answer |
| paraphrase | retrieval robustness | `fact` present despite reworded query |
| multi_part | synthesis / completeness | all required substrings present |
| out_of_scope | the relevance gate | answer == refusal |
| adversarial | injection resistance, ambiguity | real fact present, NOT the injected claim |

Cover ~10–20 to start; grow it from production.

## Scoring functions

`fn(test, output) -> float in [0,1] | None`. Return `None` when the dimension doesn't apply
(e.g. correctness on an out-of-scope case). Dimensions: correctness, source_precision,
faithfulness (Day 25 proxy), relevance, abstention, format_ok, (completeness).

## The report

- **by dimension** — the headline numbers + p50/p95 latency, mean ctx tokens.
- **by type** — where the aggregate hides a broken component (paraphrase correctness low →
  retrieval problem).
- **per case** — the first thing you read when a number looks wrong.
- **JSON report** — commit / diff in CI; list the failing case ids.

## The regression gate

```python
gate(baseline_rows, candidate_rows, must_not_regress=("faithfulness","abstention","correctness"))
# FAIL if any must-not-regress dimension drops > threshold (~0.02–0.05, calibrated so noise
# doesn't false-FAIL)
```

Plus **hard assertions** for safety properties (injection resistance, no PII) — a single
violation fails the whole gate; safety is never averaged away.

## Feeding failures back

Every production thumbs-down / judge-vs-human disagreement / new query pattern → append a test
case with the corrected expectation. The eval set is a living artifact.

## Rules

- Keep the harness outside the pipeline / framework.
- `must_not_regress`: faithfulness, abstention, correctness (cost/latency can trade; these
  can't silently regress).
- Fix or exclude flaky cases — a flaky case makes the *gate* flaky and hides real regressions.
- Freeze a test split you never tune against.

## What this does not cover

- Live production tracing / logging — Day 27.
- LLM-judge calibration detail — Day 25.
- Hill-climbing a prompt against the harness — see `claude-api` skill's hillclimb flow.
