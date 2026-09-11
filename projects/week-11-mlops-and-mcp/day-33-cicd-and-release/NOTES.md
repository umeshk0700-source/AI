# Day 33 — CI/CD & eval-gated release cheat sheet

## Pipeline stages (cheap → valuable)
lint/type → unit tests → **eval suite** → build image → **canary in prod**
- Unit tests check *shape* (non-empty, cited, within limits). They can't see answers got worse.
- Model the pipeline as ordered `(name, fn)`; each stage gets a shared `context`, returns
  artifacts, may fail → fail-fast stop.

## The eval gate
- Run the Week-9 suite on the candidate; compare to a stored **baseline** (last shipped).
- Block if: aggregate drops > `tolerance`, OR any case regresses pass→fail not on the
  reviewed **allow-list**.
- Baseline is a versioned artifact, keyed by deployed bundle id; a shipped candidate's scores
  become the new baseline.
- Full suite on main/release; fast seeded subset on PRs. Average aggregate over N runs;
  require regressions to reproduce (LLM scores are noisy).

## GitHub Actions mapping
- `jobs` = stages; `needs:` = ordering; `environment: production` = manual-approval gate.
- **Branch protection** makes a job a *required status* → red = no merge.
- Secrets from `secrets.*`, never the repo.

## Progressive delivery
| Strategy | How | Protects against |
| --- | --- | --- |
| Blue/green | full v2, flip LB, keep v1 warm | fast rollback (but 100% at flip) |
| Canary | X% to v2, ramp 5→25→50→100 on metrics | blast radius; auto-rollback |
| Shadow | mirror traffic to v2, don't return it | zero user risk; offline compare |

Canary needs: guardrail metrics (p95 latency + error rate + a **quality** proxy), enough
exposure for significance (time *and* request count; sequential testing for small deltas), and
a rollback definition.

## Version the whole bundle
An answer = code × prompt × index × model. Ship one versioned bundle
(`release-2026-09-10.4` pins image tag + prompt hash + index URI + model id). Rollback =
redeploy the previous bundle atomically. Rolling back code alone → untested combination.
