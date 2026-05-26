from __future__ import annotations
from typing import List, Optional

class BanditStats:
    """Per-arm counts and means, updated only from visible (action, reward) feedback."""
    def __init__(self) -> None:
        self.N: List[int] = []
        self.S: List[float] = []
        self.t: int = 0

    def _ensure(self, n_arms: int) -> None:
        n_arms = max(0, int(n_arms))
        if len(self.N) < n_arms:
            grow = n_arms - len(self.N)
            self.N.extend([0] * grow)
            self.S.extend([0.0] * grow)

    def ensure(self, n_arms: int) -> None:
        self._ensure(n_arms)

    @property
    def counts(self) -> List[int]:
        return list(self.N)

    @property
    def means(self) -> List[float]:
        out: List[float] = []
        for i, n in enumerate(self.N):
            out.append((self.S[i] / n) if n > 0 else 0.0)
        return out

    def update(self, action: Optional[int], reward: Optional[float], n_arms: Optional[int] = None) -> None:
        if n_arms is not None:
            self._ensure(int(n_arms))
        self.t += 1
        if action is None or reward is None:
            return
        a = int(action)
        if 0 <= a < len(self.N):
            self.N[a] += 1
            self.S[a] += float(reward)

    def update_from_feedback(self, n_arms: int, action: Optional[int], reward: Optional[float]) -> None:
        self._ensure(n_arms)
        self.update(action=action, reward=reward)

    def mean(self, a: int) -> float:
        if a < 0 or a >= len(self.N):
            return 0.0
        n = self.N[a]
        return (self.S[a] / n) if n > 0 else 0.0
