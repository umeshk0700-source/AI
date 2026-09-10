# Day 25 — What makes a good eval

The theory that makes a scoring function trustworthy: the dimensions worth measuring, how to
evaluate with **no ground-truth labels**, how to build and **calibrate an LLM-as-judge**, and
why offline evals and production monitoring are different jobs.

## Learning objectives

By the end of the hour you should be able to:

1. Judge an eval as a measurement instrument: valid, reliable, sensitive, cheap.
2. Name the eval dimensions (accuracy, relevance, faithfulness, completeness, format,
   consistency, safety, latency, cost) and pick which matter for a task.
3. Choose between reference-based (EM, F1, ROUGE, embedding-sim) and reference-free metrics,
   knowing where each lies.
4. Build an LLM-judge from a rubric, name its biases (verbosity, position, self-preference,
   sycophancy, format halo), and calibrate it against human labels.
5. Evaluate with no ground truth (property checks, self-consistency, pairwise-vs-baseline).
6. Distinguish offline eval from production monitoring.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | An eval is a measurement instrument | 3 min |
| 1 | The dimensions | 10 min |
| 2 | Reference-based vs reference-free | 10 min |
| 3 | LLM-as-judge: build one, then break it | 16 min |
| 4 | Evaluating with no ground truth | 12 min |
| 5 | Offline eval vs production monitoring | 6 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (MiniLM) for the faithfulness/relevance proxies. The LLM-judge is
a deterministic mock with injectable biases so the failure modes are reproducible; the real
judge is `claude-opus-5` with the shown rubric prompt.

## Run it

```bash
python -m jupyterlab projects/week-09-evals-and-observability/day-25-good-evals/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" — https://arxiv.org/abs/2306.05685
- Es et al., "RAGAS: Automated Evaluation of RAG" (faithfulness, relevance) — https://arxiv.org/abs/2309.15217
- Anthropic, "Create strong empirical evaluations" — https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests
- "LLM judges" survey / position & verbosity bias — https://arxiv.org/abs/2411.15594

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, numpy, matplotlib.
