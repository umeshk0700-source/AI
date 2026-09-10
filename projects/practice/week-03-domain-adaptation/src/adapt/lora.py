
"""LoRA adapter + trainer, numpy, from scratch (Day 08)."""
from __future__ import annotations

import numpy as np


class LoRAAdapter:
    """Wraps a frozen weight W (d_out, d_in). Trainable: A (r, d_in), B (d_out, r).
    Effective weight = W + (alpha/r) * B @ A ; B is zero-initialised."""

    def __init__(self, W: np.ndarray, r: int = 4, alpha: int | None = None, seed: int = 0):
        self.W = W
        self.r = r
        self.scale = (alpha if alpha is not None else r) / r
        g = np.random.default_rng(seed)
        d_out, d_in = W.shape
        self.A = g.standard_normal((r, d_in)) * 0.01
        self.B = np.zeros((d_out, r))

    def delta(self) -> np.ndarray:
        # TODO: the low-rank weight update  (alpha/r) * B @ A   -> shape == W.shape
        raise NotImplementedError("the low-rank weight update  (alpha/r) * B @ A   -> shape == W.shape")

    def forward(self, x: np.ndarray) -> np.ndarray:
        # x: (batch, d_in).  TODO: return x @ (W + delta).T
        raise NotImplementedError("the low-rank weight update  (alpha/r) * B @ A   -> shape == W.shape")

    def merge(self) -> np.ndarray:
        # TODO: return a single dense matrix W + delta (folded, zero inference overhead)
        raise NotImplementedError("return a single dense matrix W + delta (folded, zero inference overhead)")

    @property
    def n_trainable(self) -> int:
        return self.A.size + self.B.size


class LoRATrainer:
    def __init__(self, adapter: LoRAAdapter, lr: float = 0.05):
        self.a = adapter
        self.lr = lr

    def step(self, x: np.ndarray, target: np.ndarray) -> float:
        # one SGD step on mean-squared-error, updating ONLY A and B (W is frozen).
        # forward:  pred = x @ (W + scale*B@A).T
        # TODO:
        #   pred = self.a.forward(x)
        #   g_pred = 2 * (pred - target) / x.shape[0]         # dL/dpred
        #   g_eff  = g_pred.T @ x                             # dL/d(effective W), shape W.shape
        #   g_B = scale * (g_eff @ A.T) ;  g_A = scale * (B.T @ g_eff)
        #   A -= lr * g_A ; B -= lr * g_B
        #   return float mean squared error
        raise NotImplementedError("#   pred = self.a.forward(x)")

    def fit(self, x: np.ndarray, target: np.ndarray, steps: int = 400) -> list[float]:
        return [self.step(x, target) for _ in range(steps)]
