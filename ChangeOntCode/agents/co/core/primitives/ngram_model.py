# agents/co/core/primitives/ngram_model.py
from __future__ import annotations
from typing import Dict, Tuple, List, Optional
from collections import deque, defaultdict

class NGramModel:
    """
    Simple n-gram (order k) frequency model for renewal-like discrete symbols.
    Uses feedback.observation to advance context; predicts next symbol by argmax.
    """
    def __init__(self, A: int = 8, order: int = 2) -> None:
        self.A = int(A)
        self.k = max(0, int(order))
        self.ctx = deque(maxlen=self.k)
        self.counts: Dict[Tuple[int, ...], List[int]] = defaultdict(lambda: [0]*self.A)

    def on_feedback(self, obs_symbol: Optional[int]) -> None:
        if obs_symbol is None:
            return
        if self.k > 0 and len(self.ctx) == self.k:
            self.counts[tuple(self.ctx)][int(obs_symbol)] += 1
        if self.k > 0:
            self.ctx.append(int(obs_symbol))

    def predict(self) -> int:
        if self.k == 0 or len(self.ctx) < self.k:
            return 0
        row = self.counts[tuple(self.ctx)]
        # argmax with deterministic tie-break
        best = 0
        bestv = row[0]
        for a in range(1, self.A):
            v = row[a]
            if v > bestv:
                best = a; bestv = v
        return best