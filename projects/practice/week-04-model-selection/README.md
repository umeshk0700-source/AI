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
