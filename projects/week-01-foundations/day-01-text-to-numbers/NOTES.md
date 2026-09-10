# Day 01 — How text becomes numbers — cheat sheet

One page. Read this in a week instead of the whole notebook.

## The one-sentence version

Text is chopped into subword tokens by a merge table learned from data, each token is an integer,
each integer indexes a row of a learned matrix, and those rows arrange themselves so that geometric
relationships encode semantic ones.

## The pipeline

```
"the cat sat"  ->  [1820, 8415, 7731]  ->  [[0.21, -0.04, ...], ...]  ->  model
     text            token IDs                  dense vectors
                   BPE tokenizer            embedding table lookup
```

## Key ideas

| Idea | What it means | Why it matters |
| ---- | ------------- | -------------- |
| `ord()` encoding | Numbers straight from character codes | Reversible but meaningless: distance measures spelling, so `cat`-`car` is 2 and `cat`-`dog` is 19 |
| One-hot | All zeros with a single 1 | Any two distinct words have cosine similarity **exactly 0**, so no similarity and no generalisation |
| Subword / BPE | Merge the most frequent adjacent pair, repeatedly | Common words stay whole, rare words split into known fragments, nothing is ever out-of-vocabulary |
| Merge table | The ordered list of merge rules learned from the corpus | This *is* the trained tokenizer; encoding = replay the merges in order |
| Byte-level | Base symbols are the 256 byte values | Why no `<UNK>` token is ever needed |
| Embedding matrix | `(vocab_size, d_model)` of learned floats | `E[idx]` is exactly `one_hot(idx) @ E`, just never computed that way |
| Distributional hypothesis | "You shall know a word by the company it keeps" | Raw text supplies free supervision — no labels needed |
| Skip-gram | Predict context words from the centre word | Turns any corpus into `(centre, context)` training pairs |
| Negative sampling | "Is this pair real or noise?" instead of a softmax over the vocab | Cuts ~100,277 dot products per pair down to `k+1`; the trick that made Word2Vec practical |
| Static vs contextual | Word2Vec gives one vector per word, forever | `bank` (river) and `bank` (money) get the identical row; attention is what fixes this |

## Numbers worth remembering

- **1 token is roughly 0.75 English words** (~1.3 tokens/word). Use 1.3 for planning.
- Vocabulary sizes: `r50k_base` 50,257 (GPT-2/3), `cl100k_base` 100,277 (GPT-3.5/4), `o200k_base` 200,019 (GPT-4o).
- Embedding table at `d_model=768`: 38.6M params for 50k vocab, 77.0M for 100k, 153.6M for 200k.
- **~31%** of GPT-2 small's 124M parameters is just the embedding table.
- One-hot for a 1,000-token prompt at 100k vocab = **401 MB**, versus 3.1 MB dense. 99.999% zeros.
- The token tax: `नमस्ते दुनिया` costs **23** tokens in `r50k_base`, **13** in `cl100k_base`, **5** in `o200k_base`. English stayed at 9 throughout.

## Gotchas

- **The space is part of the token.** `"strawberry"` is 3 tokens (`str`+`aw`+`berry`) but
  `" strawberry"` is 1. A trailing space in a prompt changes everything after it.
- **Digit runs are capped at 3 characters by the pre-tokenizer regex**, so *no* year from 1900-2050
  is a single token. `2024` is `202`+`4`. Place value never lines up between operands, which is a
  large part of why LLMs are unreliable at arithmetic.
- **Letter counting is hard from the inside.** The model sees `str|aw|berry`, not ten letters.
- **A token can be half a character.** An emoji is several tokens, and the first one is not valid
  UTF-8 on its own — hence broken glyphs in streaming output.
- **Word2Vec keeps `W_in` and throws `W_out` away.** Two matrices exist so a word is not scored
  against itself.
- **Loss plateaus above zero and that is correct.** Some sampled negatives really are plausible
  context words.

## Code worth muscle memory

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

len(enc.encode(text))                                  # count tokens before an API call
[enc.decode_single_token_bytes(i) for i in enc.encode(text)]   # see the actual pieces

def cosine(a, b):
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
```

The whole gradient of skip-gram with negative sampling, for a centre vector `v` and candidate
rows `u` with labels `y`:

```python
grad = sigmoid(u @ v) - y      # that is the entire derivative
W_in[centre]  -= alpha * (grad @ u)
W_out[targets] -= alpha * np.outer(grad, v)
```

## What this does not cover

- **Contextual embeddings.** One vector per word cannot separate `bank` from `bank`. Self-attention
  is the fix, and is the natural Day 02.
- **Positional encoding.** `dog bites man` and `man bites dog` are the same bag of tokens, so
  position has to be added before the first layer.
- **Sentence embeddings and retrieval / RAG.** Same cosine geometry, applied to whole documents.
