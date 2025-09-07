# core/gauge/haq.py
from __future__ import annotations

from dataclasses import dataclass

@dataclass
class GaugeConfig:
    alpha0: float = 0.6   # step exponent: alpha_t = (t + t0)^-alpha0
    t0: float = 50.0
    leak: float = 1e-3    # ρ
    clip_min: float = 0.0
    clip_max: float = 1.0
    lambda_pe: float = 1.0
    beta_eu: float = 1.0

class Gauge:
    """
    Simple Robbins–Monro + leak update: g_{t+1} = clip(g_t + α_t*(λ*PE - β*EU) - ρ*g_t).
    """
    def __init__(self, cfg: GaugeConfig):
        self.cfg = cfg
        self.t = 0
        self.g = 0.5  # start mid
    def step(self, pe: float, eu: float) -> float:
        self.t += 1
        alpha_t = (self.t + self.cfg.t0) ** (-self.cfg.alpha0)
        delta = alpha_t * (self.cfg.lambda_pe * pe - self.cfg.beta_eu * eu) - self.cfg.leak * self.g
        self.g = max(self.cfg.clip_min, min(self.cfg.clip_max, self.g + delta))
        return self.g
