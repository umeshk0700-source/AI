# Day 24 — Streaming responses

A non-streaming call is silent until the whole response is done — and can hit an HTTP timeout
on long outputs. Streaming delivers the response as server-sent events as it's generated.
This day: the event protocol, accumulating text and tool-call JSON from partial deltas, the
SDK helpers, and a working console streamer.

## Learning objectives

By the end of the hour you should be able to:

1. Give concrete reasons to stream (TTFT, timeouts, incremental UI, progress).
2. Name the SSE event types in order and what each carries.
3. Accumulate `text_delta`s into a console typewriter and rebuild the full `Message`.
4. Accumulate `input_json_delta` fragments and parse tool arguments once at
   `content_block_stop` (never mid-fragment).
5. Use `stream.text_stream` / `stream.get_final_message()`, and handle a mid-stream failure
   (retry as a fresh request — you can't resume).

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Why stream | 4 min |
| 1 | The event sequence | 12 min |
| 2 | Accumulate text → a console typewriter | 12 min |
| 3 | Accumulate tool-call JSON from `input_json_delta` | 12 min |
| 4 | The SDK helpers: `text_stream`, `get_final_message` | 10 min |
| 5 | Tradeoffs: retries, errors, when not to stream | 7 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs offline against a mock event generator that produces the real SSE event shapes. Real SDK
code (`with client.messages.stream(...) as stream`) shown alongside.

## Run it

```bash
python -m jupyterlab projects/week-08-apis-in-practice/day-24-streaming/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Anthropic, "Streaming Messages" — https://docs.anthropic.com/en/api/messages-streaming
- Anthropic Python SDK streaming helpers — https://github.com/anthropics/anthropic-sdk-python#streaming-responses
- Day 22 (the `Message` object), Day 23 (tool_use blocks).

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — stdlib only.
