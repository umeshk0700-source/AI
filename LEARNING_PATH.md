# Learning paths

The course is 34 lessons in 11 weeks + 11 practice labs + 1 capstone. You don't have to do all
of it, and you shouldn't do it in a straight line the first time. Pick a track.

Each lesson is ~60 min. Each practice lab is 3–6 h of real work. The capstone is a weekend.

---

## The one-week track (~8 h) — "I need to be useful on an LLM feature by Friday"

The minimum that lets you design, build, and evaluate a real feature.

| Day | Lesson | Why it's in the short list |
| --- | --- | --- |
| 1 | [04 — Context windows](projects/week-02-context-and-prompting/day-04-context-windows/) | Every failure mode downstream is a context-budget problem |
| 2 | [05 — Prompting techniques](projects/week-02-context-and-prompting/day-05-prompting-techniques/) | Zero/few-shot/CoT — the cheapest lever, learn it first |
| 3 | [07 — Fine-tune vs RAG vs prompt](projects/week-03-fine-tuning/day-07-finetune-vs-rag-vs-prompt/) | The decision that shapes the whole architecture |
| 4 | [16 — RAG architecture](projects/week-06-rag/day-16-rag-architecture/) | The default architecture for "answer from our docs" |
| 5 | [19 — Agent concepts](projects/week-07-agents/day-19-agent-concepts/) | The tool loop + guards — when you need more than RAG |
| 6 | [22 — The Anthropic SDK](projects/week-08-apis-in-practice/day-22-sdk-deep-dive/) + [23 — Function calling](projects/week-08-apis-in-practice/day-23-function-calling/) | How you actually call the model in code |
| 7 | [25 — What makes a good eval](projects/week-09-evals-and-observability/day-25-good-evals/) | Without this you're shipping vibes |

Then do **[practice lab week 6 (policy-assistant)](projects/practice/week-06-policy-assistant/)** —
a production RAG service with citations and a faithfulness eval. That single lab exercises most
of what the week taught.

---

## The core track (~14 lessons + all 11 labs, ~2–3 weeks part-time) — recommended

Enough theory to make good decisions; most of the time in the labs, where the real learning is.

**Lessons** (in this order):

1. [01 — How text becomes numbers](projects/week-01-foundations/day-01-text-to-numbers/)
2. [02 — Attention](projects/week-01-foundations/day-02-attention-mechanism/)
3. [04 — Context windows](projects/week-02-context-and-prompting/day-04-context-windows/)
4. [05 — Prompting techniques](projects/week-02-context-and-prompting/day-05-prompting-techniques/)
5. [07 — Fine-tune vs RAG vs prompt](projects/week-03-fine-tuning/day-07-finetune-vs-rag-vs-prompt/)
6. [10 — Benchmarks and their limits](projects/week-04-model-evaluation/day-10-benchmarks/)
7. [11 — Cost / latency / accuracy tradeoffs](projects/week-04-model-evaluation/day-11-model-tradeoffs/)
8. [13 — Semantic search from scratch](projects/week-05-embeddings-and-vector-dbs/day-13-semantic-search/)
9. [16 — RAG architecture](projects/week-06-rag/day-16-rag-architecture/)
10. [19 — Agent concepts](projects/week-07-agents/day-19-agent-concepts/)
11. [22 — The Anthropic SDK](projects/week-08-apis-in-practice/day-22-sdk-deep-dive/)
12. [25 — What makes a good eval](projects/week-09-evals-and-observability/day-25-good-evals/)
13. [31 — MCP](projects/week-11-mlops-and-mcp/day-31-mcp/) — how agents get their tools in practice
14. [33 — CI/CD & eval-gated release](projects/week-11-mlops-and-mcp/day-33-cicd-and-release/) — how a change reaches prod safely

**Labs**: all 11, [week 1](projects/practice/week-01-foundations/) → [week 11](projects/practice/week-11-platform-ops/),
one per theme. Do the lab for a week right after that week's lesson above.

**Then**: the [capstone](projects/practice/capstone/) — it ties weeks 5–10 into one system.

---

## The full track (all 34 lessons + 11 labs + capstone, ~7–9 weeks part-time)

Do it in order, one lesson per day. Weeks 1–10: 2 concept lessons + 1 hands-on lesson + the
practice lab. Week 11 (MLOps & MCP) is 4 lessons — [31 MCP](projects/week-11-mlops-and-mcp/day-31-mcp/),
[32 packaging & IaC](projects/week-11-mlops-and-mcp/day-32-package-and-iac/),
[33 CI/CD & eval-gated release](projects/week-11-mlops-and-mcp/day-33-cicd-and-release/),
[34 monitoring, drift & the refresh loop](projects/week-11-mlops-and-mcp/day-34-monitor-and-retrain/) —
plus the [platform-ops lab](projects/practice/week-11-platform-ops/). The `*-hands-on` /
`*-workbench` / `*-bakeoff` lessons (06, 09, 12, 15, 18, 21, 26, 34) are the pivot from
"understand it" to "build it" — don't skip them even if the concept days felt easy.

Full lesson index: [projects/README.md](projects/README.md).
Full lab index: [projects/practice/README.md](projects/practice/README.md).

---

## Notes on how to actually do it

- **Attempt the exercises before opening `solutions/`.** Every lesson now keeps the exercise
  prompts and quiz questions in `lesson.ipynb`; the worked solutions and the answer key are in
  a sibling `solutions/solutions.ipynb`. The value is in the failed first attempt.
- **The labs cost money** (real Claude / GPT calls) but only when you run `make live` — the
  offline `make test` suite is free and is most of the work. Presets cap spend per lab; see
  [projects/practice/README.md](projects/practice/README.md).
- **If you only remember one thing per week**, make it the interview-question list at the end
  of each week's lessons — that's the "did it stick" check.
