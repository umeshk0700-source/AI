# Week 3 Lab — Domain Adaptation: decide, then build

## The brief

Product wants a "Cirrus policy assistant" that answers employee questions about the internal
handbook in the company's house style. Three ways to get there: **prompt engineering**, **RAG**,
or **fine-tuning**. Leadership wants a defensible recommendation *and* a working proof of the
mechanism you recommend.

You build:

1. `CapabilityRouter` — takes a `Requirement` (what's missing: knowledge vs behaviour, volume,
   freshness, data availability) and returns a recommendation with a cost model and reasons.
2. `LoRAAdapter` + `LoRATrainer` — a low-rank adapter and its training loop, in numpy, so the
   "fine-tune" recommendation isn't hand-waving. (This part is pure math, no API.)
3. `DatasetAudit` — the pre-flight checks that decide whether a fine-tune is even worth running:
   duplicates, train/test leakage, format drift, label noise.

## Usage

```bash
cd projects/practice/week-03-domain-adaptation
make setup        # install deps (into the shared ../../../.venv)
make test         # offline unit tests — your work-in-progress: TODOs + failures
make solution     # the same tests against the reference implementation (all green)
make live         # real Claude/GPT — needs keys, costs ~$0.02   (preset: .env.preset)
make lab          # open the walkthrough notebook
```

**Presets.** `.env.preset` (committed, no secrets) pins the models and the spend cap for this
lab. `make live` sources it automatically. Your keys go in `projects/practice/.env`
(gitignored) — copy `projects/practice/.env.example`. Override a preset per run:
`ANTHROPIC_MODEL=claude-sonnet-4-5 LAB_USD_CAP=1 make live`.

## What you implement (`src/adapt/`)

| File | TODOs |
| ---- | ----- |
| `router.py` | `CapabilityRouter.recommend`, `CostModel.monthly` |
| `lora.py` | `LoRAAdapter.delta`, `LoRAAdapter.forward`, `LoRATrainer.step`, `LoRAAdapter.merge` |
| `audit.py` | `DatasetAudit.duplicates`, `.leakage`, `.format_consistency`, `.run` |

## Acceptance criteria

- `pytest -q` green: router picks RAG for large/changing knowledge, fine-tune for
  behaviour-at-scale, prompt otherwise; LoRA at step 0 == base model; merged == unmerged;
  a rank-2 target is recovered by `r>=2` and not by `r=1`; audit flags an injected dup + leak.
- `LLM_LIVE=1 pytest -q -m live`: a real few-shot Claude call on the handbook task is the
  *baseline* the router's cost model is compared against; assert the router's recommendation
  for the given requirement is `"finetune"` and its projected monthly cost beats the
  per-call few-shot cost at the stated volume.

