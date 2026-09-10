# Week 1 Lab — The front end of a language model

The only lab with **no API calls** — it's about the internals every later lab takes for
granted. You implement, in numpy:

- `BPETokenizer` — learn a subword vocabulary, encode/decode.
- `EmbeddingTable` — id → dense vector, nearest neighbours.
- `SelfAttention` — scaled dot-product attention with an optional causal mask.

## Format

This lab is two notebooks (not a package, since there's nothing to wire up):

- `lab.ipynb` — skeleton with `raise NotImplementedError` + `# TODO`, and a **TEST SCOREBOARD**
  cell at the bottom that prints `TODO` / `FAIL` / `PASS` per check.
- `solution.ipynb` — the same notebook, filled in, all green.

## Work it

```bash
source ../../../.venv/bin/activate
jupyter lab lab.ipynb
```

Run top to bottom → all `TODO`. Implement one method, re-run its cell + the scoreboard, repeat
until `ALL GREEN 🎉`.

Covers Day 01 (tokenization, embeddings) and Day 02 (attention).
