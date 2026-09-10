# Day 05 — Prompting Techniques — cheat sheet

## The one-sentence version

Every prompting technique is the same move — add tokens that make the answer you want the most
probable continuation; they differ only in *what* tokens they add (an instruction, examples, a
reasoning scaffold, a standing rule block).

## Key ideas

| Idea | What it means | Why it matters |
| ---- | ------------- | -------------- |
| Prompt = conditioning | Model predicts next token from patterns; "following instructions" is learned behaviour | Explains why format, examples, and phrasing matter so much |
| Message → one sequence | system/user/assistant get flattened into one delimited token string | The system prompt is just early text; its influence decays with length |
| Zero-shot | Instruction only, no examples | Fine for common tasks + simple output; falls back to generic priors |
| Few-shot | k input→output pairs in the prompt | Teaches *format & label boundaries*, not new facts/skills; costs tokens |
| Dynamic few-shot | Retrieve examples similar to the query | Beats a fixed example set; = kNN over embeddings |
| Chain-of-thought | Model writes intermediate steps before the answer | Converts a depth problem into a length problem; more tokens = more compute |
| Self-consistency | Sample N CoT traces, majority-vote the answer | Trades compute for accuracy on noisy reasoning |
| System prompt | Earliest, most stable conditioning: persona, tone, format, rules | Not enough for missing knowledge (→RAG) or behaviour-at-scale (→fine-tune) |

## Numbers worth remembering

- Few-shot prompt ≈ 2–5× the tokens of the zero-shot version (each example + delimiters).
- Zero-shot CoT trigger: literally append **"Let's think step by step."**
- Prompting reliability plateaus ~95–99%; the failing tail needs fine-tune + constrained decoding.
- System-prompt influence ~`0.92^turns`; drops below 0.25 after ~17 turns (illustrative).

## Code you will reuse

```python
def build_few_shot_prompt(examples, query):
    lines = ["<instruction>\n"]
    for t, y in examples:            # keep EVERY example's format identical to the output you want
        lines.append(f"Review: {t}\nLabel: {y}\n")
    lines.append(f"Review: {query}\nLabel:")
    return "\n".join(lines)
```

## Gotchas

- Inconsistent formatting across few-shot examples → inconsistent output. Pick one template.
- CoT is overhead (or harmful) on easy tasks and under tight token budgets.
- Lower temperature ≠ more correct (Day 04); CoT ≠ always better.
- Long chats drift from the system prompt — restate hard rules, or enforce with validation/tools.

## What this does not cover

- Fine-tuning mechanics (LoRA/PEFT) — Week 3.
- RAG — Weeks 5–6.
- Measuring which technique actually won — Week 4 (evaluation).
