# Day 10 — Benchmarks and their limits

What MMLU, HumanEval, and friends actually measure — and the five ways a headline benchmark
number misleads you. We implement mini versions of both benchmark styles (multiple-choice and
code-execution) and break them on purpose.

## Learning objectives

By the end of the hour you should be able to:

1. Explain the two benchmark shapes (multiple-choice / exact-match vs execution / verifier).
2. Floor-normalise a multiple-choice score and explain why the raw number overstates skill.
3. Explain pass@k and why you can't compare it across different k.
4. Recognise contamination and name detection + mitigation strategies.
5. Explain why an aggregate score hides per-category weakness and why the same model can swing
   ~15 points on prompt format alone.
6. State the honest role of public benchmarks: shortlist, never final decision (that's Week 9).

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Why benchmarks exist, and the two styles | 4 min |
| 1 | Mini-MMLU: multiple choice + the chance floor | 11 min |
| 2 | Mini-HumanEval: pass@k with real execution | 13 min |
| 3 | Contamination: memorising the test set | 10 min |
| 4 | Aggregation hides weakness; prompt sensitivity | 12 min |
| 5 | Goodhart: when a benchmark becomes a target | 5 min |
| 6 | Exercises and self-check quiz | 5 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs fully offline — every "model" is a small Python function; the code benchmark executes real
Python.

## Run it

```bash
python -m jupyterlab projects/week-04-model-evaluation/day-10-benchmarks/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Hendrycks et al., "Measuring Massive Multitask Language Understanding" (MMLU) — https://arxiv.org/abs/2009.03300
- Chen et al., "Evaluating Large Language Models Trained on Code" (HumanEval, pass@k) — https://arxiv.org/abs/2107.03374
- "MMLU-Pro" — https://arxiv.org/abs/2406.01574
- Zhou et al., "Don't Make Your LLM an Evaluation Benchmark Cheater" (contamination) — https://arxiv.org/abs/2311.01964
- LiveBench — https://livebench.ai/

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib (base env).
