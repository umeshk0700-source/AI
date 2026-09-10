# Day 08 — LoRA from scratch

Why full fine-tuning is expensive and how a low-rank adapter gets most of the benefit for
~1% of the trainable parameters — built and trained by hand in numpy, no ML framework.

## Learning objectives

By the end of the hour you should be able to:

1. Explain the ~16 bytes/parameter memory bill of full fine-tuning with Adam.
2. Write the LoRA update `W' = W + (alpha/r)·B·A` and implement its forward + backward pass.
3. Explain why `B` is initialised to zero and what `r` and `alpha` each control.
4. Read a rank sweep: below the intrinsic rank it underfits, above it wastes parameters.
5. Merge an adapter for zero-latency inference, swap adapters on a shared base, and explain
   why fewer trainable params overfit (and forget) less.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | What "fine-tuning" updates, and the memory bill | 5 min |
| 1 | A tiny pretrained model + a new task | 8 min |
| 2 | Full fine-tuning: train it, count the cost | 10 min |
| 3 | LoRA: the low-rank update, from scratch | 14 min |
| 4 | Rank sweep: quality vs parameters | 8 min |
| 5 | Merge, swap, and forgetting | 10 min |
| 6 | Exercises and self-check quiz | 5 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs fully offline in numpy — no GPU, no torch. Day 09 does the Hugging Face `peft` version.

## Run it

```bash
python -m jupyterlab projects/week-03-fine-tuning/day-08-lora-from-scratch/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models" (2021) — https://arxiv.org/abs/2106.09685
- Dettmers et al., "QLoRA: Efficient Finetuning of Quantized LLMs" (2023) — https://arxiv.org/abs/2305.14314
- Hugging Face PEFT docs — https://huggingface.co/docs/peft
- Aghajanyan et al., "Intrinsic Dimensionality Explains the Effectiveness of Fine-Tuning" — https://arxiv.org/abs/2012.13255

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib (base env).
