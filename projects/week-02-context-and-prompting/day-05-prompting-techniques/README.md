# Day 05 — Prompting Techniques

Zero-shot, few-shot, chain-of-thought, and system prompts — what each does to the model's
next-token distribution, and where each stops working. Built with tiny models you fully control.

## Learning objectives

By the end of the hour you should be able to:

1. Explain a prompt as *conditioning* on a single flattened token sequence, not literal
   instruction-following.
2. Choose between zero-shot, few-shot, and chain-of-thought for a task, and state the token /
   latency cost of each escalation.
3. Explain why chain-of-thought raises accuracy on hard reasoning (depth → length) and when it
   hurts.
4. Recognise the wall where a system prompt is not enough and you need RAG (knowledge) or
   fine-tuning (behaviour/skill/format at scale).

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Framing: a prompt is conditioning, not instruction | 3 min |
| 1 | The message structure: roles, and what "system" really is | 8 min |
| 2 | Zero-shot: the instruction-only baseline and its ceiling | 9 min |
| 3 | Few-shot: in-context learning as pattern completion | 13 min |
| 4 | Chain-of-thought: why a scratchpad changes what's computable | 14 min |
| 5 | System prompts: persistent conditioning, and the wall | 8 min |
| 6 | Decision table | 5 min |
| 7 | Exercises and self-check quiz | — |

## Setup

```bash
source ../../../.venv/bin/activate
```

## Run it

```bash
python -m jupyterlab projects/week-02-context-and-prompting/day-05-prompting-techniques/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Brown et al., "Language Models are Few-Shot Learners" (GPT-3) — https://arxiv.org/abs/2005.14165
- Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in LLMs" — https://arxiv.org/abs/2201.11903
- Kojima et al., "Large Language Models are Zero-Shot Reasoners" ("Let's think step by step") — https://arxiv.org/abs/2205.11916
- Wang et al., "Self-Consistency Improves Chain of Thought Reasoning" — https://arxiv.org/abs/2203.11171
- Anthropic prompt engineering guide — https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib, tiktoken (all in the base env).
