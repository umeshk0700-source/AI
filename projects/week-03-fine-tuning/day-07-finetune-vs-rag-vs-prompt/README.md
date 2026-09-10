# Day 07 — Fine-tune vs RAG vs Prompt

Where does a missing capability go — into the prompt, into retrieved context, or into the
weights? One task, three attacks, compared on accuracy, cost/call, latency, freshness, and
build effort.

## Learning objectives

By the end of the hour you should be able to:

1. State the mental model: prompt = working memory, RAG = open book on the desk, fine-tune =
   what you learned in school.
2. Route a real requirement to the right mechanism using explicit decision rules.
3. Explain why RAG accuracy is capped by retrieval accuracy, and why fine-tuning on
   fast-changing facts is a predictable failure (staleness).
4. Reason about the fixed-vs-marginal cost crossover that decides when fine-tuning pays off.
5. Compose all three the way production systems do.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The three places knowledge/behaviour can live | 4 min |
| 1 | The task + a controllable model | 8 min |
| 2 | Attack 1 — prompt engineering | 9 min |
| 3 | Attack 2 — RAG (retrieve into context) | 13 min |
| 4 | Attack 3 — fine-tuning (move it into weights) | 13 min |
| 5 | The five-axis comparison + decision rules | 8 min |
| 6 | Exercises and self-check quiz | 5 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs fully offline — every "model" is a small controllable Python function.

## Run it

```bash
python -m jupyterlab projects/week-03-fine-tuning/day-07-finetune-vs-rag-vs-prompt/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- OpenAI, "When to fine-tune" / fine-tuning guide — https://platform.openai.com/docs/guides/fine-tuning
- Anthropic, "Retrieval augmented generation" — https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation
- "RAG vs Fine-tuning: Pipelines, Tradeoffs" (Balaguer et al., 2024) — https://arxiv.org/abs/2401.08406

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib (base env).
