# PATH: agents/co/agent_bandit.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from random import Random

from agents.co.core.headers.loop_score import loop_score_ema
from agents.co.core.headers.density import compute_density_signals
from agents.co.core.headers.meta_flip import MetaFlip
from agents.co.core.headers.collapse import CollapseGuard

@dataclass
class COBanditCfg:
    n_arms: int
    A: int = 8
    L_hist: int = 128
    ema_beta: float = 0.9
    theta_on: float = 0.6
    theta_off: float = 0.4
    cooldown: int = 50
    seed: int = 0

@dataclass
class COBanditAgent:
    cfg: COBanditCfg
    rng: Random = field(init=False)
    t: int = field(default=0, init=False)
    rew_hist: List[int] = field(default_factory=list)
    score: float = field(default=0.0, init=False)
    mode_exploit: bool = field(default=False, init=False)
    dwell: int = field(default=0, init=False)
    flips: MetaFlip = field(default_factory=MetaFlip)
    guard: CollapseGuard = field(default_factory=CollapseGuard)
    counts: List[int] = field(default_factory=list)
    means: List[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.rng = Random(self.cfg.seed)
        self.counts = [0] * self.cfg.n_arms
        self.means = [0.0] * self.cfg.n_arms

    def reset(self) -> None:
        self.t = 0
        self.rew_hist.clear()
        self.score = 0.0
        self.mode_exploit = False
        self.dwell = 0
        self.flips.reset()
        self.guard.reset()
        self.counts = [0] * self.cfg.n_arms
        self.means = [0.0] * self.cfg.n_arms

    def _update_headers(self, r_bin: int) -> None:
        self.rew_hist.append(r_bin)
        Hn, dens = compute_density_signals(
            self.rew_hist[-self.cfg.L_hist :],
            A=self.cfg.A,
            L=min(self.cfg.L_hist, len(self.rew_hist)),
        )
        raw_cost = 1.0 - dens
        self.score = loop_score_ema(self.score, [raw_cost], beta=self.cfg.ema_beta)
        if self.mode_exploit:
            if self.score <= self.cfg.theta_off and self.dwell <= 0:
                self.mode_exploit = False
                self.flips.add(self.t)
                self.dwell = self.cfg.cooldown
        else:
            if self.score >= self.cfg.theta_on and self.dwell <= 0:
                self.mode_exploit = True
                self.flips.add(self.t)
                self.dwell = self.cfg.cooldown
        if self.dwell > 0:
            self.dwell -= 1

    def select(self) -> int:
        self.t += 1
        step_ok = self.mode_exploit or (len(self.rew_hist) < max(5, self.cfg.L_hist // 8))
        self.guard.note(step_ok)
        for a in range(self.cfg.n_arms):
            if self.counts[a] == 0:
                return a
        if self.mode_exploit:
            return max(range(self.cfg.n_arms), key=self.means.__getitem__)
        return self.rng.randrange(self.cfg.n_arms)

    def update(self, a: int, r: float) -> None:
        r_bin = 1 if r >= 0.5 else 0
        self._update_headers(r_bin)
        self.counts[a] += 1
        n = self.counts[a]
        q = self.means[a]
        self.means[a] = q + (r - q) / n

    def budget_row(self) -> dict:
        return {"params_bits": 6, "flops_per_step": 4, "memory_bytes": 6}
