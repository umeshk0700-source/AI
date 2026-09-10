# Week 7 Lab — Ops Automation Agent

## The brief

Your on-call engineers waste time during incidents looking up runbooks and filing tickets.
Build an agent that, given an incident description, can **search runbooks**, **check incident
status**, and **file an incident** — deciding for itself which tools to use and when to stop —
with the guards that keep it from looping, over-spending, or filing tickets without a human OK.

```
goal ─▶ Agent.run() ─▶ loop { llm.chat(tools) -> tool calls -> execute -> feed back } ─▶ final answer
guards: max_steps · repeated-call detection · tool-call budget · human approval for destructive tools
```

## Usage

```bash
cd projects/practice/week-07-ops-agent
make setup        # install deps (into the shared ../../../.venv)
make test         # offline unit tests — your work-in-progress: TODOs + failures
make solution     # the same tests against the reference implementation (all green)
make live         # real Claude/GPT — needs keys, costs ~$0.05   (preset: .env.preset)
make lab          # open the walkthrough notebook
```

**Presets.** `.env.preset` (committed, no secrets) pins the models and the spend cap for this
lab. `make live` sources it automatically. Your keys go in `projects/practice/.env`
(gitignored) — copy `projects/practice/.env.example`. Override a preset per run:
`ANTHROPIC_MODEL=claude-sonnet-4-5 LAB_USD_CAP=1 make live`.

## What you implement (`src/opsagent/`)

| File | TODOs |
| ---- | ----- |
| `agent.py` | `Agent._execute`, `Agent.run` (the loop + all four guards) |

Tools, the registry, and the destructive-tool flag are given.

## Acceptance criteria

- `pytest -q` green: with a scripted `FakeLLM` the agent completes a 2-tool task; a looping
  planner is aborted by the repeated-call guard; exceeding the tool budget aborts; a
  `create_incident` call is blocked when the approver returns `False` and the tool result
  carries `is_error`.
- `LLM_LIVE=1 pytest -q -m live`: real Claude tool-use — "find the rollback steps for the
  payments API outage" is answered from the runbook in ≤ 3 steps, no `create_incident` call,
  cost < $0.03.

Covers Day 19 (agent loop + guards), Day 21 (one-tool agent → several tools).
