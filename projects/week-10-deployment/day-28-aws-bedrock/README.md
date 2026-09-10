# Day 28 — AWS Bedrock for deployment

Bedrock is a managed way to call foundation models (Claude included) from inside AWS: one API,
IAM auth, data that stays in your region, plus Guardrails / Knowledge Bases / Agents. This
day: what it adds over the first-party API, the `converse` request shape, model IDs and
inference profiles, the pricing model, and when to pick which door.

## Learning objectives

By the end of the hour you should be able to:

1. Compare the three doors to Claude on AWS (first-party API, Claude Platform on AWS, Bedrock)
   and pick one for a scenario.
2. List what Bedrock adds (IAM, data residency, VPC, CloudTrail, one API, provisioned
   throughput) and what it costs you (feature lag).
3. Write a `converse` / `converse_stream` call including tool use, and map it to/from the
   first-party Messages shape.
4. Explain cross-region inference profiles and when to use one.
5. Decide on-demand vs provisioned throughput vs batch with a cost calculator.
6. Recognise Guardrails / Knowledge Bases / Agents as managed versions of Weeks 5–9.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Three doors to Claude on AWS | 5 min |
| 1 | What Bedrock adds over the direct API | 10 min |
| 2 | The `converse` API (and `invoke_model`) | 14 min |
| 3 | Model IDs, regions, inference profiles | 8 min |
| 4 | Pricing: on-demand vs provisioned throughput | 10 min |
| 5 | Guardrails, Knowledge Bases, Agents | 8 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs offline against a mock `bedrock-runtime` client that mirrors `converse` / `converse_stream`.
Real `boto3` calls are shown alongside every mock. No AWS account needed.

## Source material

- AWS, "Amazon Bedrock — Converse API" — https://docs.aws.amazon.com/bedrock/latest/userguide/converse-api.html
- AWS, "Cross-region inference" — https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
- AWS, "Provisioned Throughput" — https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html
- AWS, "Bedrock Guardrails / Knowledge Bases / Agents" — https://docs.aws.amazon.com/bedrock/
- `claude-api` skill → `shared/platform-availability.md`, Provider Clients.

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — stdlib only (mock); `boto3` / `anthropic[bedrock]` for the real thing.
