# Day 11 — Cost / latency / accuracy tradeoffs

Benchmarks tell you a model *can* do the task; this hour is the *should you pay for it*
question. A runnable tradeoff calculator: model lineup, Pareto frontier, total-cost-at-volume,
latency budget, and a cascade router that beats every single model on accuracy-per-dollar.

## Learning objectives

By the end of the hour you should be able to:

1. Compute cost per call and total cost at volume, and reason about prompt-cache ROI.
2. Build a Pareto frontier and identify dominated models to drop from consideration.
3. Design a latency budget around p95 (not p50) and explain how streaming changes which models
   pass.
4. Build and tune a cascade router (cheap-first, escalate on low confidence) and explain its
   preconditions and failure modes.
5. Pick the cheapest model that clears an accuracy bar, and know what to do with the savings.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The three axes and why you can't max all three | 3 min |
| 1 | A model lineup + the cost-per-call formula | 10 min |
| 2 | The Pareto frontier: which models are never the right choice | 12 min |
| 3 | Latency: p50 vs p95, streaming, and the budget | 10 min |
| 4 | Total cost at volume + caching | 10 min |
| 5 | The cascade router: cheap-first, escalate on doubt | 12 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs fully offline — a calculator over an illustrative model lineup (numbers in the shape of a
2024–25 lineup, not live pricing).

## Run it

```bash
python -m jupyterlab projects/week-04-model-evaluation/day-11-model-tradeoffs/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Chen et al., "FrugalGPT: How to Use LLMs While Reducing Cost and Improving Performance" — https://arxiv.org/abs/2305.05176
- Anthropic, "Prompt caching" — https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- "Reducing LLM latency" / streaming — https://platform.openai.com/docs/guides/latency-optimization
- LLM pricing trackers (for current numbers) — e.g. https://artificialanalysis.ai/

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib (base env).
