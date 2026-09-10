# Day 04 — Context Windows

Why models "forget," hallucinate, and have hard token limits — built from scratch with
numbers you generate yourself.

## Learning objectives

By the end of the hour you should be able to:

1. Explain why a token limit is architectural (quadratic attention + KV-cache memory), not a
   setting you can raise.
2. Show that "the model forgot" almost always means the runtime truncated tokens before the
   model ran, and pick a truncation strategy on purpose.
3. Explain why next-token prediction fabricates confidently, and why temperature does not fix it.
4. Apply the right mitigation to the right failure: compaction, reordering, RAG, citations,
   staying within trained length.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The question: why did it forget the start of our chat? | 3 min |
| 1 | The naive view: context is unlimited — watch it break | 8 min |
| 2 | What a context window actually is: fixed slots, quadratic attention | 12 min |
| 3 | Build a fixed-window model: information falls off the left edge | 10 min |
| 4 | Positions: why going past the trained length degrades | 6 min |
| 5 | Hallucination: softmax always answers; "lost in the middle" | 14 min |
| 6 | Mitigations: truncation, compaction, RAG, ordering, citations | 7 min |
| 7 | Exercises and self-check quiz | — |

## Setup

Runs in the shared uv venv at the repo root (see [the root README](../../../README.md)):

```bash
source ../../../.venv/bin/activate
```

## Run it

```bash
python -m jupyterlab projects/week-02-context-and-prompting/day-04-context-windows/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. The notebook ships with outputs populated; use
Kernel > Restart Kernel and Run All Cells to run it yourself.

## Source material

- Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (2023) — https://arxiv.org/abs/2307.03172
- "Attention Is All You Need" (2017), §3.2 on attention cost — https://arxiv.org/abs/1706.03762
- Press et al., position interpolation / "Train Short, Test Long" (ALiBi) — https://arxiv.org/abs/2108.12409
- Anthropic, "Prompt engineering: long context tips" — https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips

## Files

- `lesson.ipynb` — the guided lesson. Everything happens here.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — what this lesson needs (numpy, matplotlib, tiktoken — all in the base env).
