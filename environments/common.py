from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Optional

@dataclass
class RNG:
    seed: int
    _rng: random.Random

    @classmethod
    def from_seed(cls, seed: Optional[int]) -> "RNG":
        s = int(seed if seed is not None else 0)
        return cls(seed=s, _rng=random.Random(s))

    def rand(self) -> float:
        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        return self._rng.randint(a, b)

    def choice(self, seq):
        return self._rng.choice(seq)
