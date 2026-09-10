# Day 19 — Agent concepts — cheat sheet

## The one-sentence version

An agent is an LLM in a loop that *chooses its own next action* — think → act (call a tool) →
observe (feed the result back) → repeat until done — which is powerful and is exactly why it
needs hard guards.

## Agent vs pipeline

| | Fixed pipeline (e.g. RAG) | Agent |
| --- | --- | --- |
| Who decides the steps | you, at build time | the model, at runtime |
| Number of steps | fixed | 1..N (until "done" or a guard fires) |
| Failure shapes | a bad answer | bad answer **+ infinite loop + runaway bill** |

## The loop

```
messages = [system, user]
for step in range(MAX_STEPS):
    action = llm(messages, tools)          # tool call OR final answer
    if action is final: return it
    result = run_tool(action.name, action.args)     # VALIDATE args inside the tool
    messages += [assistant: action, tool: result]   # the observation
```

Real LLMs return structured `tool_use` blocks — no parsing. You own the loop and its guards.

## A tool = schema + function

```python
{"name": "get_team", "description": "...",
 "input_schema": {"type": "object", "properties": {...}, "required": [...]}}
```
The schema is what the model sees; the function is what runs.

## The three failure modes + guards

| Failure | Guard |
| ------- | ----- |
| Infinite / repeated loop | `max_steps`; abort on repeated (tool, args); no-progress detection |
| Wrong / destructive action | validate args **inside every tool**; tool allowlist per agent; human approval for delete/send/pay/deploy |
| Runaway cost | tool-call budget + token budget; per-tool timeout |

Plus: structured logging of every (thought, action, observation) — you can't debug what you
didn't trace.

## Cost grows super-linearly

Each step is a fresh LLM call over the **whole growing transcript**, so per-step input tokens
rise ~linearly with step number → cumulative cost ~quadratic. Toy model: 20 steps ≈ 54× a
1-step answer. Default `max_steps` ≈ 6–12; raise only with a dollar/token budget guard.

## The real Anthropic tool-use loop

```python
resp = client.messages.create(model="claude-opus-5", max_tokens=1024,
                              system=SYSTEM, tools=tools, messages=messages)
messages.append({"role": "assistant", "content": resp.content})
if resp.stop_reason != "tool_use": ...            # final answer
results = [{"type": "tool_result", "tool_use_id": b.id, "content": json.dumps(run(b))}
          for b in resp.content if b.type == "tool_use"]
messages.append({"role": "user", "content": results})   # ALL results in ONE user message
```

`client.beta.messages.tool_runner` automates the loop while keeping per-turn hooks for
approval/logging.

## What this does not cover

- Frameworks that package this (LangChain / LlamaIndex) — Day 20.
- Building a working agent against a real model — Day 21.
- Multi-agent orchestration, planning/reflection patterns — beyond this week.
