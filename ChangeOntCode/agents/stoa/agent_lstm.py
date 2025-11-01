from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import math


# Minimal, dependency-free LSTM-like cell (for tiny baselines)
class LSTMLite:
    def __init__(self, input_dim: int, hidden_dim: int):
        self.input_dim = int(input_dim)
        self.hidden_dim = int(hidden_dim)
        # Tiny parameter sets (initialized deterministically)
        rng = self._rng(7)
        def init(m, n):
            return [[rng() * 0.1 for _ in range(n)] for _ in range(m)]
        H = hidden_dim
        D = input_dim
        self.Wf = init(H, H + D)
        self.Wi = init(H, H + D)
        self.Wo = init(H, H + D)
        self.Wg = init(H, H + D)
        self.bf = [0.0] * H
        self.bi = [0.0] * H
        self.bo = [0.0] * H
        self.bg = [0.0] * H

    @staticmethod
    def _rng(seed: int):
        # simple LCG
        state = seed & 0xFFFFFFFF
        def f():
            nonlocal state
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            return ((state >> 8) & 0xFFFFFF) / float(1 << 24)
        return f

    @staticmethod
    def _sigmoid(x: float) -> float:
        if x < -40: return 0.0
        if x >  40: return 1.0
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def _tanh(x: float) -> float:
        if x < -20: return -1.0
        if x >  20: return 1.0
        e = math.exp(2.0 * x)
        return (e - 1.0) / (e + 1.0)

    def _affine(self, W, b, h, x):
        # W: H x (H + D)
        z: List[float] = []
        cat = h + x
        for row, bias in zip(W, b):
            s = bias
            for w, v in zip(row, cat):
                s += w * v
            z.append(s)
        return z

    def step(self, h: List[float], c: List[float], x: List[float]) -> tuple[List[float], List[float]]:
        H = self.hidden_dim
        f = [self._sigmoid(v) for v in self._affine(self.Wf, self.bf, h, x)]
        i = [self._sigmoid(v) for v in self._affine(self.Wi, self.bi, h, x)]
        o = [self._sigmoid(v) for v in self._affine(self.Wo, self.bo, h, x)]
        g = [self._tanh(v)    for v in self._affine(self.Wg, self.bg, h, x)]
        c_new = [f[j] * c[j] + i[j] * g[j] for j in range(H)]
        h_new = [o[j] * self._tanh(c_new[j]) for j in range(H)]
        return h_new, c_new


@dataclass
class LSTMLiteAgent:
    """
    Tiny LSTM baseline. Not meant for SOTA performance—just a simple sequence learner.
    For bandits: we map one-hot arm index to input and choose argmax of predicted reward.
    """
    input_dim: int = 4
    hidden_dim: int = 8
    lstm: LSTMLite = field(init=False)
    h: List[float] = field(init=False)
    c: List[float] = field(init=False)
    last_arm: Optional[int] = None
    n_arms: int = 0

    def __post_init__(self) -> None:
        self.lstm = LSTMLite(self.input_dim, self.hidden_dim)
        self.h = [0.0] * self.hidden_dim
        self.c = [0.0] * self.hidden_dim

    def reset(self, env_or_n: int | object) -> None:
        if isinstance(env_or_n, int):
            self.n_arms = env_or_n
        else:
            self.n_arms = int(getattr(env_or_n, "n_arms", 0))
        if self.n_arms <= 0:
            self.n_arms = self.input_dim
        self.h = [0.0] * self.hidden_dim
        self.c = [0.0] * self.hidden_dim
        self.last_arm = None

    def act(self) -> int:
        # Probe each arm quickly and pick the best predicted immediate reward proxy
        best = 0
        best_score = -1e9
        for i in range(self.n_arms):
            x = [0.0] * self.input_dim
            x[i % self.input_dim] = 1.0
            h2, c2 = self.lstm.step(self.h, self.c, x)
            # simple readout: sum of hidden (monotone proxy)
            score = sum(h2)
            if score > best_score:
                best_score = score
                best = i
        self.last_arm = best
        return best

    def observe(self, reward: float) -> None:
        # Nudge internal state with observed reward as a scalar input
        x = [0.0] * self.input_dim
        x[0] = float(reward)  # crude, but keeps it dependency-free
        self.h, self.c = self.lstm.step(self.h, self.c, x)
