from __future__ import annotations
from typing import Dict, Tuple, List, Optional
from collections import deque, defaultdict

class NGramModel:
    """
    Simple n-gram (order k) frequency model for renewal-like discrete symbols.
    Tracks a context of length k and exposes both hard prediction and probability APIs.
    """
    def __init__(self, A: int = 8, order: int = 2) -> None:
        self.A = max(1, int(A))
        self.k = max(0, int(order))
        self.ctx = deque(maxlen=self.k)
        self.counts: Dict[Tuple[int, ...], List[int]] = defaultdict(self._new_row)

    def _new_row(self) -> List[int]:
        return [0] * self.A

    def ensure(self, A: Optional[int] = None, order: Optional[int] = None) -> None:
        if A is not None and int(A) != self.A:
            new_A = max(1, int(A))
            old_counts = self.counts
            self.A = new_A
            self.counts = defaultdict(self._new_row)
            for ctx, row in old_counts.items():
                grown = list(row[:new_A])
                if len(grown) < new_A:
                    grown.extend([0] * (new_A - len(grown)))
                self.counts[ctx] = grown
        if order is not None and int(order) != self.k:
            self.k = max(0, int(order))
            self.ctx = deque(list(self.ctx)[-self.k:], maxlen=self.k)

    def reset(self) -> None:
        self.ctx = deque(maxlen=self.k)

    def on_feedback(self, obs_symbol: Optional[int]) -> None:
        if obs_symbol is None:
            return
        obs = int(obs_symbol)
        if self.k > 0 and len(self.ctx) == self.k:
            self.counts[tuple(self.ctx)][obs] += 1
        if self.k > 0:
            self.ctx.append(obs)

    def predict(self) -> int:
        proba = self.predict_proba()
        if not proba:
            return 0
        return max(sorted(proba.keys()), key=lambda a: proba[a])

    def predict_proba(self) -> Dict[int, float]:
        if self.k == 0 or len(self.ctx) < self.k:
            return {a: 1.0 / float(self.A) for a in range(self.A)}
        row = self.counts.get(tuple(self.ctx))
        if row is None:
            return {a: 1.0 / float(self.A) for a in range(self.A)}
        total = float(sum(row))
        if total <= 0.0:
            return {a: 1.0 / float(self.A) for a in range(self.A)}
        return {a: float(row[a]) / total for a in range(self.A)}
