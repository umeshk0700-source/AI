# Day 34 — Monitoring, drift & the refresh loop cheat sheet

## Golden signals for an LLM app
| Family | Signal |
| --- | --- |
| Latency | p50 / p95 / p99 |
| Traffic | req/s, tokens/s |
| Errors | error / refusal / timeout rate |
| Cost | $/req, $/day |
| **Quality** | retrieval hit rate, grounded rate, judge score on a sample |
| **Feedback** | thumbs-down rate, escalation rate |
Infra dashboards usually miss the last two — alert on `grounded_rate` like you alert on errors.

## Drift
- **PSI**: bin reference & current the same way, `Σ (cur% − ref%)·ln(cur%/ref%)`.
  `<0.1` stable · `0.1–0.25` moderate · `>0.25` significant. Works on numeric (quantile bins)
  and categorical (category proportions).
- **KS test** (`scipy.stats.ks_2samp`): max gap between empirical CDFs; `p < α` ⇒ drift.
- Types: data/covariate drift (inputs move → PSI/KS on input embeddings); **concept drift**
  (P(answer|input) moves, inputs unchanged → only re-labelled evals + feedback catch it);
  retrieval decay (corpus coverage → hit rate, PSI on doc age); model drift (provider changed
  → daily canary of the frozen eval set).

## Operational layer
- Alert on symptoms, page on impact; multi-window burn-rate > single threshold.
- Sample stored traces (~1–5%, but 100% of errors + thumbs-down).
- Redact PII before logging; never log keys/auth; set a retention window.
- Run the frozen Week-9 suite against prod daily as a model-drift canary.

## The refresh loop
```
serve → trace → signals → drift / decay / feedback
                     → RefreshTrigger (needs 2+ reasons, + cooldown)
   → collect good cases → rebuild (re-index / re-tune / new few-shots)
   → eval gate (Day 33) → canary (Day 33) → promote → new baseline → serve
```

## Feedback hazards
- Training on the model's own outputs → error compounding, diversity collapse. Use
  human-labelled/corrected data; gate model outputs through a judge + human sample.
- Feedback bias: thumbs-down is unrepresentative (given more often, by some users, on some
  topics).
- Goodhart: optimising `grounded_rate` → "always cite something". Keep a held-out human eval.
- Don't chase every PSI spike — a one-day news event isn't concept drift.
