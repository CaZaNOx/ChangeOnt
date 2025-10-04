# agents/co/core/primitives/filters/ema.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

def clamp01(x: float) -> float:
    """Clamp a float to [0, 1]."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x

@dataclass
class EMAState:
    """
    Lightweight container for a functional EMA.
    - value: current EMA value
    - initialized: whether the state has been initialized with the first sample
    """
    value: float = 0.0
    initialized: bool = False

def ema_update(state: EMAState, x: float, alpha: float) -> EMAState:
    """
    Functional EMA:
      m_t = alpha * x + (1 - alpha) * m_{t-1}
    Returns an updated EMAState (does not mutate the input state).
    """
    a = clamp01(alpha)
    if not state.initialized:
        return EMAState(value=float(x), initialized=True)
    new_val = a * float(x) + (1.0 - a) * float(state.value)
    return EMAState(value=new_val, initialized=True)

def ema_value(state: EMAState) -> float:
    """Return the current value stored in the EMAState."""
    return float(state.value)

@dataclass
class EMA:
    """
    Object-oriented EMA for registry-based construction.

    Example:
        ema = EMA(alpha=0.2)
        ema.update(1.0)
        ema.update(2.0)
        current = ema.value
    """
    alpha: float = 0.2
    _value: float = 0.0
    _initialized: bool = False

    def __post_init__(self) -> None:
        self.alpha = clamp01(float(self.alpha))

    def reset(self, init_value: Optional[float] = None) -> None:
        if init_value is None:
            self._initialized = False
            self._value = 0.0
        else:
            self._initialized = True
            self._value = float(init_value)

    def update(self, x: float) -> float:
        if not self._initialized:
            self._initialized = True
            self._value = float(x)
            return self._value
        self._value = self.alpha * float(x) + (1.0 - self.alpha) * self._value
        return self._value

    @property
    def value(self) -> float:
        return float(self._value)
