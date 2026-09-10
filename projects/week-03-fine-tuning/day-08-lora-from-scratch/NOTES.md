# Day 08 — LoRA from scratch — cheat sheet

## The one-sentence version

Freeze the pretrained weights and learn the *update* as a skinny product `ΔW = (alpha/r)·B·A`
— a few hundred KB of trainable parameters instead of gigabytes, because the update a related
task needs is intrinsically low-rank.

## The equation

```
W' = W + (alpha / r) * B @ A
     A : (r, d_in)   trained,  init small random
     B : (d_out, r)  trained,  init ZERO  -> adapter is a no-op at step 0
     W : (d_out, d_in) FROZEN
     r : rank, tiny (8/16/32/64 in practice)
     alpha : fixed scale constant (often alpha = r, or 2r)
```

Trainable params per adapted matrix: `r * (d_in + d_out)` instead of `d_in * d_out`.

## The memory bill

| Buffer (full FT, Adam mixed precision) | bytes/param |
| --- | --- |
| fp16 weights | 2 |
| fp16 grads | 2 |
| fp32 Adam m | 4 |
| fp32 Adam v | 4 |
| fp32 master weights | 4 |
| **total** | **~16** |

7B full FT ≈ 112 GB of optimizer+weight state → won't fit one 80 GB GPU. LoRA applies the 16×
only to the adapter (~0.1–1% of params).

## Knobs

- **r too small** (< intrinsic rank): underfits, loss plateaus high.
- **r at/above intrinsic rank**: same quality; extra rank = wasted params.
- **alpha**: sets update magnitude via `alpha/r`. Too small → slow; too large → unstable.
  Double r → usually double alpha to hold the scale.
- **target modules**: which matrices get adapters (commonly `q_proj`, `v_proj`; sometimes all
  linear layers).
- **B = 0 init**: guarantees the model starts exactly equal to the pretrained checkpoint.

## Merge / swap / forget

- **Merge:** `W += (alpha/r)·B·A` once → zero extra inference latency, same shape.
- **Swap:** one shared frozen base + many small adapters (MBs each) → serve dozens of
  fine-tunes from one GPU. 40 full fine-tunes of a 13B = ~1 TB; 40 LoRA adapters ≈ 1 GB.
- **Forget less:** far fewer trainable params can't memorise noise / overwrite pretrained
  features; and the adapter is reversible (drop it, base is bit-for-bit back).

## PEFT family

LoRA, **QLoRA** (LoRA on a 4-bit-quantized base — fits 65B on one 24–48 GB GPU), prefix/prompt
tuning, adapters, IA³. LoRA and QLoRA dominate in practice.

## Numbers worth remembering

- LoRA trainable fraction: typically 0.05–1% of model params.
- QLoRA base memory: ~1/4 (int8) to ~1/8 (int4) of fp16, adapter stays fp16.
- Adapter checkpoint: MBs, vs the full model's GBs.

## What this does not cover

- The Hugging Face `peft` API and a real GPU run — Day 09.
- Data quality for fine-tuning runs — Day 09.
- Serving infrastructure (adapter routing, batching) — Week 10.
