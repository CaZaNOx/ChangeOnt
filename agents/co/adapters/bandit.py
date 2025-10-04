from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import math
import random

@dataclass
class COBanditCfg:
    n_arms: int
    seed: int = 0
    # optional: smoothing for a simple CO-ish header (loop/ema idea is not needed for bandit baseline)
    ema_alpha: float = 0.0  # 0.0 => pure sample-mean, deterministic tie-breaks

class COBanditAgent:
    """
    Deterministic CO adapter for K-armed Bernoulli bandit.
    - Keeps per-arm estimates with optional EMA.
    - NO unseeded randomness; deterministic tie-breaks by lowest index.
    - budget_row aligned with a tiny agent: 6/4/6 like PhaseFSM ledger we use for parity.
    """
    def __init__(self, cfg: COBanditCfg):
        self.cfg = cfg
        self.n = int(cfg.n_arms)
        self.counts: List[int] = [0] * self.n
        self.values: List[float] = [0.0] * self.n
        self.alpha = float(cfg.ema_alpha)
        self._rng = random.Random(cfg.seed)  # if alpha>0 and we ever add stochastic bits, this stays pinned

    def select(self) -> int:
        # Play each arm once (deterministic order)
        for a in range(self.n):
            if self.counts[a] == 0:
                return a
        # Greedy on current values; deterministic tie-break (lowest index)
        best_val = max(self.values)
        # find the first arm achieving best_val
        for a in range(self.n):
            if self.values[a] == best_val:
                return a
        return 0  # unreachable safeguard

    def update(self, a: int, r: float) -> None:
        a = int(a)
        self.counts[a] += 1
        if self.alpha <= 0.0:
            # sample-mean
            n = self.counts[a]
            q = self.values[a]
            self.values[a] = q + (r - q) / n
        else:
            # EMA (still deterministic)
            q = self.values[a]
            self.values[a] = (1.0 - self.alpha) * q + self.alpha * r

    # For budget parity with our frozen ledger (renewal lane): 6/4/6
    def budget_row(self) -> dict:
        return {"params_bits": 6, "flops_per_step": 4, "memory_bytes": 6}
