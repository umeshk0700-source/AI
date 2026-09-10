# Day 23 — Function calling & structured outputs — cheat sheet

## The one-sentence version

The model can't run code — it emits a `tool_use` block proposing a call; you execute the
function and send a `tool_result` block back; structured outputs (`output_config.format`)
instead constrain the model's *answer* to a JSON schema.

## Tool definition

```python
{"name": "get_weather",
 "description": "Get current weather for a city. Use for weather/temp questions.",  # picks tools BY THIS
 "input_schema": {"type": "object", "additionalProperties": false,
                  "properties": {"city": {"type": "string"}}, "required": ["city"]},
 "strict": true}   # top-level field (NOT on tool_choice); guarantees input validates exactly
```

The **description** is the highest-leverage field — write it like docs: purpose, trigger
phrases, boundaries.

## The round trip

| Turn | role | content |
| ---- | ---- | ------- |
| 1 | user | question (+ you pass `tools`) |
| 1 | assistant | `[TextBlock?, ToolUseBlock(id, name, input)]`, `stop_reason="tool_use"` — append whole turn |
| 2 | user | `[{"type":"tool_result","tool_use_id": id, "content": json.dumps(out)}]` (ALL results, ONE message) |
| 2 | assistant | final text, `stop_reason="end_turn"` |

Parallel calls: multiple `tool_use` blocks in one assistant turn → run all → all `tool_result`
blocks in one `user` message (splitting trains the model to stop parallelising). Failed tool →
`tool_result` with `"is_error": true`, don't drop it.

## `tool_choice`

`auto` (default) · `any` (some tool) · `{"type":"tool","name":...}` (this tool) · `none`.
**`any` and `tool` return 400 on Claude Fable 5.1 / Mythos 5.1** → use `auto` + an instruction,
`strict:true` for valid args, or structured outputs.

## Structured outputs

```python
resp = client.messages.parse(model="claude-opus-5", max_tokens=200, messages=[...],
    output_config={"format": {"type": "json_schema", "schema": Ticket.model_json_schema()}})
ticket = resp.parsed_output          # validated instance; no regex, no retry loop
```

Current field is `output_config.format` (`output_format` is deprecated). Incompatible with
document citations (400).

## `tool_runner`

`client.beta.messages.tool_runner(...)` drives the loop over `@beta_tool`-decorated functions,
with per-turn hooks for approval/logging/result-modification. Removes the plumbing, not the
guard responsibility (Day 19: max_steps, arg validation, allowlist, approval, budget).

## Schema token cost

Every request re-sends every tool schema. 10 tools × 80 tok × 20 turns = 16k input tokens for
schemas alone → prompt-cache the prefix (~10% on hits), or use tool search (`defer_loading` +
a search tool) so only relevant schemas load.

## What this does not cover

- Streaming tool-call JSON as it arrives — Day 24.
- Server-side tools (web search, code execution) — API reference.
- Programmatic tool calling (tools called from inside code execution) — API reference.
