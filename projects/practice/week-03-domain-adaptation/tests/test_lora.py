import numpy as np
from adapt.lora import LoRAAdapter, LoRATrainer

rng = np.random.default_rng(0)
W = rng.standard_normal((16, 12)) / np.sqrt(12)


def test_zero_init_is_a_noop():
    a = LoRAAdapter(W, r=4)
    x = rng.standard_normal((5, 12))
    assert np.allclose(a.forward(x), x @ W.T)
    assert np.allclose(a.delta(), 0.0)


def test_merge_equals_unmerged():
    a = LoRAAdapter(W, r=4)
    a.B = rng.standard_normal(a.B.shape) * 0.1        # pretend it trained
    x = rng.standard_normal((3, 12))
    assert np.allclose(a.forward(x), x @ a.merge().T)


def test_trainable_param_count():
    a = LoRAAdapter(W, r=3)
    assert a.n_trainable == 3 * (16 + 12)


def test_recovers_low_rank_target():
    # target task = W + a rank-2 twist
    U = rng.standard_normal((16, 2)); V = rng.standard_normal((2, 12))
    dW = 0.6 * (U @ V)
    X = rng.standard_normal((256, 12))
    Y = X @ (W + dW).T
    losses_r2 = LoRATrainer(LoRAAdapter(W, r=2), lr=0.05).fit(X, Y, steps=600)
    losses_r1 = LoRATrainer(LoRAAdapter(W, r=1), lr=0.05).fit(X, Y, steps=600)
    assert losses_r2[-1] < 1e-3, f"r=2 should recover a rank-2 update, loss={losses_r2[-1]:.4f}"
    assert losses_r1[-1] > losses_r2[-1] * 5, "r=1 should underfit a rank-2 update"
