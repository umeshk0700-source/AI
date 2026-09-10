# Week 2 Lab — Support Ticket Triage Service

## The brief

You're on the platform team at a B2B SaaS company. Support gets ~4,000 inbound tickets/week.
Agents waste hours reading, categorising and routing them. Build the **triage service** that
sits in front of the queue: given a raw ticket it emits a structured decision that the routing
system and the agent UI consume.

```
inbound ticket ─▶ TriageService.triage() ─▶ TriageResult
                                             { category, priority, sentiment,
                                               needs_human, route_to_team,
                                               sla_due_at, draft_reply, confidence }
```

The model does the reading; **your code owns the business rules** layered on top (SLA math,
priority escalation for enterprise customers, hard routing for security/legal).

## Usage

```bash
cd projects/practice/week-02-support-triage
make setup        # install deps (into the shared ../../../.venv)
make test         # offline unit tests — your work-in-progress: TODOs + failures
make solution     # the same tests against the reference implementation (all green)
make live         # real Claude/GPT — needs keys, costs ~$0.10   (preset: .env.preset)
make lab          # open the walkthrough notebook
```

**Presets.** `.env.preset` (committed, no secrets) pins the models and the spend cap for this
lab. `make live` sources it automatically. Your keys go in `projects/practice/.env`
(gitignored) — copy `projects/practice/.env.example`. Override a preset per run:
`ANTHROPIC_MODEL=claude-sonnet-4-5 LAB_USD_CAP=1 make live`.

## What you implement (`src/triage/`)

| File | TODOs |
| ---- | ----- |
| `prompts.py` | `FewShotStrategy.build`, `ChainOfThoughtStrategy.build` |
| `service.py` | `TriageService._classify` (the schema-constrained LLM call), `_apply_rules` (routing + escalation + SLA), `triage`, `triage_batch` |
| `evaluate.py` | `TriageEval.score_one`, `TriageEval.run` |

`schemas.py` and the LLM plumbing (`llmlab`) are given.

## Acceptance criteria

- `pytest -q` green (offline: schema validation, prompt content, routing rules, service logic
  with a `FakeLLM`).
- `LLM_LIVE=1 pytest -q -m live` green: over the 12 fixture tickets —
  category accuracy ≥ 0.75, priority within ±1 ≥ 0.80, `needs_human` recall ≥ 0.80,
  run cost < $0.10.
- Swapping `get_client("anthropic")` ↔ `get_client("openai")` requires **no change** to
  `service.py`.

