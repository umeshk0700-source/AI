# Attention Mechanism — Cheat Sheet

## Core Intuition

**Problem:** RNNs process sequences step-by-step and forget earlier information.
**Solution:** Attention lets the model "look at everything at once" when making decisions.

## Key Components

### Basic Attention
```
attention_weights = softmax(similarity(query, all_keys))
output = weighted_sum(attention_weights, values)
```

### Self-Attention (Transformer)
- **Query (Q):** What am I looking for?
- **Key (K):** What information is available?
- **Value (V):** The actual information to use
- **Formula:** `Attention(Q,K,V) = softmax(QK^T/√d_k)V`

## Why It Works

1. **Parallel processing:** No sequential bottleneck
2. **Long-range dependencies:** Direct connections between any two positions  
3. **Selective focus:** Learns what to pay attention to
4. **Interpretability:** Attention weights show what the model is "looking at"

## Multi-Head Attention

- Multiple attention mechanisms running in parallel
- Each head can focus on different types of relationships
- Heads are concatenated and projected back to original dimension

## Common Patterns

- **Self-attention:** Keys, queries, values all come from same sequence
- **Cross-attention:** Queries from one sequence, keys/values from another
- **Masked attention:** Prevent looking at future tokens (during training)

## Scale Considerations

- Attention is O(n²) in sequence length
- Need techniques like sparse attention for very long sequences
- Typical transformer: 8-16 attention heads, 512-1024 dimensional embeddings

## Key Insight

Attention replaces the RNN's sequential "memory" with a learned "search" over the entire input.