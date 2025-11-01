# agents/co/core/primitives/bandit_stats.py
from __future__ import annotations
from typing import List, Optional

class BanditStats:
    """Per-arm counts and means, updated from feedback {action,reward}."""
    def __init__(self) -> None:
        self.N: List[int] = []
        self.S: List[float] = []
        self.t: int = 0

    def _ensure(self, n_arms: int) -> None:
        if n_arms <= 0:
            return
        if len(self.N) < n_arms:
            grow = n_arms - len(self.N)
            self.N.extend([0]*grow)
            self.S.extend([0.0]*grow)

    def update_from_feedback(self, n_arms: int, action: Optional[int], reward: Optional[float]) -> None:
        self._ensure(n_arms)
        self.t += 1
        if action is None or reward is None:
            return
        a = int(action)
        if 0 <= a < len(self.N):
            self.N[a] += 1
            self.S[a] += float(reward)

    def mean(self, a: int) -> float:
        n = self.N[a]
        return (self.S[a] / n) if n > 0 else 0.0