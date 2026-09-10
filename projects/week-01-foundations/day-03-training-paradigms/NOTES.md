# Training Paradigms — Cheat Sheet

## The Three-Stage Pipeline

### 1. Pretraining (Foundation)
- **Goal:** Learn language patterns and world knowledge
- **Data:** Massive unlabeled text (trillions of tokens)
- **Task:** Predict next word (causal language modeling)
- **Duration:** Weeks/months with massive compute
- **Output:** Foundation model with broad capabilities

### 2. Fine-tuning (Specialization)  
- **Goal:** Adapt to specific tasks or domains
- **Data:** Smaller labeled datasets (thousands to millions)
- **Task:** Specific objectives (classification, QA, summarization)
- **Duration:** Hours to days
- **Output:** Task-specific model

### 3. RLHF (Alignment)
- **Goal:** Align with human preferences and values
- **Data:** Human rankings/feedback on outputs
- **Task:** Maximize reward based on human preferences  
- **Duration:** Days to weeks
- **Output:** Aligned, deployable model

## Key Insights

### Why This Order?
1. **Pretraining first:** Builds foundational language understanding
2. **Fine-tuning second:** Specializes to desired behavior
3. **RLHF last:** Aligns with human values and safety

### Data Requirements
- **Pretraining:** ~100B-1T tokens of text
- **Fine-tuning:** ~10K-1M examples  
- **RLHF:** ~10K-100K preference pairs

### Computational Costs
- **Pretraining:** $1M-$100M+ in compute
- **Fine-tuning:** $1K-$100K in compute
- **RLHF:** $10K-$1M in compute

## Common Patterns

### Transfer Learning Magic
- Pretrained models learn generalizable representations
- Small amounts of task-specific data can achieve high performance
- Cross-domain knowledge transfer

### Emergence
- Capabilities appear suddenly at certain scales
- In-context learning emerges around 1B+ parameters
- Chain-of-thought reasoning emerges around 10B+ parameters

### Alignment Challenges
- Models can be capable but misaligned
- Human feedback helps but isn't perfect
- Ongoing research area for AI safety

## Practical Takeaways

- **For most applications:** Use existing pretrained models + fine-tuning
- **For specialized domains:** Additional domain pretraining may help
- **For deployment:** RLHF or similar alignment techniques are essential
- **For research:** Understanding scaling laws and emergence patterns