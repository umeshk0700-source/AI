# Day 12 — Model bake-off (hands-on)

Build the script that runs the same prompts against 2–3 real models (two sizes of SmolLM2 +
Qwen2.5-0.5B, on CPU) and produces the cost / latency / accuracy table you learned to read on
Day 11 — with measured numbers, not assumptions.

## Learning objectives

By the end of the hour you should be able to:

1. Build a model-agnostic harness: one `complete(system, user)` adapter interface for local and
   API models alike.
2. Score format adherence separately from correctness and explain why.
3. Produce the comparison table (accuracy, format_ok, p50/p95 latency, $/1k calls) and the
   accuracy-vs-cost / accuracy-vs-latency plots.
4. Run a sensitivity check (prompt wording, sampling) and refuse to pick a model on an unstable
   ranking.
5. Use the model-disagreement set to grow your eval.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The task, the gold set, the price table | 6 min |
| 1 | A uniform model adapter (local + how to add an API model) | 12 min |
| 2 | The scoring functions: format + correctness | 8 min |
| 3 | Run the bake-off | 12 min |
| 4 | The comparison table + Pareto plot | 12 min |
| 5 | Sensitivity: prompt wording and sampling | 7 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Needs `torch`, `transformers` (in the shared venv). First run downloads Qwen2.5-0.5B-Instruct
and two SmolLM2-Instruct models (~1 GB total) from the Hugging Face Hub. Runs on CPU; a full
pass is ~2–3 minutes.

## Run it

```bash
python -m jupyterlab projects/week-04-model-evaluation/day-12-model-bakeoff/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Day 06 (prompt workbench) and Day 11 (tradeoffs) — the methods this day combines.
- Hugging Face `transformers` generation docs — https://huggingface.co/docs/transformers/main/en/llm_tutorial
- Qwen2.5 technical report — https://arxiv.org/abs/2412.15115
- SmolLM2 — https://huggingface.co/blog/smollm

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — torch, transformers, numpy, matplotlib.
