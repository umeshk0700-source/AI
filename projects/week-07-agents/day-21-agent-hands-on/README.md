# Day 21 — Build a simple agent (hands-on)

One model, one tool (`search_kb`), the loop from Day 19: a help-desk agent that decides *when*
to search a knowledge base instead of always retrieving. Runs against the Anthropic API when
`ANTHROPIC_API_KEY` is set, with a working local fallback so it executes offline.

## Learning objectives

By the end of the hour you should be able to:

1. Define a single tool as a JSON schema and wire it into the Anthropic tool-use loop.
2. Explain the decision an agentic RAG system makes that a fixed pipeline doesn't (whether /
   how many times / with what query to retrieve).
3. Handle greetings (no search), single-hop, multi-hop, and out-of-scope questions in one loop.
4. Apply loop and budget guards to a real agent.
5. Evaluate agentic vs always-retrieve on a mixed question set (correctness, wasted searches,
   cost).

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The task: agentic RAG with one tool | 4 min |
| 1 | The tool: `search_kb` | 8 min |
| 2 | The agent loop (Anthropic tool-use + local fallback) | 16 min |
| 3 | Run it: single-hop, multi-hop, no-match | 12 min |
| 4 | Guards in action | 8 min |
| 5 | Evaluate: agentic vs always-retrieve | 9 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (MiniLM) for the tool. Generation/planning runs on a deterministic
local planner offline; set `ANTHROPIC_API_KEY` and paste `run_agent_anthropic` (shown in §2)
to run the real model. `anthropic` is in the shared venv.

## Run it

```bash
python -m jupyterlab projects/week-07-agents/day-21-agent-hands-on/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Anthropic tool use docs — https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Anthropic, "Building effective agents" — https://www.anthropic.com/research/building-effective-agents
- "Self-RAG" / adaptive retrieval — https://arxiv.org/abs/2310.11511
- Day 19 (agent loop + guards), Day 18 (RAG baseline).

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, numpy; anthropic (optional, for the real run).
