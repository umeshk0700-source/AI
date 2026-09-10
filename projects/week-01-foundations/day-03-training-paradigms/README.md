# Day 03 — Training Paradigms

**Objective:** Understand the three-stage training pipeline that creates modern AI systems: pretraining → fine-tuning → RLHF, focusing on practical understanding over mathematical details.

## What you'll learn

- Why we need different training stages for different goals  
- How pretraining teaches language understanding from raw text
- How fine-tuning specializes models for specific tasks
- How RLHF aligns models with human preferences
- The practical trade-offs between each approach

## Agenda

| Segment | Time | Description |
| ------- | ---- | ----------- |
| 0. The training problem | 3 min | Why one training method isn't enough |
| 1. Supervised learning failure | 8 min | Try to train on end task, watch it fail |
| 2. Pretraining on language | 12 min | Self-supervised learning from text |
| 3. Fine-tuning implementation | 10 min | Adapt pretrained model to specific tasks |
| 4. Scale and data requirements | 5 min | Real-world training costs and data |
| 5. RLHF deep dive | 15 min | Human feedback and preference learning |
| 6. The alignment problem | 7 min | Why RLHF is crucial for deployment |
| 7. Exercises and quiz | — | Practice problems and self-check |

## Prerequisites

- Understanding of neural networks and backpropagation
- Familiarity with transformers (from Day 02)
- Basic understanding of supervised learning

## Key concepts covered

- **Pretraining**: Learning language patterns from massive unlabeled text
- **Fine-tuning**: Adapting to specific tasks with labeled data  
- **RLHF**: Reinforcement Learning from Human Feedback for alignment
- **Transfer learning**: Why pretrained models generalize so well
- **Emergence**: How capabilities appear with scale and data

## How to run

```bash
cd projects/week-01-foundations/day-03-training-paradigms
jupyter notebook lesson.ipynb
```

## Files

- `lesson.ipynb` — Interactive lesson (60 minutes)
- `NOTES.md` — One-page cheat sheet
- `requirements.txt` — Dependencies for this lesson