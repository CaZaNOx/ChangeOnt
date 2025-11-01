# FILE: agents/stoa/vo_markov.py
from __future__ import annotations
from collections import defaultdict, deque

class VOKT:
    def __init__(self, A: int, max_order: int):
        self.A = int(A)
        self.K = int(max_order)
        self.ctx = deque([0]*self.K, maxlen=self.K)
        self.counts = defaultdict(lambda: defaultdict(int))  # ctx -> {y: count}

    def reset(self, init_obs: int):
        self.ctx = deque([int(init_obs)]*self.K, maxlen=self.K)
        self.counts.clear()

    def _score(self, ctx, y: int) -> float:
        c = self.counts.get(ctx, {})
        num = c.get(y, 0) + 0.5
        den = sum(c.values()) + 0.5*self.A
        return num/den if den > 0 else 1.0/self.A

    def act(self, obs: int) -> int:
        ctx = tuple(self.ctx)
        best_y, best_s = 0, -1.0
        for y in range(self.A):
            s = self._score(ctx, y)
            if s > best_s:
                best_s, best_y = s, y
        y_obs = int(obs)
        self.counts[ctx][y_obs] += 1
        if self.K > 0:
            self.ctx.append(y_obs)
        return int(best_y)

    def budget_row(self) -> dict:
        return {"params_bits": self.A*self.K, "flops_per_step": self.A + self.K, "memory_bytes": self.A*self.K}
