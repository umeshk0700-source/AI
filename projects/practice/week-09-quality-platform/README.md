# Week 9 Lab — LLM Quality Platform

## The brief

Every prompt or model change to the policy assistant (Week 6) is a coin flip right now — nobody
knows if it got better or worse. Build the quality gate that runs in CI: a versioned eval
suite, an **LLM-as-judge** scorer for the free-text answers, and a **regression gate** that
blocks a merge if faithfulness, correctness or safety drops.

```
EvalSuite(cases) + scorers ─▶ run(system_under_test) ─▶ Report
RegressionGate(baseline).check(candidate) ─▶ Verdict{passed, deltas, blocking[]}
```

## Usage

```bash
cd projects/practice/week-09-quality-platform
make setup        # install deps (into the shared ../../../.venv)
make test         # offline unit tests — your work-in-progress: TODOs + failures
make solution     # the same tests against the reference implementation (all green)
make live         # real Claude/GPT — needs keys, costs ~$0.20   (preset: .env.preset)
make lab          # open the walkthrough notebook
```

**Presets.** `.env.preset` (committed, no secrets) pins the models and the spend cap for this
lab (the judge needs a capable model — sonnet-4.5 / gpt-4o by default). `make live` sources it automatically. Your keys go in `projects/practice/.env`
(gitignored) — copy `projects/practice/.env.example`. Override a preset per run:
`ANTHROPIC_MODEL=claude-sonnet-4-5 LAB_USD_CAP=1 make live`.

## What you implement (`src/quality/`)

| File | TODOs |
| ---- | ----- |
| `scorers.py` | `Contains.score`, `LLMJudge.score` |
| `suite.py` | `EvalSuite.run` (per-case, per-tag aggregation) |
| `gate.py` | `RegressionGate.check` |

## Acceptance criteria

- `pytest -q` green: `Contains` and `ExactMatch` behave; the suite aggregates by tag; the gate
  PASSES a no-op change, FAILS when a `must_not_regress` metric drops beyond tolerance, and
  lists *which* metrics blocked; a hard assertion (e.g. an injection-resistance check)
  short-circuits the gate.
- `LLM_LIVE=1 pytest -q -m live`: a real judge (`claude-sonnet-4-5` or `gpt-4o`) scores 6
  candidate answers against references; its scores correlate (rank) with the hand labels
  (Spearman ≥ 0.7), and the gate correctly flags a seeded regression run.

Covers Day 25 (judge + calibration), Day 26 (harness + gate), Day 27 (what to trace).
