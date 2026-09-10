# Day 22 — The Anthropic SDK, in depth

Open up the "API" helper every previous day hid: the exact request shape, the `Message`
response object, the parameters that matter (and the ones that were removed), prompt caching,
token counting, stateless multi-turn, and error handling.

## Learning objectives

By the end of the hour you should be able to:

1. Build a `messages.create()` request by hand: model, `max_tokens`, `system`, `messages` with
   roles and content blocks.
2. Read a `Message` response — iterate `content` blocks by `.type`, branch on `stop_reason`,
   inspect `usage`.
3. Explain why the API is stateless and what that forces you to do every turn.
4. Name the parameters removed on current models (`temperature`, `top_p`, `top_k`,
   `budget_tokens`, prefill) and what replaced them (`effort`, adaptive thinking, structured
   outputs).
5. Cache a stable prefix correctly, count tokens with the API (not `tiktoken`), and write a
   most-specific-first exception chain.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | One endpoint: `POST /v1/messages` | 3 min |
| 1 | The request: model, max_tokens, system, messages | 12 min |
| 2 | The response: content blocks, stop_reason, usage | 12 min |
| 3 | Multi-turn: the API is stateless | 8 min |
| 4 | Parameters that matter (and ones that were removed) | 10 min |
| 5 | Prompt caching + token counting + errors | 12 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs fully offline against a **faithful mock client** that reproduces the `Message` object
shape, `usage` accounting, cache reads, and `stop_reason` behaviour. Real SDK code is shown
alongside every mock and is a drop-in.

## Run it

```bash
python -m jupyterlab projects/week-08-apis-in-practice/day-22-sdk-deep-dive/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Anthropic Messages API reference — https://docs.anthropic.com/en/api/messages
- Anthropic, "Prompt caching" — https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Anthropic, "Token counting" — https://docs.anthropic.com/en/docs/build-with-claude/token-counting
- Anthropic Python SDK — https://github.com/anthropics/anthropic-sdk-python

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — stdlib only.
