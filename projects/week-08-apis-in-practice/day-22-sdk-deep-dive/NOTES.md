# Day 22 — The Anthropic SDK — cheat sheet

## The one-sentence version

Everything is `POST /v1/messages`: you send `model` + `max_tokens` + `system` + the full
`messages` history every call, and read back a `Message` whose `content` is a list of typed
blocks and whose `stop_reason` tells you what to do next.

## The request

```python
client.messages.create(
    model="claude-opus-5",        # exact ID, NO date suffix
    max_tokens=16000,             # REQUIRED; hard output ceiling
    system="...",                 # str, or [{"type":"text","text":...,"cache_control":{...}}]
    messages=[{"role":"user","content": "..."}],   # first must be user; string or block list
)
```

- Stateless — resend the whole history, and append the assistant's reply to it.
- **No assistant prefill** on current models (trailing assistant msg → 400).

## The `Message` response

| Field | Use |
| ----- | --- |
| `content` | list of blocks — iterate, check `.type` (`text` / `thinking` / `tool_use`) |
| `stop_reason` | `end_turn` / `max_tokens` (truncated!) / `tool_use` / `stop_sequence` / `refusal` |
| `usage` | `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` |
| `_request_id` | log it on failures (public) |
| `stop_details` | only set when `stop_reason == "refusal"` — guard before reading |

```python
text = "".join(b.text for b in resp.content if b.type == "text")
```

## Parameters

| Keep | Removed on current models (→ 400) | Use instead |
| ---- | -------------------------------- | ----------- |
| `model`, `max_tokens`, `system`, `stop_sequences` (≤4), `metadata` (no PII) | `temperature`, `top_p`, `top_k` | `output_config={"effort": "low".."max"}` |
| `thinking={"type":"adaptive"}` | `thinking.budget_tokens` | adaptive thinking + `effort` |
| `output_config={"format": {...}}` (Day 23) | assistant prefill | system prompt / structured outputs |

## `max_tokens` defaults

`~16000` non-streaming · `~64000` streaming · `~256` classification · `0` cache pre-warm only.
Hitting it = truncated partial + a retry. Don't lowball.

## Prompt caching

```python
system=[{"type":"text","text": BIG_STABLE_PREFIX, "cache_control": {"type":"ephemeral"}}]
messages=[{"role":"user","content": volatile_question}]   # volatile AFTER the breakpoint
```

Prefix match — any byte change before the breakpoint invalidates it. Order is
`tools → system → messages`. Verify with `usage.cache_read_input_tokens` (0 = a silent
invalidator: timestamp, UUID, unsorted JSON, varying tool list).

## Token counting

`client.messages.count_tokens(model=, system=, messages=, tools=)` → `.input_tokens`.
**Never `tiktoken`** — wrong tokenizer for Claude, and it changed at Opus 4.7.

## Errors — most-specific first

`NotFoundError` → `BadRequestError` → `AuthenticationError` → `RateLimitError` →
`APIStatusError` (check `.status_code >= 500`) → `APIConnectionError`. SDK auto-retries
408/409/429/≥500 + connection errors (`max_retries=2`). Never one broad `except`.

## What this does not cover

- Tool-use wire format + structured outputs — Day 23.
- Streaming events — Day 24.
- Batches / Files / Vision (see the API reference).
