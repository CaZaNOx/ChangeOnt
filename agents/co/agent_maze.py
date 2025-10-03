# PATH: agents/co/agent_maze.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from agents.co.core.headers.meta_flip import MetaFlip
from agents.co.core.headers.loop_score import LoopEMA
from agents.co.core.headers.density import compute_density_signals


@dataclass
class HAQMazeCfg:
    """
    CO-HAQ for Maze.
    - Rewards: maze gives -1 per step, 0 at goal.
      We SYMBOLIZE to {0,1}:  -1 -> 0 (step),  0 -> 1 (goal).
    """
    A: int = 2                  # symbol alphabet after mapping
    L_hist: int = 16            # history window for headers
    ema_alpha: float = 0.1      # EMA for loop score smoothing


class HAQMazeAgent:
    """
    Minimal HAQ agent for deterministic grid maze.
    Actions: 'UP','DOWN','LEFT','RIGHT'
    Strategy: rank actions via MetaFlip (lightweight cyclic preference),
              use loop_score / density for gating.
    """
    def __init__(self, cfg: HAQMazeCfg | None = None):
        self.cfg = cfg or HAQMazeCfg()
        self.flips = MetaFlip()            # CO header (already present in your repo)
        self.rew_hist: List[int] = []      # store SYMBOLS, not raw rewards
        self.last_obs: Tuple[int, int] | None = None

    # ---------------------------
    # Public API expected by maze_runner
    # ---------------------------

    def reset(self, obs) -> None:
        self.flips.reset()
        self.rew_hist.clear()
        self.last_obs = obs

    def select(self) -> str:
        # Ordered candidate actions via MetaFlip (cyclic) -> ["UP","RIGHT","DOWN","LEFT"] rotated
        cand = self._ordered_actions()
        return cand[0]

    def update(self, obs, reward: float, done: bool) -> None:
        # Push SYMBOLIZED reward
        self._push_reward(reward, done)
        # Optionally update flips/headers from signals
        self._update_headers()
        self.last_obs = obs

    def budget_row(self) -> dict:
        # Keep parity modest; adjust if you want different accounting
        return {"params_bits": 6, "flops_per_step": 4, "memory_bytes": 6}

    # ---------------------------
    # Internals
    # ---------------------------

    def _ordered_actions(self) -> List[str]:
        # Simple cyclic preference using MetaFlip’s internal counter
        # We assume MetaFlip exposes .count() that increments on .flip()/update(),
        # but we also guard with getattr default 0.
        k = getattr(self.flips, "count", lambda: 0)()
        base = ["UP", "RIGHT", "DOWN", "LEFT"]
        r = k % 4
        return base[r:] + base[:r]

    def _push_reward(self, raw_reward: float, done: bool) -> None:
        """
        Symbolize maze reward stream:
          - step: -1  -> 0
          - goal:  0  -> 1   (done is True exactly when reward==0 in this env)
        """
        sym = 1 if raw_reward == 0.0 else 0
        self.rew_hist.append(sym)
        if len(self.rew_hist) > self.cfg.L_hist:
            self.rew_hist.pop(0)

    def _update_headers(self) -> None:
        if not self.rew_hist:
            return
        L = min(self.cfg.L_hist, len(self.rew_hist))
        # Density signals over symbolized stream
        dens_smooth, dens = compute_density_signals(
            self.rew_hist[-L:], A=self.cfg.A, L=L
        )
        # Loop score smoothing over same history
        loop_s = LoopEMA(self.rew_hist[-L:], alpha=self.cfg.ema_alpha)
        # Use signals to toggle meta flips lightly (example: flip when loopiness drops)
        if loop_s < 0.25:
            self.flips.flip()
