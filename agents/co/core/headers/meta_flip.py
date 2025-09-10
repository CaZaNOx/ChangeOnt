# core/headers/meta_flip.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class FlipConfig:
    beta: float = 0.9  # EMA factor
    theta_on: float = 0.25
    theta_off: float = 0.15
    cooldown_steps: int = 10

class HysteresisFlip:
    """
    Tracks loop_score with EMA; flips mode when thresholds crossed, enforcing cooldown and hysteresis.
    """
    def __init__(self, cfg: FlipConfig):
        self.cfg = cfg
        self.ema: Optional[float] = None
        self.mode: int = 0  # 0 = exploit, 1 = explore (example)
        self._cooldown: int = 0
        self.flip_count: int = 0

    def step(self, loop_score: float) -> int:
        # update EMA
        if self.ema is None:
            self.ema = loop_score
        else:
            self.ema = self.cfg.beta * self.ema + (1 - self.cfg.beta) * loop_score

        if self._cooldown > 0:
            self._cooldown -= 1
            return self.mode

        # hysteresis thresholds
        if self.mode == 0 and self.ema is not None and self.ema >= self.cfg.theta_on:
            self.mode = 1
            self._cooldown = self.cfg.cooldown_steps
            self.flip_count += 1
        elif self.mode == 1 and self.ema is not None and self.ema <= self.cfg.theta_off:
            self.mode = 0
            self._cooldown = self.cfg.cooldown_steps
            self.flip_count += 1
        return self.mode

    @property
    def cooldown(self) -> int:
        return self._cooldown
