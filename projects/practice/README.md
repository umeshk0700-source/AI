# Practice Labs — corporate-grade builds

One hands-on lab per week. Each is a small real repo: a **corporate use case**, a typed
object-oriented skeleton with `TODO`s, a **pytest** suite (offline unit tests + opt-in live
integration tests against **real Claude / GPT APIs**), fixtures, a `lab.ipynb` walkthrough,
and a fully-implemented `solution/`.

The lessons (`projects/week-*/day-*/`) teach the concept from scratch. These labs make you
build the production version.

## Layout

```
projects/practice/
  common/                      # llmlab — the shared toolkit (installed, not stubbed)
    llmlab/
      client.py                #   get_client("anthropic"|"openai") — retries, cost, tracing
      embeddings.py            #   get_embedder("openai"|"voyage"|"local")
      cost.py                  #   CostTracker, pricing, a hard per-run $ cap
      trace.py                 #   span() / @traced — pipeline observability
      testing.py               #   live() marker, load_jsonl(), judge()
  .env.example
  week-01-foundations/         # the "how it works" lab (numpy internals — no API)
  week-02-support-triage/      # ... weeks 2–10: corporate scenarios, real API calls
  ...
```

## Setup (once)

```bash
source ../../.venv/bin/activate
pip install -e common                       # makes `import llmlab` work everywhere
cp .env.example .env && $EDITOR .env         # add ANTHROPIC_API_KEY, OPENAI_API_KEY
```

## Working a lab

```bash
cd week-02-support-triage
pip install -r requirements.txt
pytest -q                                    # offline unit tests — should pass on the solution,
                                             # show failures/todos on your work-in-progress
LLM_LIVE=1 pytest -q -m live                  # the real-API integration tests (costs ~$0.25)
jupyter lab lab.ipynb                         # guided walkthrough
```

Then implement the `TODO`s in `src/`. Re-run `pytest` until green. Compare with `solution/`
only when stuck.

## Cost control

- Unit tests never call an API.
- Live tests default to the cheapest models (`claude-haiku-4-5`, `gpt-4o-mini`) and small
  fixture sets — a full live run per lab is a few cents, `LAB_USD_CAP=0.25` by default.
- `CostTracker` raises `BudgetExceeded` if a run crosses the cap. Raise it in `.env` when you
  want a bigger eval.

## Lab index

| Week | Lab | Use case | Real APIs used |
| ---- | --- | -------- | -------------- |
| 1 | foundations | Build a tokenizer + embedding table + attention (internals) | none |
| 2 | support-triage | Classify / route / draft-reply for inbound support tickets | Claude, GPT |
| 3 | domain-adaptation | Prompt vs RAG vs LoRA decision + a real LoRA fine-tune | Claude + local HF |
| 4 | model-selection | Same extraction task across 4 models → a selection memo | Claude, GPT |
| 5 | kb-search | Embeddings + vector index + hybrid retrieval over a KB | OpenAI embeddings |
| 6 | policy-assistant | Production RAG with citations + faithfulness eval | Claude, OpenAI embed |
| 7 | ops-agent | Tool-using agent with guards + human approval | Claude tool use |
| 8 | llm-gateway | Resilient multi-provider gateway: retries, cache, failover, streaming | Claude, GPT |
| 9 | quality-platform | Eval harness (LLM-as-judge) + tracing + a CI regression gate | Claude judge |
| 10 | ship-it | Wrap the RAG service as an API: FastAPI, auth, limits, load test | Claude |
