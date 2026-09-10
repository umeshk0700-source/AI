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

## Usage

```bash
cd projects/practice/week-01-foundations
make lab          # open lab.ipynb, implement the TODOs, watch the scoreboard go green
make solution     # open the filled reference notebook
```

No API keys, no cost — this lab is pure numpy.

