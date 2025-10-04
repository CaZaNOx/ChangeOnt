# agents/co/core/headers/loop_signal.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class LoopEMA:
    """
    Exponential Moving Average (EMA) over a binary 'still looping?' indicator ζ_t.
    ζ_t can be e.g. 1[a_t == a_{t-1}].
    """
    beta: float = 0.20  # smoothing
    value: float = 0.0  # λ_0

    def push(self, zeta: int | float) -> float:
        b = float(self.beta)
        z = 1.0 if float(zeta) > 0.5 else 0.0
        self.value = (1.0 - b) * self.value + b * z
        # clip for numerical safety
        if self.value < 0.0: self.value = 0.0
        if self.value > 1.0: self.value = 1.0
        return self.value
