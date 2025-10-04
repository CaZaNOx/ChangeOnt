# agents/co/core/primitives/hysteresis.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class HysteresisFilter:
    """
    Exponential smoothing with a threshold: only emit a 'change' if the smoothed
    value moved enough (>= threshold) since the last commit.
    """
    alpha: float = 0.2
    threshold: float = 0.05
    _smooth: float = 0.0
    _last_committed: float = 0.0
    _initialized: bool = False

    def reset(self) -> None:
        self._smooth = 0.0
        self._last_committed = 0.0
        self._initialized = False

    def update(self, x: float) -> float:
        if not self._initialized:
            self._smooth = float(x)
            self._last_committed = float(x)
            self._initialized = True
            return self._last_committed

        self._smooth = self.alpha * float(x) + (1.0 - self.alpha) * self._smooth
        if abs(self._smooth - self._last_committed) >= self.threshold:
            self._last_committed = self._smooth
        return self._last_committed

    def score(self) -> float:
        """Return the current smooth value (useful for introspection)."""
        return self._smooth

    def __repr__(self) -> str:
        return (f"HysteresisFilter(alpha={self.alpha}, threshold={self.threshold}, "
                f"smooth={self._smooth:.4f}, committed={self._last_committed:.4f})")
