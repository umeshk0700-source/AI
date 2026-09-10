# Day 06 — Prompt Workbench — cheat sheet

## The one-sentence version

Never ship a prompt you didn't measure: a gold set + a scoring function + a runner turns
"this prompt feels better" into "prompt 6 gets 0.90 at 30% the token cost of prompt 10".

## The harness, in three pieces

| Piece | What it is | Real-world size |
| ----- | ---------- | --------------- |
| Gold set | `[(input, expected_output), ...]` labeled by hand | 50–200, with a held-out slice |
| Scoring function | `response, gold -> {format_ok, fields, score}` | partial credit; format scored separately |
| Runner | every prompt × every gold item × N repeats → table | N ≥ 5 because models are stochastic |

## What the bake-off reliably shows

- Naming **JSON** / giving an explicit **schema** = the biggest jump in format validity.
- **Rules text** (explicit thresholds) lifts accuracy on fields that depend on thresholds
  (priority, needs_human) more than examples alone do.
- **Few-shot** locks output format/style and helps borderline category calls.
- **Few-shot + CoT** usually wins on score but costs 3–6× the tokens and more latency.
- There's often a **mid prompt** (schema + rules, no CoT) at ~90% of best score for ~30% cost.

## How to choose

Pick from the **frontier**, not the top score: the cheapest prompt that clears your quality
bar. Escalate only if the bar isn't met. Recompute cost at real volume
(`$3/1M in`, `$15/1M out` order-of-magnitude) before committing.

## Code you will reuse

```python
def extract_json(text):
    m = re.search(r"\{.*\}", text, re.DOTALL)
    try: return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError: return None

def score_response(text, gold):        # 0 if unparseable, else field-match fraction
    obj = extract_json(text)
    if not (obj and REQUIRED_KEYS <= set(obj)): return {"format_ok": 0, "score": 0.0}
    ...
```

## Gotchas

- One run is an anecdote. Repeat and report mean + spread.
- Prompts are **not portable across model versions** — re-run the harness after any model swap.
- A blended score hides whether format or reasoning is what's hurting you. Keep them separate.
- Don't peek at the held-out slice while iterating.

## What this does not cover

- No-ground-truth evals (LLM-as-judge, faithfulness) — Week 9.
- Cross-model comparison and cost/latency tradeoffs — Week 4.
- Constrained decoding / tool schemas for guaranteed-valid output — Week 8.
