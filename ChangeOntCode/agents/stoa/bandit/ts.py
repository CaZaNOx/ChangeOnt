# FILE: agents/bandit/ts.py
from __future__ import annotations
import random

class ThompsonSampling:
    def __init__(self, n_arms: int):
        self.n = int(n_arms)
        self.alpha = [1.0] * self.n
        self.beta  = [1.0] * self.n

    def select(self) -> int:
        samples = [random.betavariate(self.alpha[i], self.beta[i]) for i in range(self.n)]
        return max(range(self.n), key=lambda i: samples[i])

    def update(self, arm: int, reward: float) -> None:
        if reward >= 0.5:
            self.alpha[int(arm)] += 1.0
        else:
            self.beta[int(arm)]  += 1.0
