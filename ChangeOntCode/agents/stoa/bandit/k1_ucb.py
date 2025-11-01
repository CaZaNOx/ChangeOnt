# FILE: agents/bandit/kl_ucb.py
from __future__ import annotations
import math

def _kl_bernoulli(p: float, q: float) -> float:
    p = min(max(p, 1e-12), 1 - 1e-12)
    q = min(max(q, 1e-12), 1 - 1e-12)
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))

def _inv_kl(p: float, c: float) -> float:
    lo, hi = p, 1 - 1e-12
    for _ in range(35):
        mid = 0.5 * (lo + hi)
        if _kl_bernoulli(p, mid) > c:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

class KLUCB:
    def __init__(self, n_arms: int, c: float = 0.0):
        self.n = int(n_arms)
        self.succ = [0.0] * self.n
        self.count = [0] * self.n
        self.tot = 0
        self.c = float(c)

    def select(self) -> int:
        if self.tot < self.n:
            return self.tot
        ucb = []
        for i in range(self.n):
            p_hat = self.succ[i] / max(1, self.count[i])
            c = (math.log(self.tot) + 3 * math.log(max(2.0, math.log(self.tot + 1)))) / max(1, self.count[i]) + self.c
            ucb.append(_inv_kl(p_hat, c))
        return max(range(self.n), key=lambda i: ucb[i])

    def update(self, arm: int, reward: float) -> None:
        self.tot += 1
        ai = int(arm)
        self.count[ai] += 1
        if reward >= 0.5:
            self.succ[ai] += 1.0
