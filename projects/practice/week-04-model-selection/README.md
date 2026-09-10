# Week 4 Lab — Model Selection Board

## The brief

Finance wants to auto-extract fields from vendor invoices (10k/month). You must pick **one
model** and defend it. Run the *same* extraction task across a lineup, measure field accuracy,
latency and real cost, and produce a `SelectionMemo` the team can sign off.

```
invoice text ─▶ Extractor(model).extract() ─▶ Extraction{vendor, invoice_number, total,
                                                          currency, due_date, line_item_count}
ModelBench.run({...}) ─▶ per-model metrics ─▶ ModelBench.select() ─▶ SelectionMemo
```

## Usage

```bash
cd projects/practice/week-04-model-selection
make setup        # install deps (into the shared ../../../.venv)
make test         # offline unit tests — your work-in-progress: TODOs + failures
make solution     # the same tests against the reference implementation (all green)
make live         # real Claude/GPT — needs keys, costs ~$0.15   (preset: .env.preset)
make lab          # open the walkthrough notebook
```

**Presets.** `.env.preset` (committed, no secrets) pins the models and the spend cap for this
lab (gpt-4o-mini vs claude-haiku — swap to gpt-4o / claude-sonnet-4-5 for a sharper comparison). `make live` sources it automatically. Your keys go in `projects/practice/.env`
(gitignored) — copy `projects/practice/.env.example`. Override a preset per run:
`ANTHROPIC_MODEL=claude-sonnet-4-5 LAB_USD_CAP=1 make live`.

## What you implement (`src/bench/`)

| File | TODOs |
| ---- | ----- |
| `extractor.py` | `Extractor.extract` (schema-constrained call + parse) |
| `bench.py` | `ModelBench._score_one`, `ModelBench.run`, `ModelBench.select` |

## Acceptance criteria

- `pytest -q` green: `_score_one` field accuracy math; `select` returns the **cheapest** model
  whose accuracy clears `min_accuracy`, or the most accurate if none do, with a populated
  comparison table.
- `LLM_LIVE=1 pytest -q -m live`: real `claude-haiku-4-5` + `gpt-4o-mini` over 8 fixture
  invoices; a `SelectionMemo` is produced, every model's `field_accuracy` is populated, the
  `recommended` label is one of the lineup, and the run costs < $0.10.

Covers Day 10 (benchmark limits), Day 11 (cost/latency/accuracy), Day 12 (bake-off).
