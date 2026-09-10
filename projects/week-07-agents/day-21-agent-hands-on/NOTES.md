# Day 21 — Build a simple agent — cheat sheet

## The one-sentence version

An agentic RAG system has one tool (`search_kb`) and a loop that lets the model decide whether
to retrieve, how many times, and with what query — 0 searches for "hi", 1 for a fact, 2+ for a
multi-part question, and an abstention when scores are low.

## The tool

```python
SEARCH_TOOL = {
 "name": "search_kb",
 "description": "Search the KB. Returns passages with a relevance score "
                "(>0.4 good, <0.3 = nothing relevant).",   # tell the model how to read the score
 "input_schema": {"type": "object",
                  "properties": {"query": {"type": "string"}}, "required": ["query"]},
}
```

## The Anthropic tool-use loop

```python
messages = [{"role": "user", "content": question}]
for _ in range(MAX_STEPS):
    resp = client.messages.create(model="claude-opus-5", max_tokens=600,
                                  system=SYSTEM, tools=[SEARCH_TOOL], messages=messages)
    messages.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason != "tool_use":
        return "".join(b.text for b in resp.content if b.type == "text")   # done
    results = [{"type": "tool_result", "tool_use_id": b.id, "content": json.dumps(search_kb(**b.input))}
               for b in resp.content if b.type == "tool_use"]
    messages.append({"role": "user", "content": results})                  # ALL results, one message
```

## The system prompt does the routing

Tell the model: answer greetings directly (no search); search once per distinct sub-question;
answer only from returned passages + cite topics; abstain when the best score < 0.3.

## Guards

- `max_steps` (bounds iterations / cost)
- repeated-query detection (`counts[query] > max_same` → abort)
- total search budget (`max_searches`)
- (real deployments: per-tool timeout, tool allowlist, approval for destructive tools)

## Agentic vs always-retrieve

| | always-retrieve (Day 18) | agentic |
| --- | --- | --- |
| greeting / OOS | wasted search every time | 0 searches |
| single fact | 1 | 1 |
| multi-part | 1 (may miss 2nd half on a big KB) | 2+ |
| cost | 1 model call | 1–3 model calls (super-linear, Day 19) |

Worth it when queries vary in what they need; overhead when every query is "retrieve once".

## Cost math (haiku, 900 in + 150 out, +400 in per prior tool result)

1-hop ≈ $0.0017/query, 3-hop ≈ $0.0062/query (~3.7×). At 100k/month that's a ~$450 delta.

## What this does not cover

- Multi-agent orchestration, planner/reflection loops.
- The Anthropic SDK's `tool_runner` helper (automates the loop with hooks) — Week 8.
- Streaming tool calls, structured outputs — Week 8.
