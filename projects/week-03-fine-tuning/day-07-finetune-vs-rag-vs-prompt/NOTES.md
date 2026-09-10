# Day 07 — Fine-tune vs RAG vs Prompt — cheat sheet

## The one-sentence version

Prompt = working memory (this call only), RAG = an open book on the desk (looked up per call),
fine-tune = what was learned in school (in the weights) — knowledge goes in RAG, behaviour goes
in the weights, and most real systems use all three.

## The five axes

| Axis | Prompt | RAG | Fine-tune |
| ---- | ------ | --- | --------- |
| Accuracy on *knowledge* | low (generic) | high, if retrieval hits | high, but frozen at train time |
| Accuracy on *behaviour/format* | medium | medium (still needs prompt) | high, consistent |
| Cost per call | high (big context) | medium (retrieved chunk) | low (short prompt) |
| Latency | low | +retrieval step | lowest |
| Freshness | edit prompt | edit KB + re-embed | **retrain** |
| Build effort | minutes | ~hours | days + labeled data + infra |

## Decision rules

1. **Always start with prompt engineering** — free to try, often enough.
2. **RAG when the missing thing is knowledge that's large or changing** — docs, policies,
   per-user data, anything you'd cite.
3. **Fine-tune when the missing thing is behaviour/skill/format** that must hold across many
   calls AND prompt+RAG have plateaued below your bar AND you have training data AND volume
   justifies the fixed cost.
4. **They compose:** fine-tune the voice + tool-use, RAG the facts, keep a thin prompt.
5. **Never fine-tune on facts that change weekly** — you'll retrain forever.

## Numbers worth remembering

- RAG accuracy ≤ retrieval accuracy — always. (top-1 → top-3 can jump a toy task 0.5 → 1.0.)
- Fine-tune = high fixed cost ($ eng + training + eval), low marginal cost (short prompts).
  Prompt/RAG = ~0 fixed, higher per-call. Crossover is a volume question.

## Signs you picked wrong

- Every policy change triggers a training run → those facts belonged in RAG.
- 30-example few-shot block on every call, huge bill, still inconsistent → behaviour belonged
  in the weights.
- RAG retrieves fine but tone/format is all over the place → add fine-tune or a firmer system
  prompt for style.
- "We fine-tuned on our catalog and prices are stale" → prices are fast facts; move to RAG / a
  live lookup.

## What this does not cover

- LoRA/PEFT mechanics — Day 08.
- Real embeddings, chunking, vector DBs — Weeks 5–6.
- Measuring the plateau rigorously — Weeks 4 & 9.
