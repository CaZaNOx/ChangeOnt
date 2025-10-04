# agents/co/core/primitives/robins_monro.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RobbinsMonroEstimator:
    """
    Robbins–Monro online mean estimator:
      m_{t+1} = m_t + η_t * (x_t - m_t),   η_t = 1/(t+1) or a clamped minimum.
    """
    min_eta: float = 0.0
    _mean: float = 0.0
    _t: int = 0

    def reset(self) -> None:
        self._mean = 0.0
        self._t = 0

    def update(self, x: float) -> float:
        self._t += 1
        eta = max(1.0 / self._t, float(self.min_eta))
        self._mean += eta * (float(x) - self._mean)
        return self._mean

    @property
    def mean(self) -> float:
        return self._mean
