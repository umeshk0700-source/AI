# Day 02 — Attention Mechanism

**Objective:** Understand the core intuition behind the attention mechanism that powers transformers, focusing on conceptual understanding rather than mathematical complexity.

## What you'll learn

- Why traditional sequence models fail on long-range dependencies
- The core insight behind attention: "looking at everything at once"
- How attention weights are computed and applied
- The difference between self-attention and cross-attention
- Why attention is the foundation of transformers

## Agenda

| Segment | Time | Description |
| ------- | ---- | ----------- |
| 0. Motivation | 3 min | The problem with sequential processing |
| 1. The RNN limitation | 8 min | Build an RNN and watch it forget |
| 2. Attention mechanism | 12 min | The "looking everywhere" solution |
| 3. Build attention from scratch | 10 min | Implement basic attention in ~30 lines |
| 4. Scale and context | 5 min | Real-world transformer attention |
| 5. Self-attention deep dive | 15 min | Query, Key, Value matrices explained |
| 6. Multi-head attention | 7 min | Why we need multiple attention heads |
| 7. Exercises and quiz | — | Practice problems and self-check |

## Prerequisites

- Understanding of neural networks and matrix operations
- Familiarity with embeddings (from Day 01)

## Key source

- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) by Jay Alammar
- Focus on intuition, skip the mathematical details for now

## How to run

```bash
cd projects/day-02-attention-mechanism
jupyter notebook lesson.ipynb
```

## Files

- `lesson.ipynb` — Interactive lesson (60 minutes)
- `NOTES.md` — One-page cheat sheet
- `requirements.txt` — Dependencies for this lesson