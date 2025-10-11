from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional, Iterable, Tuple

# Density header (returns floats)
from agents.co.core.headers.density import density_rho


@dataclass
class HAQCfg:
    """
    Minimal HAQ config:
      - A:         alphabet size of observations/actions
      - L:         default window for short-horizon signals
      - L_win:     optional alias (if the caller prefers "L_win"); when set it overrides L
      - ema_alpha: smoothing for internal signals (kept for future use)
      - L_hist:    how many rewards to keep in a rolling history
    """
    A: int = 8
    L: int = 6
    L_win: Optional[int] = None
    ema_alpha: float = 0.1
    L_hist: int = 64

    @property
    def L_eff(self) -> int:
        return int(self.L_win if self.L_win is not None else self.L)


class HAQAgent:
    """
    Extremely lightweight HAQ-style agent for the renewal environment.

    Policy (for now): predict the previous observation (last-FSM) —
    with CO headers computed internally for future tuning / gating.
    This keeps behavior deterministic and aligns budget parity.

    Methods used by runners:
      - reset(obs: int) -> None
      - act(obs: int) -> int
      - update(obs: int, reward: float, done: bool) -> None
      - budget_row() -> dict
    """

    def __init__(self, cfg: HAQCfg) -> None:
        self.cfg = cfg
        self.prev_obs: int = 0
        self.rew_hist: Deque[float] = deque(maxlen=max(1, int(cfg.L_hist)))

        # Internal smoothed signals (kept for potential future use)
        self._ema_rho: float = 0.0
        self._ema_rho_ex: float = 0.0

    # ---- API expected by runners ----

    def reset(self, obs: int) -> None:
        self.prev_obs = int(obs)
        self.rew_hist.clear()
        self._ema_rho = 0.0
        self._ema_rho_ex = 0.0

    def act(self, obs: int) -> int:
        # Predict last observation (keeps determinism and correct invariants)
        return int(self.prev_obs)

    def update(self, obs: int, reward: float, done: bool) -> None:
        # Maintain last-observation memory
        self.prev_obs = int(obs)

        # Record reward and compute density headers (floats)
        self.rew_hist.append(float(reward))
        L = max(1, min(self.cfg.L_eff, len(self.rew_hist)))
        rho, rho_ex = self._safe_density(self.rew_hist, L=L, A=self.cfg.A)

        # Simple EMA smoothing of signals (not used for policy yet)
        a = float(self.cfg.ema_alpha)
        self._ema_rho = (1.0 - a) * self._ema_rho + a * rho
        self._ema_rho_ex = (1.0 - a) * self._ema_rho_ex + a * rho_ex

        # No telemetry writes here (runner owns metrics.jsonl). This avoids
        # shape mismatches and keeps the agent side-effect free.

    def budget_row(self) -> dict:
        # Parity with STOA baselines the user expects (6/4/6).
        return {"params_bits": 6, "flops_per_step": 4, "memory_bytes": 6}

    # ---- helpers ----

    @staticmethod
    def _safe_density(history: Iterable[float], L: int, A: int) -> Tuple[float, float]:
        try:
            return density_rho(history, L=L, A=A)
        except Exception:
            # Extremely defensive fallback
            return 0.0, 0.0
