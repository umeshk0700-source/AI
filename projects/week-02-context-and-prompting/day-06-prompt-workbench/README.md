# Day 06 — Prompt Workbench (hands-on)

Pick one real task, write 10 prompts across zero-shot / few-shot / chain-of-thought / system
framing, and run them all through one harness that measures accuracy, format validity, token
cost, and latency.

Task used: triage a support ticket → strict JSON `{category, priority, needs_human}`.

## Learning objectives

By the end of the hour you should be able to:

1. Build a reusable prompt bake-off harness: gold set + scoring function + runner.
2. Score format validity separately from field accuracy, and know why that split matters.
3. Read an accuracy-vs-cost frontier and pick the cheapest prompt that clears your quality bar.
4. Turn the harness into a regression test you re-run on every prompt / model / version change.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The task, the gold set, the rules of the bake-off | 5 min |
| 1 | The model backend: a local mock now, real API later | 8 min |
| 2 | The scoring function: partial credit + format validity | 8 min |
| 3 | Write the 10 prompts | 15 min |
| 4 | Run the bake-off | 10 min |
| 5 | Read the results: accuracy vs cost frontier | 9 min |
| 6 | Exercises and self-check quiz | 5 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

The notebook runs fully offline against a local mock model. To use a real model, uncomment the
"REAL BACKEND" block in Segment 1 and add `anthropic` to the root `requirements.txt`
(`python -m uv pip install --python .venv/bin/python -r requirements.txt`), then set
`ANTHROPIC_API_KEY`. Every downstream cell is unchanged.

## Run it

```bash
python -m jupyterlab projects/week-02-context-and-prompting/day-06-prompt-workbench/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Anthropic, "Define your success criteria" / "Create strong empirical evaluations" —
  https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests
- OpenAI cookbook, "Evaluating model outputs" — https://cookbook.openai.com/
- Day 05 (prompting techniques) — the concepts this day exercises.

## Files

- `lesson.ipynb` — the guided workbench.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib, tiktoken (base env); `anthropic` optional.
