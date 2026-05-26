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

    def ensure(self, A: int) -> None:
        A = int(A)
        if A <= self.A:
            return
        oldA = self.A
        self.A = A
        for key, row in list(self.counts.items()):
            if len(row) < A:
                row.extend([0] * (A - len(row)))

    def predict_proba(self):
        if self.k == 0 or len(self.ctx) < self.k:
            return [1.0 / max(1, self.A)] * max(1, self.A)
        row = list(self.counts[tuple(self.ctx)])
        total = float(sum(row))
        if total <= 0.0:
            return [1.0 / max(1, self.A)] * max(1, self.A)
        return [float(v) / total for v in row]

    def update_from_feedback(self, obs_symbol: Optional[int]) -> None:
        self.on_feedback(obs_symbol)
