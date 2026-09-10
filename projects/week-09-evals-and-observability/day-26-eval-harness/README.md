# Day 26 — Build an eval harness (hands-on)

Turn Day 25's dimensions into a runnable harness for a RAG pipeline: a curated 14-case test
set (5 types), per-dimension scoring functions, a runner + report, a **regression gate**
comparing two configs, and the loop that feeds production failures back in.

## Learning objectives

By the end of the hour you should be able to:

1. Assemble the five parts of a harness: test set, scoring functions, runner, report, gate.
2. Design a test set with type tags (single-fact, paraphrase, multi-part, out-of-scope,
   adversarial) and know what each type stresses.
3. Write one scoring function per dimension, returning `None` for cases where it doesn't apply.
4. Produce a per-case table + by-dimension + by-type report and a JSON report for CI.
5. Build a regression gate that blocks a merge on faithfulness / abstention / correctness
   regressions, and add hard assertions for safety properties.
6. Turn a production failure into a permanent test case.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | What an eval harness is made of | 3 min |
| 1 | The system under test (a small RAG pipeline) | 8 min |
| 2 | The test set: 14 cases, 5 types | 12 min |
| 3 | Scoring functions, one per dimension | 14 min |
| 4 | The runner + the report | 12 min |
| 5 | Regression gate + feeding failures back | 8 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (MiniLM). The generator is a deterministic extractive mock so the
harness runs instantly and reproducibly; swapping in the real `generate()` (Day 18/21) is a
one-liner.

## Run it

```bash
python -m jupyterlab projects/week-09-evals-and-observability/day-26-eval-harness/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Anthropic, "Create strong empirical evaluations" — https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests
- Day 25 (eval dimensions, LLM-judge, no-ground-truth methods).
- promptfoo / Braintrust / OpenAI Evals (harness patterns) — https://www.promptfoo.dev/

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, numpy.
