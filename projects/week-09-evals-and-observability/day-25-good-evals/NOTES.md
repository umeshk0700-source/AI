# Day 25 — What makes a good eval — cheat sheet

## The one-sentence version

An eval is a measurement instrument — valid, reliable, sensitive, cheap — that answers "did
this change make the product better?"; a bad eval gives false confidence and you Goodhart
toward its blind spots.

## Dimensions

| Dimension | Question | Measure |
| --------- | -------- | ------- |
| Accuracy | is it right? | EM/F1 vs reference, judge, task check |
| Relevance | addresses *this* question? | sim(answer, question), judge |
| **Faithfulness** | every claim ⊆ provided context? | per-claim entailment (NLI / judge / embed proxy) |
| Completeness | covered all parts? | checklist of required elements |
| Format | parses / schema-valid? | parser / JSON-schema validator |
| Consistency | stable across re-runs? | variance over N samples |
| Safety | refuses right, no PII, non-toxic | classifier + rules |
| Latency / Cost | p50/p95 s, $/call | measure |

Correctness alone ≠ enough: a RAG answer can be **correct + unfaithful** (fact from weights,
not context) → silent retriever failure.

## Reference-based metrics and where they lie

| Metric | Lies when |
| ------ | --------- |
| Exact match | any valid paraphrase ("five business days") |
| Token F1 | word overlap ≠ meaning |
| BLEU/ROUGE | fluent correct paraphrase scores low; word-salad-with-right-words scores high |
| Embedding sim | can't tell correct from plausible-but-wrong |

→ combine; prefer faithfulness/judge for prose.

## LLM-as-judge

Rubric prompt → 1–5 scores on correctness/relevance/faithfulness, JSON out. Biases:

| Bias | Judge... | Fix |
| ---- | -------- | --- |
| verbosity/length | scores longer higher | "ignore length"; penalise padding |
| position (pairwise) | prefers first/fixed slot | swap order, require agreement |
| self-preference | prefers same model family | different judge model / ensemble |
| sycophancy | rewards confident tone | rubric weights evidence not confidence |
| format halo | markdown reads as quality | judge content only |

**Calibrate against 50–100 human labels** — report MAE + rank correlation. An uncalibrated
judge is a random number generator with good PR.

## No ground truth? Evaluate anyway

1. Property checks (faithfulness, format, safety, on-topic) — cheap, deterministic.
2. Self-consistency — sample N; low agreement = low confidence, route to review.
3. Calibrated LLM-judge with a rubric.
4. **Pairwise vs baseline** — "is B better than A on this input?" — easier for a judge, and
   it's the question you actually care about.
5. Human review of a sample (20–50/release), especially the disagreement set.

## Offline eval vs production monitoring

| | Offline | Production |
| --- | --- | --- |
| Data | frozen curated test set | live unlabelled shifting traffic |
| Question | "is the new version better?" | "is quality holding / anything on fire?" |
| Ground truth | yes | rarely (property checks + sampled judge + user signals) |
| Catches | regressions from your change | prompt drift, model updates, new query types, abuse |

Need both; feed production failures back into the offline set.

## What this does not cover

- Building the actual harness — Day 26.
- Tracing / logging — Day 27.
