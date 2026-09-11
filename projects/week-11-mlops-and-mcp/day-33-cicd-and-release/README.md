# Day 33 — CI/CD and eval-gated release

How a change to the RAG service — code, prompt, or re-chunked index — reaches production
without a regression reaching users first. Build a pipeline runner, an **eval gate** that
blocks quality regressions against a stored baseline, and a **canary controller** with
automatic rollback — all from scratch, offline, with a fake judge.

## Learning objectives

1. Model a CI pipeline as ordered stages with fail-fast and artifacts passed between them.
2. Build an eval gate: run the suite, compare to a stored baseline, block on regression.
3. Read a GitHub Actions workflow and map each job to a pipeline stage.
4. Explain blue/green vs canary vs shadow deployment and what each protects against.
5. Implement a canary controller: traffic split → metric collection → SLO check → promote/rollback.
6. Explain why prompt + code + index must be versioned and rolled back together.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The question: safe path from commit to prod | 3 min |
| 1 | "push to main = deploy", and the regression it ships | 8 min |
| 2 | A pipeline runner: stages, fail-fast, artifacts | 12 min |
| 3 | The eval gate: baseline, threshold, allow-list | 13 min |
| 4 | The same pipeline in GitHub Actions | 6 min |
| 5 | Progressive delivery: canary with auto-rollback | 15 min |
| 6 | Versioning the whole bundle; bridge to monitoring | 3 min |
| 7 | Exercises and self-check quiz | — |

## Setup

```bash
source ../../../.venv/bin/activate
```

Pure standard library + a fixed random seed. No API calls. Writes an example `ci.yml` into
this folder as it runs.

## Run it

```bash
python -m jupyterlab projects/week-11-mlops-and-mcp/day-33-cicd-and-release/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- GitHub Actions — https://docs.github.com/actions
- Anthropic — building evals / test-driven development — https://docs.anthropic.com/en/docs/test-and-evaluate
- "Progressive Delivery" (canary / blue-green) — https://martinfowler.com/bliki/BlueGreenDeployment.html
- Google SRE Workbook — "Canarying Releases" — https://sre.google/workbook/canarying-releases/

## Files

- `lesson.ipynb` — the guided lesson.
- `solutions/solutions.ipynb` — worked solutions + answer key.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — none (standard library only).
