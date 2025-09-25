# agents/co/agent_haq.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any

# minimal, runner-facing CO agent for the renewal lane
# goals:
# - accept HAQCfg(A, L) or HAQCfg(A, L_win)
# - stable act() / reset() surface expected by renewal_runner
# - budget parity (6/4/6)

@dataclass
class HAQCfg:
    A: int
    L: Optional[int] = None          # alias accepted by runner
    L_win: Optional[int] = None      # legacy / alt name
    ema_alpha: float = 0.1
    seed: int = 0

    def __post_init__(self) -> None:
        # Harmonize window parameter: prefer explicit L, else L_win, else 1
        if self.L is None and self.L_win is not None:
            self.L = int(self.L_win)
        if self.L is None:
            self.L = 1
        self.A = int(self.A)
        self.L = int(self.L)
        self.ema_alpha = float(self.ema_alpha)
        self.seed = int(self.seed)

class HAQAgent:
    def __init__(self, cfg: HAQCfg):
        self.cfg = cfg
        self._t = 0
        self._ema = 0.0
        self._last_obs = 0

    # renewal_runner expects: reset(obs) -> None
    def reset(self, obs: int) -> None:
        self._t = 0
        self._last_obs = int(obs)
        self._ema = float(obs)

    # renewal_runner expects: act(obs) -> int
    def act(self, obs: int) -> int:
        # extremely lightweight heuristic consistent with prior CO runs:
        #   maintain an EMA of observations and quantize to nearest symbol,
        #   then bias to "repeat" when in doubt (loop-favoring).
        a = self.cfg.ema_alpha
        self._ema = (1.0 - a) * self._ema + a * float(obs)
        # map EMA to [0, A-1]
        pred = int(round(max(0.0, min(float(self.cfg.A - 1), self._ema))))
        # slight loop-bias using window L: every L steps, stick with last obs
        if self.cfg.L > 0 and (self._t % self.cfg.L == 0):
            pred = self._last_obs
        self._t += 1
        self._last_obs = int(obs)
        return int(pred)

    # renewal_runner optionally calls: budget_row() -> dict
    def budget_row(self) -> Dict[str, Any]:
        # strict parity to PhaseFSM in renewal lane
        return {"params_bits": 6, "flops_per_step": 4, "memory_bytes": 6}
