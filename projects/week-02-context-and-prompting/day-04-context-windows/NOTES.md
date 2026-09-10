# Day 04 — Context Windows — cheat sheet

One page. Read this instead of the whole notebook when you come back in a week.

## The one-sentence version

The model sees a fixed-length window of tokens; "forgetting" is the runtime truncating that
window, and "hallucination" is the softmax being forced to emit *something* even when the
answer was never in the window or the training data.

## Key ideas

| Idea | What it means | Why it matters |
| ---- | ------------- | -------------- |
| Context window | Fixed max number of token slots, set at training time | You can't raise it with a parameter; you must shorten input or switch models |
| Quadratic attention | Every token attends to every token → `O(n²)` compute, `O(n²)` score memory | Doubling context ≈ 4× the read cost; this is *why* the limit exists |
| KV cache | Each kept token stores K+V vectors in every layer → `O(n)` GPU memory | Ongoing cost of a long chat; why long context is priced higher |
| Truncation | Runtime drops tokens when the chat exceeds the window | This *is* "the model forgot"; choose drop-oldest vs keep-system+pin |
| Positional encoding | Order is *added* to tokens; weights only trained up to length L | Feeding 4× the trained length → degraded/incoherent output |
| Softmax always answers | Final layer is a distribution over the whole vocab, no "null" | Fabrication is the default; "I don't know" is a *learned* behavior (RLHF) |
| Lost in the middle | Facts at the start/end of context are used; middle is often ignored | Put the question + key context first or last, not buried |

## Numbers worth remembering

- Double the context → attention time ~4×, score-matrix memory exactly 4×, KV cache 2×.
- One 100k×100k fp32 attention score matrix = 40 GB (per head, per layer, unoptimized).
- Rule-of-thumb data: pretraining ~1e12 tokens, fine-tuning ~1e4–1e6 examples.
- Budget a prompt: `usable = window − system_prompt − answer_reserve`.

## Code you will reuse

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
ntok = lambda s: len(enc.encode(s))          # count tokens before you send

def budget(W, sys_tokens, answer_reserve):    # tokens left for history + retrieved docs
    return W - sys_tokens - answer_reserve
```

## Gotchas

- Lowering temperature to 0 does **not** stop hallucination — it just makes the model emit its
  single most-probable token, fabrication included, deterministically.
- "The model forgot" is almost never a model problem; check what the runtime actually sent.
- A compaction summary is lossy by design: you trade perfect raw recall for fitting the window.
- Position matters even when the fact *is* in the window (lost-in-the-middle).

## What this does not cover

- Actual attention implementations (FlashAttention, sparse/linear attention) — mechanism only.
- Embeddings and retrieval as the real fix for "my data doesn't fit" — Weeks 5–6.
- RLHF, which is *how* models learn to say "I don't know" — Day 03.
