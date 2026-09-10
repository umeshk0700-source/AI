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

## Run

```bash
pip install -r requirements.txt
pytest -q                       # your WIP: failures + NotImplementedError
LLM_LIVE=1 pytest -q -m live      # real Claude/GPT, ~$0.03
jupyter lab lab.ipynb
```

Covers Day 04 (token budget), Day 05 (zero/few-shot/CoT), Day 06 (bake-off harness).
