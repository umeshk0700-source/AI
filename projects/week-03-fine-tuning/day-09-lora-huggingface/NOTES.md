# Day 09 — LoRA on Hugging Face — cheat sheet

## The one-sentence version

`peft` wraps a frozen `transformers` model with LoRA `A`/`B` matrices on the `target_modules`
you name; you train those (~0.2% of params), then `merge_and_unload()` to ship — but the run
is only as good as the data, so run the six checks first.

## The minimal recipe

```python
from peft import LoraConfig, get_peft_model, TaskType
cfg = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16, lora_dropout=0.05,
                 target_modules=["c_attn"], bias="none")   # c_attn = distilgpt2 fused QKV
model = get_peft_model(base, cfg)
model.print_trainable_parameters()          # -> ~0.18%
# ... train A/B with any loop ...
model.save_pretrained("adapter")            # ~500 KB
merged = model.merge_and_unload()           # plain model, zero extra matmul
```

`lora_alpha / r` = effective update scale (16/8 = 2.0). Llama-style models: `target_modules =
["q_proj","k_proj","v_proj","o_proj"]`.

## The 6 data-quality checks (run BEFORE the GPU-hour)

| Check | One-line test | Why it ruins the run |
| ----- | ------------- | -------------------- |
| Duplicates | hash `(prompt, completion)` | over-weights repeats; inflates eval if cross-split |
| Train/test leakage | `test.prompt in train_prompts` | you measure memorisation, not generalisation |
| Format drift | regex-match completions to the template | model learns a blurry average of formats |
| Class/length imbalance | class counts + token-length histogram | rare classes under-learned; length ≈ category |
| Label noise | hand-check a random 50 | model faithfully learns the wrong labels |
| Prompt not masked | check `labels` has `-100` on prompt tokens | ~½ the gradient trains the wrong task |

Prompt masking:

```python
labels = input_ids.copy()
labels[:len(prompt_ids)] = [-100] * len(prompt_ids)   # loss ignores -100
```

## Numbers worth remembering

- distilgpt2 + LoRA r=8 on `c_attn`: 147 K trainable / 82 M total = 0.18%.
- Adapter on disk: ~500 KB. Full model: ~330 MB.
- CPU training: ~30 s for 8 epochs over 48 short examples.
- Colab: add `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")` → QLoRA.

## Gotchas

- `target_modules` names are architecture-specific — `c_attn` (GPT-2) ≠ `q_proj` (Llama).
- `B` is zero-init, so before training the PEFT model == base model exactly.
- 0.98 eval / 0.80 prod almost always = train/test leakage.
- Split the data *before* any augmentation, then dedupe across splits.

## What this does not cover

- Full RLHF / DPO preference tuning — see Day 03.
- Serving adapters at scale (routing, batched multi-adapter inference) — Week 10.
- Rigorous eval of the fine-tuned model — Weeks 4 & 9.
