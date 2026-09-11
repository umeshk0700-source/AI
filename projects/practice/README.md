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

## Setup (once, from the repo root)

```bash
source .venv/bin/activate
./scripts/setup-hooks.sh                     # pre-commit: blocks secrets, strips notebook outputs
pip install -e projects/practice/common       # makes `import llmlab` work everywhere
cp projects/practice/.env.example projects/practice/.env
$EDITOR projects/practice/.env                # add ANTHROPIC_API_KEY, OPENAI_API_KEY
```

## Working a lab

Every week has a `Makefile`:

```bash
cd projects/practice/week-02-support-triage
make setup        # install this lab's deps
make test         # offline unit tests — TODOs + failures on your WIP
make solution     # the same tests against solution/ (should be all green)
make live         # real Claude/GPT integration tests — costs a few cents, per .env.preset
make lab          # open the walkthrough notebook
```

Then implement the `TODO`s in `src/`, re-run `make test` until green. `solution/` is the
reference; `make solution` runs the suite against it.

## Cost & secret safety (set up by `scripts/setup-hooks.sh`)

- **Unit tests never call an API.** Live tests are opt-in (`-m live` + `LLM_LIVE=1`).
- Each week ships a committed **`.env.preset`** — model names + a spend cap tuned for that
  lab (no secrets). `make live` sources it; override per run:
  `LAB_USD_CAP=1 ANTHROPIC_MODEL=claude-sonnet-4-5 make live`.
- `llmlab.CostTracker` raises `BudgetExceeded` the moment a run crosses `LAB_USD_CAP`
  (default `$0.25`, lower in most presets).
- Your keys live only in `projects/practice/.env` — **gitignored**.
- The **pre-commit hook** refuses to commit `.env` files or anything that looks like a key
  (`sk-ant-…`, `AKIA…`, private-key blocks, …), and strips cell outputs from any
  `projects/practice/**/*.ipynb` (a live-run notebook embeds real API responses + fixture
  data — never committed). Lesson notebooks keep their outputs.

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
| 11 | platform-ops | Release gate + canary + drift monitor + refresh loop for the RAG service | Claude judge |

**[`capstone/`](capstone/)** — one system spanning weeks 5–10: ingest → vector index → RAG with
citations → tool-using agent → gateway (cache + failover) → FastAPI (auth + rate limit) → eval
gate. Same format (typed stubs + `solution/` + offline tests + a live end-to-end).
