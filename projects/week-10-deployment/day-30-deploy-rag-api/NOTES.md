# Day 30 — Deploy the RAG pipeline as an API — cheat sheet

## The one-sentence version

Serverless HTTP API for RAG: API Gateway (auth + throttle) → thin Lambda (no model in it) →
Bedrock/Anthropic + vector DB; module-scope init, 25s timeout, structured logs with a
trace_id, and move off Lambda when requests exceed 29s or RPS is steady-high.

## The handler

```python
# module scope — runs ONCE per cold start, reused by every warm invocation
STATE = _init()            # boto3 clients, config, secrets — NOT the KB, NOT a model

def handler(event, context=None):
    trace_id = context.aws_request_id
    body = json.loads(event.get("body") or "{}")
    question = (body.get("question") or "").strip()
    if not question: return _response(400, {"error": "missing 'question'"}, trace_id)
    answer, sources = rag_answer(question, STATE)
    print(json.dumps({"evt": "rag_request", "trace_id": trace_id, "latency_ms": ...}))
    return _response(200, {"answer": answer, "sources": sources, "trace_id": trace_id}, trace_id)
```

Contract: `POST /ask` · `{"question": "<=2000"}` · `x-api-key` → `200 {answer, sources,
trace_id, latency_ms}` / `400` / `413` / `429` (edge) / `500 {error, trace_id}`. Every response
carries `x-trace-id`.

## Cold starts

| Cause | Fix |
| ----- | --- |
| `torch` / `sentence-transformers` in the zip | use **API embeddings** (Bedrock Titan) or a **Knowledge Base** — no model in the Lambda |
| Loading KB/index at init | keep it in the vector DB; handler just queries |
| First request after idle | **provisioned concurrency** (keep N warm) |
| Big zip / slow import | trim deps, lazy-import, arm64 manylinux wheels |

**The rule:** no model in the Lambda → ~200ms cold start instead of seconds.

## SAM template essentials

- `Timeout: 25` (< 29s API Gateway hard cap)
- `Architectures: [arm64]` (~20% cheaper, faster here)
- `ReservedConcurrentExecutions` — caps cost blast radius + protects Bedrock quota / DB pool
- `ProvisionedConcurrencyConfig` — hot path always warm
- IAM: only `bedrock:InvokeModel` on `anthropic.*` + read the one secret. No `*`.
- Rollout: `AutoPublishAlias` + `DeploymentPreference: Canary10Percent5Minutes` + an error alarm

## Auth / limits / logs / errors

- **API keys + usage plans** (`ApiKeyRequired: true`) — rate limit enforced at the edge, before
  Lambda, so throttled callers cost nothing. User-facing → Lambda authorizer / Cognito.
- **Request validation** at the route (JSON schema) — reject malformed bodies at the edge.
- **One structured JSON log line** per request → CloudWatch → Logs Insights dashboard (= your
  production monitoring, Day 25). Turn on **X-Ray**.
- Map exceptions → HTTP status; always return `trace_id`; never leak stack traces.
- Secrets from Secrets Manager/SSM, fetched at init, cached. Never plaintext env vars.

## Streaming

API Gateway buffers → no streaming. Use a **Lambda Function URL** with response-stream mode
(up to 15 min / 20 MB) for long answers or typewriter UX.

## When NOT Lambda

| Situation | Use |
| --------- | --- |
| requests > 29s | Fargate / App Runner + ALB, or Function-URL streaming |
| steady high RPS | always-on container (Fargate / App Runner / EKS) |
| needs a GPU | ECS-GPU / EKS / SageMaker endpoint / Bedrock |
| WebSockets / long-lived | API Gateway WebSocket + Lambda, or Fargate |

Lambda is right for RAG when: spiky/low-average traffic, few-second requests, no model in the
function.

## What this does not cover

- Multi-region / DR, blue-green at the API Gateway layer.
- CI/CD pipeline wiring (CodePipeline / GitHub Actions + `sam deploy`).
