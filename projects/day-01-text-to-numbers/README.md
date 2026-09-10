# Day 01 — How text becomes numbers

A model never sees the word "cat". It sees an integer, which it uses to look up a row of floats.
This hour is about that conversion: how text is split into tokens, why tokens are odd-looking
fragments rather than words, and how those tokens turn into vectors that carry meaning.

You will build a byte-pair tokenizer and train Word2Vec from scratch in numpy. No black boxes.

## Learning objectives

By the end of the hour you should be able to:

1. Explain why one-hot encoding is useless for meaning, and prove it with a cosine similarity of exactly 0.
2. Predict roughly how a string will be tokenized, and explain why `"strawberry"` is 3 tokens but `" strawberry"` is 1.
3. Implement byte-pair encoding yourself: learn a merge table from a corpus and apply it to unseen text.
4. Explain the embedding matrix as a one-hot matrix multiply, and compute how many parameters it costs.
5. Derive skip-gram with negative sampling and train it in numpy until analogy arithmetic works.
6. Say precisely why Word2Vec is not enough for a modern LLM, and what replaced it.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Why numbers at all — the `ord()` baseline and its emptiness | 3 min |
| 1 | One-hot encoding, and watching it fail numerically | 8 min |
| 2 | Tokenization for real, hands-on with `tiktoken` | 12 min |
| 3 | Implement byte-pair encoding from scratch | 10 min |
| 4 | Token IDs to vectors: the embedding matrix | 5 min |
| 5 | Word2Vec from scratch: skip-gram, negative sampling, training | 15 min |
| 6 | Why Word2Vec is not enough: context and order | 7 min |
| 7 | Six exercises with solutions, plus a self-check quiz | — |

## Setup

Everything runs in the shared uv venv at the repo root. If you have not created it yet, follow
[the root README](../../README.md), then from the repo root:

```powershell
.venv\Scripts\activate
```

This lesson needs `numpy`, `matplotlib` and `tiktoken`, all already in the root `requirements.txt`.

`tiktoken` downloads its vocabulary files from `openaipublic.blob.core.windows.net` the first time
you use each encoding, so the first cell in segment 2 needs a network connection. After that they
are cached on disk.

## Run it

```powershell
python -m jupyterlab projects\day-01-text-to-numbers\lesson.ipynb
```

The notebook is pinned to the **Python (ai-upskill)** kernel, which is the venv. If the kernel
picker shows anything else, switch it back or the imports will fail.

The notebook ships with all outputs populated, so you can read it start to finish first. To work
through it properly, use Kernel > Restart Kernel and Run All Cells and go segment by segment.

Segment 5 trains a real model. It takes a few seconds, not minutes.

## Source material

- [The Illustrated Word2Vec](https://jalammar.github.io/illustrated-word2vec/) — Jay Alammar. Read
  this alongside segment 5; the notebook deliberately follows its structure and builds the model it
  describes.
- [tiktoken](https://github.com/openai/tiktoken) — the tokenizer used in segments 2 and 4.
- [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781) —
  Mikolov et al. 2013, the original Word2Vec paper, if you want the source.
- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) —
  Sennrich et al. 2015, which brought BPE to NLP.

## Files

- `lesson.ipynb` — the guided lesson. Everything happens here.
- `NOTES.md` — one-page cheat sheet. Read this in a week instead of the whole notebook.
- `requirements.txt` — what this lesson needs.
