# Day 09 — LoRA on Hugging Face (hands-on)

Day 08's numpy LoRA, now in the real `peft` + `transformers` stack: fine-tune `distilgpt2`
(runs on CPU in ~30s) to a house reply format, plus the six data-quality checks every tutorial
skips. Ends with the exact Colab-GPU / QLoRA version for a real model.

## Learning objectives

By the end of the hour you should be able to:

1. Map `LoraConfig` fields (`r`, `lora_alpha`, `target_modules`) to the Day 08 mechanics.
2. Run the pre-flight data checklist: duplicates, train/test leakage, format drift, imbalance,
   label noise, prompt-token masking — with a one-line test and a fix for each.
3. Train a LoRA adapter with a plain PyTorch loop and read the loss curve.
4. Generate with the adapter, `merge_and_unload()` for zero-latency inference, save the
   ~500 KB adapter, and swap adapters on a shared base.
5. Adapt the run to a Colab T4 with QLoRA (4-bit base) and architecture-correct target modules.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Setup + the base model's baseline behaviour | 6 min |
| 1 | Build the fine-tuning dataset | 8 min |
| 2 | Data quality: the 6 checks that ruin a run | 15 min |
| 3 | `LoraConfig` + `get_peft_model`: inspect the adapter | 10 min |
| 4 | Train the adapter, watch the loss | 12 min |
| 5 | Generate, merge, save, swap | 6 min |
| 6 | Colab GPU version + exercises + quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Needs `torch`, `transformers`, `peft`, `datasets`, `accelerate` (already installed in the
shared venv; also in the root `requirements.txt`). First run downloads `distilgpt2` (~350 MB)
from the Hugging Face Hub — needs network once, then cached.

## Run it

```bash
python -m jupyterlab projects/week-03-fine-tuning/day-09-lora-huggingface/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated. Training runs on
CPU; no GPU required.

## Source material

- Hugging Face PEFT — LoRA guide — https://huggingface.co/docs/peft/task_guides/lora_based_methods
- Hugging Face, "Fine-tune a language model" course chapter — https://huggingface.co/learn/nlp-course/chapter7/6
- `trl` SFTTrainer docs — https://huggingface.co/docs/trl/sft_trainer
- Dettmers et al., QLoRA — https://arxiv.org/abs/2305.14314

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — torch, transformers, peft, datasets, accelerate, matplotlib.
- `cirrus_adapter/` — the saved LoRA adapter produced by the notebook (~600 KB).
