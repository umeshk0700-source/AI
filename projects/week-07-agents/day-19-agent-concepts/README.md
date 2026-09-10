# Day 19 — Agent concepts: tools, the loop, and guards

An agent is an LLM in a loop: it picks an action (usually a tool call), you run it, feed the
result back, repeat until it produces a final answer. Built from scratch, run on a multi-step
task, then broken to motivate every guard a real agent needs.

## Learning objectives

By the end of the hour you should be able to:

1. State precisely what makes something an agent (model-driven control flow) vs a fixed
   pipeline.
2. Define a tool as a JSON schema + a function, and build a tool registry.
3. Implement the think → act → observe → repeat loop, including a variable number of steps.
4. Recognise the three failure modes — loops, wrong/destructive actions, runaway cost — and
   write a guard for each.
5. Map the from-scratch loop onto the real Anthropic tool-use API.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Prompt-response vs agent | 4 min |
| 1 | Tools: a schema and a registry | 8 min |
| 2 | The loop: think → act → observe → repeat | 14 min |
| 3 | A real multi-step task (the ReAct shape) | 10 min |
| 4 | Failure modes: loops, wrong actions, runaway cost | 12 min |
| 5 | Guards, and the real Anthropic tool-use API | 9 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs fully offline — the "LLM" is a deterministic scripted planner so the loop mechanics are
visible without a model. Runs in seconds. The real Anthropic tool-use loop is shown as
reference code.

## Run it

```bash
python -m jupyterlab projects/week-07-agents/day-19-agent-concepts/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" — https://arxiv.org/abs/2210.03629
- Anthropic, "Building effective agents" — https://www.anthropic.com/research/building-effective-agents
- Anthropic tool use docs — https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Anthropic, "Tool runner" (SDK agentic loop helper) — https://docs.anthropic.com/en/api/tool-runner

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — stdlib only (numpy/tiktoken for exercises).
