# Week 11 lab — platform-ops

**Use case.** You own the platform for the RAG service shipped in Week 10. Product wants to
release changes weekly without regressions reaching users, and the service must stay healthy
as the question mix and the document corpus drift. Build the control plane: a **release
gate**, a **canary controller**, a **drift monitor**, a **signal aggregator**, and the
**refresh trigger** that ties them together.

Lessons [Day 33](../../week-11-mlops-and-mcp/day-33-cicd-and-release/) and
[Day 34](../../week-11-mlops-and-mcp/day-34-monitor-and-retrain/) teach these ideas; here you
build the production version with typed interfaces and a test suite.

## Usage

```bash
cd projects/practice/week-11-platform-ops
make setup        # install deps into the shared venv
make test         # offline unit tests — your TODOs fail until implemented
make solution     # the same tests against solution/ (all green)
make live         # one end-to-end test with a real Claude judge (~$0.05, per .env.preset)
make lab          # open the walkthrough notebook
```

Implement the `TODO`s in `src/platformops/`, re-run `make test` until green. `solution/` is
the reference.

## What you implement

| Module | Class / fn | Job |
| ------ | ---------- | --- |
| `gate.py` | `ReleaseGate.check` | block a candidate that drops the aggregate eval score or regresses a case not on the allow-list |
| `canary.py` | `CanaryController.roll_out`, `_healthy` | ramp 5→25→50→100% while p95 latency / error rate / quality hold; roll back on breach |
| `drift.py` | `psi`, `categorical_psi`, `ks_drift`, `DriftMonitor.assess` | detect input distribution drift |
| `signals.py` | `SignalAggregator.observe`, `signals` | the golden signals over a rolling trace window |
| `refresh.py` | `RefreshTrigger.decide` | fire only when ≥2 of {drift, low grounded rate, eval decay, high thumbs-down} breach |

## Acceptance criteria

- `make test` green (15 offline tests): gate blocks/permits correctly, canary promotes a
  healthy candidate and rolls a bad one back at step 1, PSI/KS behave on same vs shifted
  samples, the aggregator's window is bounded and its quality signal drops when the corpus
  misses a topic while error rate does not, the trigger needs 2+ reasons.
- `make solution` green.
- `make live` (with keys): a real judge scores a good and a bad bundle; the gate passes the
  first and blocks the second.

## Files

- `src/platformops/` — the stubs you implement.
- `solution/platformops/` — the reference implementation.
- `tests/` — offline tests + `test_live.py` (marked `live`).
- `fixtures/trace_helpers.py` — synthetic trace stream + canary measurement fns.
- `lab.ipynb` — walkthrough: wire the five components into one refresh loop.
- `.env.preset` — model + `$0.05` cap for `make live` (no secrets).
