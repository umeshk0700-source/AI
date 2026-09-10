# Day 20 — Frameworks: LangChain vs LlamaIndex — cheat sheet

## The one-sentence version

LangChain = orchestration-first (`Runnable` + `|`, LangGraph for stateful agents, huge
integration catalog); LlamaIndex = retrieval-first (`Index` → `QueryEngine`, deep RAG
machinery); build v1 yourself and adopt a framework when you're reimplementing loaders,
integrations, or streaming.

## LangChain / LCEL

Every component is a `Runnable` with `.invoke()` (+ `stream`, `batch`, `ainvoke`). Compose
with `|`:

```python
chain = prompt | llm | parser          # output of each feeds the next
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | parser
```

- `RunnableParallel` — run branches on the same input, collect a dict.
- `RunnableBranch` — conditional routing.
- Agents: `create_tool_calling_agent` + `AgentExecutor(max_iterations=…)`; **LangGraph** for
  branching / state / human-in-the-loop / resumable runs (LangChain now points you there for
  non-trivial agents).
- Tracing: **LangSmith** (first-party).

## LlamaIndex

```python
docs  = SimpleDirectoryReader("kb/").load_data()       # 300+ connectors via LlamaHub
index = VectorStoreIndex.from_documents(docs)           # chunk + embed + store
qe    = index.as_query_engine(similarity_top_k=4)       # retrieve + prompt + synthesize + cite
resp  = qe.query("...")                                 # resp.response, resp.source_nodes
```

- `Document` → node parser (`SentenceSplitter`) → `Node`s → `Index`.
- Many index types (vector, tree, keyword, KG); response synthesizers (refine,
  tree-summarize, compact); advanced query engines (sub-question, router, multi-step).
- `index.as_retriever()` to use retrieval as a component elsewhere.

## Choosing

| Situation | Pick |
| --------- | ---- |
| RAG over docs, citations, swappable retrievers = most of the app | **LlamaIndex** |
| Agent with several tools, branching, approval steps | **LangGraph** (LangChain) |
| prompt→model→parse pipeline; want the integration catalog | **LangChain / LCEL** |
| Focused app, deps are a liability, you built the pieces | **roll your own** (Weeks 5–7) |
| Retrieval inside an agent | **compose** (LlamaIndex retriever as a LangGraph tool) |

## Costs a framework adds

Churning dependency tree (40–80 transitive deps for the LangChain+LlamaIndex set); an
abstraction to learn and debug *through*; opinions that fight non-standard use cases; slower
cold starts.

## Non-negotiable

Keep the **eval harness (Day 18 / Week 9) outside** the framework — so ground truth survives a
framework swap and the eval measures your task, not the framework.

## What this does not cover

- Actually installing and running LangChain/LlamaIndex (shown as reference snippets only).
- LangGraph state-machine details.
- A working agent against a real model — Day 21.
