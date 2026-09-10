# Day 30 — Deploy the RAG pipeline as an API

Package Week 6's RAG pipeline as an HTTP endpoint: the Lambda handler, the request/response
contract, cold-start mitigation, the API Gateway + IAM infrastructure, auth and rate limiting,
and when Lambda is the wrong choice. The handler runs locally in the notebook exactly as it
would in Lambda; the deployable artifacts (`template.yaml`, `src/`) are written to this folder.

## Learning objectives

By the end of the hour you should be able to:

1. Write a Lambda handler with module-scope init, an API-Gateway-shaped event contract, and
   proper HTTP status mapping.
2. Explain cold starts for ML workloads and apply the design rule: keep no model in the
   Lambda.
3. Read a SAM template: timeout under the 29s API Gateway cap, arm64, reserved + provisioned
   concurrency, least-privilege IAM.
4. Choose auth (API keys + usage plan vs Lambda authorizer vs Cognito) and rate limiting, and
   know why edge enforcement saves money.
5. Emit one structured log line per request (trace_id, latency, cold_start) and query it.
6. Decide when Lambda is wrong (>29s, steady high RPS, GPU, WebSockets) and what to use
   instead.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The target: a serverless HTTP API | 3 min |
| 1 | The Lambda handler + the contract | 14 min |
| 2 | Cold starts: the enemy of ML on Lambda | 12 min |
| 3 | The infrastructure (SAM template, API Gateway, IAM) | 12 min |
| 4 | Auth, rate limiting, logging, errors | 12 min |
| 5 | When Lambda is the wrong choice | 4 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs offline — the handler is invoked locally against fake API Gateway events. To deploy for
real: `sam build && sam deploy --guided` (needs the AWS SAM CLI + credentials).

## Source material

- AWS SAM developer guide — https://docs.aws.amazon.com/serverless-application-model/
- AWS, "Lambda response streaming" — https://docs.aws.amazon.com/lambda/latest/dg/configuration-response-streaming.html
- AWS Lambda Power Tuning — https://github.com/alexcasalboni/aws-lambda-power-tuning
- Day 27 (tracing), Day 28 (Bedrock), Day 29 (serving cost).

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `template.yaml` — the SAM template (written by the notebook).
- `src/` — where `handler.py` + the Lambda `requirements.txt` go.
- `requirements.txt` — stdlib only to run the notebook.
