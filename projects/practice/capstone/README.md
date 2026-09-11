# Capstone — one system, weeks 5–10

Everything from the second half of the course, wired into a single deployable service:

```
ingest (wk6)  ->  vector index (wk5)  ->  RAG + citations + faithfulness (wk6)
      ->  tool-using agent (wk7)  ->  gateway: cache + failover (wk8)
      ->  FastAPI: API key + rate limit (wk10)  ->  eval gate: LLM judge vs baseline (wk9)
```

You implement the `TODO`s in `src/ragplatform/`; `solution/` is the reference. Offline tests
use `llmlab.FakeLLM` and the local embedder, so `make test` is free. `make live` runs the
whole platform against real Claude and checks it passes its own eval gate.

## Usage

```bash
cd projects/practice/capstone
make setup
make test        # 13 offline tests
make solution    # same, against solution/
make live        # real end-to-end + eval gate  (~$0.15, per .env.preset)
make lab         # the walkthrough notebook
```

## What you implement

| Module | Piece | From week |
| ------ | ----- | --------- |
| `ingest.py` | `chunk_doc` — overlapping, citable chunks | 6 |
| `index.py` | `VectorIndex.add` / `.search` — cosine over an llmlab embedder | 5 |
| `rag.py` | `RAGPipeline.answer` / `.faithful` — grounded prompt, `[n]` citations, refusal | 6 |
| `agent.py` | `Agent.run` — the tool loop (`kb_search`, `calc`) with a step budget | 7 |
| `gateway.py` | `Gateway.chat` — cache hit/miss + failover to a second client | 8 |
| `evalgate.py` | `EvalGate.score` / `.check` — judge each case, compare to a baseline | 9 |
| `platform.py` | `RagPlatform` — wire all of the above together | — |
| `service.py` | `TokenBucket.allow`, `create_app` `/ask` — auth + 429 | 10 |

## Acceptance criteria

- `make test` green: chunks overlap and are ordered; the index retrieves the right doc; RAG
  cites and refuses out-of-scope; the agent returns a direct answer when no tool is called;
  the gateway caches, fails over, and re-raises without a fallback; the eval gate sets a
  baseline then blocks a regression; the service returns 401 without a key, 200 with one, and
  429 under the rate limit.
- `make solution` green.
- `make live` (with keys): the platform scores ≥ 0.6 on its own eval cases and refuses the
  out-of-scope question.

## Files

- `src/ragplatform/`, `solution/ragplatform/` — stubs / reference.
- `tests/` — offline suite + `test_live.py`.
- `fixtures/kb.py` — the policy KB + eval cases.
- `lab.ipynb` — build it up component by component, then serve it.
- `.env.preset` — model + `$0.15` cap (no secrets).
