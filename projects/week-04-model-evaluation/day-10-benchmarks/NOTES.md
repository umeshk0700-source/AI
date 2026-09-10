# Day 10 — Benchmarks and their limits — cheat sheet

## The one-sentence version

A benchmark is a proxy measured under one harness; use it to shortlist models and spot
category weaknesses, never to make the final call — that needs your own task eval (Week 9).

## The two shapes

| Shape | Examples | Score | Weakness |
| ----- | -------- | ----- | -------- |
| Multiple-choice / exact-match | MMLU, ARC, GSM8K, TruthfulQA-MC | accuracy | chance floor, easy to game, format-sensitive |
| Execution / verifier | HumanEval, MBPP, SWE-bench | pass@k on hidden tests | expensive, narrow, k-dependent |
| Open-ended quality | chat, helpfulness | human / LLM judge | subjective, costly (Week 9) |

## The 5 limits

1. **Chance floor.** 4-way MC → 25% free. Normalise: `(score − 1/n) / (1 − 1/n)`.
2. **Aggregation.** Headline is a mean; opposite per-category profiles can tie. Read the
   breakdown.
3. **pass@k ≠ pass@1.** `pass@k = 1 − (1−p)^k`. More shots → higher score for free. Check the k.
4. **Contamination.** Test data in training → measures memory. Signs: implausibly high on old
   benchmarks, big drop on paraphrased / perturbed / fresh variants, score doesn't track
   downstream. Mitigate: private/held-out sets, canary strings, time-split (test only on
   post-cutoff data).
5. **Harness sensitivity.** Same model, same questions, ~15-point swing from option labels /
   few-shot / CoT / answer parsing. Only compare models run through the *identical* harness.

## Goodhart

"When a measure becomes a target, it ceases to be a good measure." Models get trained and
checkpoint-selected on benchmark-like data → benchmark saturates (~90%) while real gaps
persist → field retires it (MMLU → MMLU-Pro → GPQA → …).

## Code you will reuse

```python
def normalize(score, n_options):        # floor-adjusted score
    return (score - 1/n_options) / (1 - 1/n_options)

def pass_at_k(p, k):                     # p = true per-sample success rate
    return 1 - (1 - p) ** k
```

## Honest use

| Do | Don't |
| -- | ----- |
| Shortlist 2–3 candidates | Decide on a 1–2 point gap |
| Read per-category breakdowns | Trust the single mean |
| Check k / prompt / harness | Compare across harnesses |
| Prefer fresh / private / time-split | Trust old public benchmarks |
| Confirm with your own eval | Ship on public benchmarks alone |

## What this does not cover

- Cost / latency / accuracy tradeoffs across models — Day 11.
- Running your own multi-model comparison — Day 12.
- No-ground-truth and production evals — Week 9.
