# Day 34 — Monitoring, drift & the retraining loop

The course finale. The RAG service is live; production is a stream you watch. Hands-on: the
**golden signals** for an LLM app, **distribution drift** detection on the inputs (PSI + KS
from scratch), and the **refresh loop** that closes back to Day 33 — detect decay → collect +
label → update → eval-gate → canary → promote.

## Learning objectives

1. Name the golden signals for an LLM service and build an aggregator over a trace stream.
2. Compute Population Stability Index and a KS test to detect input drift; set thresholds.
3. Distinguish data drift, concept drift, and quality decay — and which signal catches each.
4. Implement a `RefreshTrigger` that combines drift + eval-score decay + user feedback.
5. Run a full simulated refresh loop and show the Day 33 eval gate + canary close it.
6. List the feedback-loop hazards: training on your own outputs, feedback bias, metric gaming.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Production is a stream, not a state | 3 min |
| 1 | Monitoring only latency, and missing the collapse | 7 min |
| 2 | Golden signals: an aggregator over the trace stream | 13 min |
| 3 | Drift from scratch: PSI and KS | 14 min |
| 4 | Alerting, sampling, PII — the operational layer | 6 min |
| 5 | The refresh loop, end to end | 14 min |
| 6 | Feedback hazards; course wrap-up | 3 min |
| 7 | Exercises and self-check quiz | — |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `numpy` and `scipy` (already installed). No API calls — the trace stream is synthetic.

## Run it

```bash
python -m jupyterlab projects/week-11-mlops-and-mcp/day-34-monitor-and-retrain/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Google SRE Book — "Monitoring Distributed Systems" (the four golden signals) — https://sre.google/sre-book/monitoring-distributed-systems/
- "A unified view of concept drift" — https://arxiv.org/abs/2004.00458
- Population Stability Index — https://www.listendata.com/2015/05/population-stability-index.html
- "Constitutional AI" / RLAIF self-training hazards — https://arxiv.org/abs/2212.08073

## Files

- `lesson.ipynb` — the guided lesson.
- `solutions/solutions.ipynb` — worked solutions + answer key.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, scipy.
