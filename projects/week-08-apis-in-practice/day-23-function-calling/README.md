# Day 23 — Function calling & structured outputs

Day 19 built the agent *loop*; this day is the exact **wire format** it rides on — how a tool
call travels from your schema, through the model, back to your function, and returns — plus
structured outputs that constrain the model's own JSON to a schema.

## Learning objectives

By the end of the hour you should be able to:

1. Explain that the model proposes calls (`tool_use` blocks) and never executes anything.
2. Write a tool definition (schema + description + `strict`) and know why the description is
   the highest-leverage field.
3. Walk one tool-use round trip block by block, including parallel calls and `tool_result`
   with `tool_use_id`.
4. Use `tool_choice` (and know it's rejected on Fable 5.1) and `strict: true`.
5. Use structured outputs (`output_config.format`, `messages.parse()`) for schema-valid answers.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | What "function calling" actually is | 4 min |
| 1 | The tool definition | 8 min |
| 2 | The request/response cycle, block by block | 14 min |
| 3 | Parallel tools, tool_choice, strict | 10 min |
| 4 | Structured outputs: schema-constrained JSON | 14 min |
| 5 | The tool_runner helper + guards recap | 7 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs offline against a mock model that emits real `tool_use` blocks and a from-scratch
JSON-schema validator (what the API enforces server-side). Real SDK code shown alongside.

## Run it

```bash
python -m jupyterlab projects/week-08-apis-in-practice/day-23-function-calling/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Anthropic, "Tool use (function calling)" — https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Anthropic, "Structured outputs" — https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
- Anthropic, "Tool runner" — https://docs.anthropic.com/en/api/tool-runner
- Day 19 (the loop + guards).

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — stdlib only.
