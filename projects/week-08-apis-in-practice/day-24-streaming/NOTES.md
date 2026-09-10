# Day 24 — Streaming — cheat sheet

## The one-sentence version

Stream to cut time-to-first-token and to avoid HTTP timeouts on big `max_tokens`; the response
arrives as typed SSE events you accumulate — `text_delta` into text, `input_json_delta`
fragments into a JSON string you parse once at `content_block_stop`.

## Event sequence (one text block)

```
message_start        -> Message shell: id, model, role, empty content, initial usage
content_block_start  -> {index, content_block: {type: text|tool_use|thinking}}
content_block_delta  -> text_delta {text} | input_json_delta {partial_json} | thinking_delta {thinking}
content_block_stop
  (start/delta*/stop repeats per block)
message_delta        -> {stop_reason}, cumulative usage.output_tokens
message_stop
```

## Accumulation rules

- **text**: append `delta.text` as it arrives.
- **tool args**: append `delta.partial_json` to a buffer keyed by block `index`; `json.loads`
  **once** at `content_block_stop` — a fragment is not valid JSON.
- **thinking**: append `delta.thinking`; keep as its own content block; don't show as the answer.

## SDK helpers

```python
with client.messages.stream(model="claude-opus-5", max_tokens=1024, messages=[...]) as stream:
    for text in stream.text_stream:        # the 90% case: filtered text chunks
        print(text, end="", flush=True)
    final = stream.get_final_message()     # complete reassembled Message
```

- `stream.text_stream` — text only, no event parsing.
- `for event in stream:` — raw events (needed for live tool-call UI / thinking display).
- `stream.get_final_message()` — always available after the stream is consumed.
- Large `max_tokens` (128k): streaming + `get_final_message()` is the **only** safe path.
- Don't hand-roll accumulation with `.on()` + `Promise` — the helper handles the edge cases.
- `eager_input_streaming: true` on a tool def emits `input_json_delta` sooner (not a beta).

## Tradeoffs

| | non-streaming | streaming |
| --- | --- | --- |
| TTFT | = total | ~0.5s |
| big max_tokens | may time out | required |
| retry on failure | clean | messy (may have shown partial text) |
| errors | one at the end | can fail mid-stream (or an `error` event) |

**Mid-stream failure:** catch it around the loop, show partial with "(interrupted)" or
discard, retry as a **fresh request** — you cannot resume a stream.

**Don't stream:** batch jobs; when you need the whole output before acting (JSON parse,
routing); tiny classification outputs; inside a tool loop wanting only the final message.

## Cancellation & billing

Streaming doesn't reduce token cost. Cancel early and you're still billed for the output
tokens the **server generated** before the connection closed, not just what you read.

## What this does not cover

- Async streaming (`AsyncAnthropic`).
- Server-side reconnect for very long agent sessions.
- Compaction blocks in the stream (long-conversation beta).
