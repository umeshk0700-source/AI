# Day 31 — MCP: the Model Context Protocol

Build the Model Context Protocol from scratch (it is JSON-RPC 2.0 over a pipe), then use the
official `mcp` SDK, then wire an MCP server into an agent turn so the agent discovers its
tools at runtime instead of importing them.

## Learning objectives

By the end of the hour you should be able to:

1. Explain the N×M integration problem MCP solves and where it sits vs raw function-calling.
2. Speak the three core JSON-RPC methods by hand: `initialize`, `tools/list`, `tools/call`.
3. Implement a minimal MCP server and client over stdio.
4. Use `FastMCP` to expose tools and `ClientSession` to consume them.
5. Convert MCP tool definitions into an Anthropic tool schema and run one agent step.
6. Name the trust-boundary risks: prompt injection via tool descriptions, tool shadowing,
   over-broad scopes.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The N×M problem | 4 min |
| 1 | Hand-wired tools, and why they don't compose | 8 min |
| 2 | The protocol by hand: JSON-RPC messages | 12 min |
| 3 | A stdio server + client from scratch | 12 min |
| 4 | Resources, prompts, capabilities | 5 min |
| 5 | The real SDK: FastMCP + ClientSession + an agent turn | 15 min |
| 6 | Trust boundaries; bridge to deployment | 4 min |
| 7 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `mcp<2` (added to the root `requirements.txt`). Everything runs locally over subprocess
stdio — no network, no API key. The agent step uses a fake LLM. The notebook writes a few
helper `*.py` files into this folder as it runs.

## Run it

```bash
python -m jupyterlab projects/week-11-mlops-and-mcp/day-31-mcp/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Model Context Protocol — spec & docs — https://modelcontextprotocol.io
- Python SDK — https://github.com/modelcontextprotocol/python-sdk
- JSON-RPC 2.0 — https://www.jsonrpc.org/specification
- Anthropic, "MCP" — https://docs.anthropic.com/en/docs/agents-and-tools/mcp

## Files

- `lesson.ipynb` — the guided lesson.
- `solutions/solutions.ipynb` — worked solutions + answer key (try the exercises first).
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — `mcp`.
