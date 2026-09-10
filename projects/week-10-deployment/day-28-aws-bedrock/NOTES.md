# Day 28 — AWS Bedrock — cheat sheet

## The one-sentence version

Bedrock = Claude (and other models) called from inside AWS with IAM auth, in-region data, VPC,
and CloudTrail — one `converse` API across vendors — at the cost of a weeks-to-months lag
behind the first-party API.

## Three doors to Claude on AWS

| Door | Auth | Pricing | Pick when |
| ---- | ---- | ------- | --------- |
| First-party Anthropic API | key / OAuth | Anthropic list | newest features, simplest |
| Claude Platform on AWS | AWS | Anthropic list | AWS billing + same-day parity |
| **Amazon Bedrock** | IAM | Bedrock pricing | deep in AWS (IAM/VPC/CloudTrail), one API |

## `converse` (boto3, `bedrock-runtime`)

```python
brt = boto3.client("bedrock-runtime", region_name="us-east-1")
resp = brt.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",   # inference profile
    system=[{"text": "..."}],
    messages=[{"role": "user", "content": [{"text": "..."}]}],
    inferenceConfig={"maxTokens": 512},
    toolConfig={"tools": [{"toolSpec": {"name": ..., "inputSchema": {"json": {...}}}}]},
)
resp["output"]["message"]["content"][0]["text"]
resp["usage"]        # inputTokens / outputTokens / totalTokens
resp["stopReason"]   # end_turn | max_tokens | tool_use | ...
```

Shape vs first-party: `content` is a list of `{"text": ...}` / `{"toolUse": ...}` blocks,
camelCase keys, `system` is a list, tool results are `{"toolResult": {"toolUseId", "content":
[{"json": ...}]}}`.

`invoke_model` = send the vendor's native body (Anthropic Messages JSON for Claude); more
control, less portable. Or use `AnthropicBedrockMantle(aws_region=...)` for the first-party SDK
surface routed through Bedrock.

## Model IDs

- `anthropic.claude-...-v1:0` — region-pinned foundation model.
- `us.` / `eu.` / `apac.` prefix — **inference profile** = cross-region routing (higher
  availability, same price). **Use in production** unless data residency pins one region.
- Request model access once per account. Not every model in every region.

## Pricing

- **On-demand** — per token, no commit. **The default.** Subject to account throughput quotas.
- **Provisioned Throughput** — reserve model units (fixed tokens/min) for 1- or 6-month
  commits. Predictable, no throttling; you pay whether used or not. Rarely beats on-demand for
  token-metered models — only at steady very-high load; size for p95.
- **Batch** — ~50% off, async, results to S3.
- **Prompt caching** — available on Bedrock (separate cache-write/read rates).

## Managed add-ons (= things you built earlier)

| Feature | = your | Trade |
| ------- | ------ | ----- |
| Guardrails | Day 16/25/27 (refusal, safety, redaction) | config vs code |
| Knowledge Bases (`retrieve_and_generate`) | Weeks 5–6 (RAG) | fast ship vs tuning chunking/hybrid/rerank |
| Agents | Day 19/21 (tool loop) | managed loop vs control |

## Clients

`bedrock` = control plane (list models, provisioned throughput, guardrails, logging).
`bedrock-runtime` = data plane (`converse`, `invoke_model`, `apply_guardrail`).
`bedrock-agent-runtime` = `retrieve`, `retrieve_and_generate`, `invoke_agent`.

## What this does not cover

- Sizing/paying for the serving layer — Day 29.
- Deploying the endpoint (Lambda + API Gateway) — Day 30.
