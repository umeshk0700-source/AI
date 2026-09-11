# AI Upskill — Daily Deep Dives

One concept per day, one hour each, learned by building it from scratch rather than reading about it.

Days are grouped into 11 themed weeks. Every day lives in its own folder with the same files:
a `README.md` with the agenda, a `lesson.ipynb` you actually run, a `NOTES.md` cheat sheet to
keep, a `requirements.txt`, and a `solutions/solutions.ipynb` holding the worked exercise
solutions + the quiz answer key (attempt the exercises before opening it).

New here? Read [../LEARNING_PATH.md](../LEARNING_PATH.md) — it picks a subset for a one-week,
core, or full track instead of grinding all 34 days in order.

## How to start a day

Open [_template/PROMPT.md](_template/PROMPT.md), copy the block, change the concept line, and paste it
into a new chat. Everything else is handled for you.

## Index

### Week 1 — Foundations · [`week-01-foundations/`](week-01-foundations/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 01 | How text becomes numbers: tokenization, embeddings, Word2Vec | [day-01-text-to-numbers](week-01-foundations/day-01-text-to-numbers/) | Done |
| 02 | Attention mechanism: from intuition to implementation | [day-02-attention-mechanism](week-01-foundations/day-02-attention-mechanism/) | Ready |
| 03 | Training paradigms: pretraining → fine-tuning → RLHF | [day-03-training-paradigms](week-01-foundations/day-03-training-paradigms/) | Ready |

### Week 2 — Context Windows + Prompting · [`week-02-context-and-prompting/`](week-02-context-and-prompting/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 04 | Context windows: why models forget, hallucinate, and hit token limits | [day-04-context-windows](week-02-context-and-prompting/day-04-context-windows/) | Done |
| 05 | Prompting techniques: zero-shot, few-shot, chain-of-thought, system prompts | [day-05-prompting-techniques](week-02-context-and-prompting/day-05-prompting-techniques/) | Done |
| 06 | Hands-on: 10 prompts for one task, techniques compared on cost + accuracy | [day-06-prompt-workbench](week-02-context-and-prompting/day-06-prompt-workbench/) | Done |

### Week 3 — Fine-Tuning · [`week-03-fine-tuning/`](week-03-fine-tuning/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 07 | Fine-tune vs RAG vs prompt: routing a capability to the right mechanism | [day-07-finetune-vs-rag-vs-prompt](week-03-fine-tuning/day-07-finetune-vs-rag-vs-prompt/) | Done |
| 08 | LoRA from scratch: the low-rank update, trained by hand in numpy | [day-08-lora-from-scratch](week-03-fine-tuning/day-08-lora-from-scratch/) | Done |
| 09 | LoRA on Hugging Face: peft + transformers, and the data-quality checklist | [day-09-lora-huggingface](week-03-fine-tuning/day-09-lora-huggingface/) | Done |

### Week 4 — Model Evaluation · [`week-04-model-evaluation/`](week-04-model-evaluation/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 10 | Benchmarks and their limits: mini-MMLU / mini-HumanEval, contamination, Goodhart | [day-10-benchmarks](week-04-model-evaluation/day-10-benchmarks/) | Done |
| 11 | Cost / latency / accuracy tradeoffs: Pareto frontier + a cascade router | [day-11-model-tradeoffs](week-04-model-evaluation/day-11-model-tradeoffs/) | Done |
| 12 | Model bake-off: same prompts vs 2–3 real models, cost/latency/accuracy table | [day-12-model-bakeoff](week-04-model-evaluation/day-12-model-bakeoff/) | Done |

### Week 5 — Embeddings & Vector Databases · [`week-05-embeddings-and-vector-dbs/`](week-05-embeddings-and-vector-dbs/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 13 | Semantic search from scratch: co-occurrence → SVD → cosine, BM25 vs dense, ANN | [day-13-semantic-search](week-05-embeddings-and-vector-dbs/day-13-semantic-search/) | Done |
| 14 | Vector databases: IVF + HNSW from scratch, pgvector vs Pinecone vs Weaviate | [day-14-vector-databases](week-05-embeddings-and-vector-dbs/day-14-vector-databases/) | Done |
| 15 | pgvector hands-on: vector SQL, indexes, filtered search, deploying on RDS | [day-15-pgvector-hands-on](week-05-embeddings-and-vector-dbs/day-15-pgvector-hands-on/) | Done |

