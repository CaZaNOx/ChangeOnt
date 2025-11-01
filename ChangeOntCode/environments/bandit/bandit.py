from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from environments.common import RNG


@dataclass
class BernoulliBanditEnv:
    """
    Stationary Bernoulli K-armed bandit.

    API exposed to runners/agents:
      - .n_arms : int
      - reset(seed: Optional[int]) -> None
      - step(arm: int) -> tuple[None, float, bool, dict]
        (obs is None; done always False unless horizon is set)
    """
    probs: List[float]
    horizon: Optional[int] = None
    _rng: RNG = field(init=False)
    _t: int = field(default=0, init=False)
    n_arms: int = field(init=False)

    def __post_init__(self) -> None:
        if not self.probs:
            raise ValueError("BernoulliBanditEnv: probs must be non-empty")
        if any(p < 0.0 or p > 1.0 for p in self.probs):
            raise ValueError("BernoulliBanditEnv: probs must be in [0,1]")
        self.n_arms = len(self.probs)
        self._rng = RNG.from_seed(0)

    def reset(self, seed: Optional[int] = None) -> None:
        self._rng = RNG.from_seed(seed)
        self._t = 0

    def step(self, arm: int) -> Tuple[None, float, bool, Dict]:
        if arm < 0 or arm >= self.n_arms:
            raise IndexError(f"arm index {arm} out of range 0..{self.n_arms-1}")
        self._t += 1
        p = self.probs[arm]
        r = 1.0 if self._rng.rand() < p else 0.0
        done = False
        if self.horizon is not None and self._t >= self.horizon:
            done = True
        info: Dict = {"t": self._t}
        return None, r, done, info
