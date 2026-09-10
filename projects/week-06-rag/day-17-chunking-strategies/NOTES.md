# Day 17 — Chunking strategies — cheat sheet

## The one-sentence version

Chunk size trades retrievability (small chunks embed precisely, but split facts) against
answerability (big chunks hold context, but embed as a topic blur) — measure recall@k / MRR on
a QA set for any chunking change.

## The strategies

| Strategy | How | Best for |
| -------- | --- | -------- |
| Fixed-size | every N chars/tokens | speed/predictability; needs overlap |
| Fixed + overlap | N chars, step N−overlap (~15%) | keeps boundary-straddling facts whole |
| Sentence packing | pack whole sentences up to a budget | prose; solid default |
| Paragraph / section | split on blank lines / headings | short structured sections |
| Recursive | biggest separator that fits: heading → blank → sentence → space, recurse | **clean structured docs — the pragmatic default** |
| Semantic | embed sentences, split where adjacent similarity drops | transcripts, scraped HTML, OCR |

Keep atomic units whole: a code function, a table row, a Q&A pair — don't split them.

## Overlap

Fixes: a fact split across a chunk boundary is intact in at least one chunk (toy: recall@3
0.86 → 0.95). Costs: more chunks to store/index, redundant text in every prompt.

## Metadata

Prepend the section heading / doc title to each chunk. Helps most at **small chunk sizes**
(a 150-char chunk gains the topical anchor it lacked) and hands the LLM the section name.

## Small-to-big (parent-document) retrieval

Retrieve against **small** precise chunks; pass the **parent** section to the LLM. Optimises
retrieval precision *and* answer context — at more prompt tokens.

## Chunk-size sweep

Sweep max size and plot recall@k + MRR — there's a sweet spot (often ~300–500 chars for
prose). Too small: fragmented facts, noisy embeddings. Too big: topic blur, imprecise match,
token cost.

## Method (non-negotiable)

Every chunking change → re-run recall@k on a real QA set before/after. "RAG got worse" is
almost always a retrieval-recall regression, and chunking is the usual cause.

## Code you will reuse

```python
def recursive_split(text, max_chars=400, seps=("\n## ", "\n\n", ". ", " ")):
    text = text.strip()
    if len(text) <= max_chars: return [text]
    sep = next((s for s in seps if s in text), None)
    ...  # split on `sep`, pack up to max_chars, recurse on oversized pieces
```

## What this does not cover

- The full pipeline + generation + eval — Day 18.
- Multi-vector / ColBERT-style late interaction — mentioned only.
- Document parsing (PDF/HTML → text) — out of scope.