### Week 6 — RAG · [`week-06-rag/`](week-06-rag/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 16 | RAG architecture end-to-end: chunk→embed→retrieve→augment→generate→cite | [day-16-rag-architecture](week-06-rag/day-16-rag-architecture/) | Done |
| 17 | Chunking strategies: fixed / sentence / recursive / semantic, measured | [day-17-chunking-strategies](week-06-rag/day-17-chunking-strategies/) | Done |
| 18 | Build a RAG pipeline: DuckDB + hybrid retrieval + Anthropic API + eval harness | [day-18-rag-pipeline](week-06-rag/day-18-rag-pipeline/) | Done |

### Week 7 — Agents & Orchestration · [`week-07-agents/`](week-07-agents/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 19 | Agent concepts: tools, the think→act→observe loop, and the guards it needs | [day-19-agent-concepts](week-07-agents/day-19-agent-concepts/) | Done |
| 20 | Frameworks: LangChain (LCEL) vs LlamaIndex (index→query engine), built small | [day-20-agent-frameworks](week-07-agents/day-20-agent-frameworks/) | Done |
| 21 | Build a simple agent: one tool, agentic RAG, Anthropic tool-use loop + eval | [day-21-agent-hands-on](week-07-agents/day-21-agent-hands-on/) | Done |

### Week 8 — APIs in Practice · [`week-08-apis-in-practice/`](week-08-apis-in-practice/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 22 | The Anthropic SDK in depth: request/response, stateless multi-turn, caching, errors | [day-22-sdk-deep-dive](week-08-apis-in-practice/day-22-sdk-deep-dive/) | Done |
| 23 | Function calling & structured outputs: the tool-use wire format, schema-valid JSON | [day-23-function-calling](week-08-apis-in-practice/day-23-function-calling/) | Done |
| 24 | Streaming: the SSE event protocol, accumulating text + tool JSON, a console streamer | [day-24-streaming](week-08-apis-in-practice/day-24-streaming/) | Done |

### Week 9 — Evals & Observability · [`week-09-evals-and-observability/`](week-09-evals-and-observability/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 25 | What makes a good eval: dimensions, reference-free metrics, LLM-judge + calibration | [day-25-good-evals](week-09-evals-and-observability/day-25-good-evals/) | Done |
| 26 | Build an eval harness: 14-case set, scoring functions, report, regression gate | [day-26-eval-harness](week-09-evals-and-observability/day-26-eval-harness/) | Done |
| 27 | Observability: build a tracer, instrument a pipeline, debug from a trace | [day-27-observability](week-09-evals-and-observability/day-27-observability/) | Done |

### Week 10 — Deployment · [`week-10-deployment/`](week-10-deployment/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 28 | AWS Bedrock: the converse API, inference profiles, pricing, Guardrails/KB/Agents | [day-28-aws-bedrock](week-10-deployment/day-28-aws-bedrock/) | Done |
| 29 | Serving & cost: prefill/decode, batching, KV cache, replica sizing, cost levers | [day-29-serving-and-cost](week-10-deployment/day-29-serving-and-cost/) | Done |
| 30 | Deploy the RAG pipeline: Lambda + API Gateway, cold starts, SAM template, auth | [day-30-deploy-rag-api](week-10-deployment/day-30-deploy-rag-api/) | Done |

### Week 11 — MLOps & MCP · [`week-11-mlops-and-mcp/`](week-11-mlops-and-mcp/)

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 31 | MCP: JSON-RPC from scratch, `FastMCP` + `ClientSession`, MCP→Anthropic tools, trust boundaries | [day-31-mcp](week-11-mlops-and-mcp/day-31-mcp/) | Done |
| 32 | Packaging & IaC: image layers/caching, a declarative plan/apply/drift engine, Terraform, secrets | [day-32-package-and-iac](week-11-mlops-and-mcp/day-32-package-and-iac/) | Done |
| 33 | CI/CD & eval-gated release: pipeline runner, eval gate vs baseline, GitHub Actions, canary + rollback | [day-33-cicd-and-release](week-11-mlops-and-mcp/day-33-cicd-and-release/) | Done |
| 34 | Monitoring, drift & the retraining loop: golden signals, PSI/KS, `RefreshTrigger`, the loop closed | [day-34-monitor-and-retrain](week-11-mlops-and-mcp/day-34-monitor-and-retrain/) | Done |

## Environment

All days share one uv-managed venv at the repo root. See [the root README](../README.md) for
first-time setup; after that it is just:

```bash
source .venv/bin/activate      # or  .venv\Scripts\activate  on Windows
```

Notebooks are pinned to the **Python (ai-upskill)** kernel. Each day also keeps a
`requirements.txt` listing what that specific lesson needs, but the packages themselves are
installed once into the shared venv from the root `requirements.txt`.
