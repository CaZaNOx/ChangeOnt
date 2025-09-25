# PATH: agents/co/agent_maze.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from random import Random

from agents.co.core.headers.loop_score import loop_score_ema
from agents.co.core.headers.density import compute_density_signals
from agents.co.core.headers.meta_flip import MetaFlip
from agents.co.core.headers.collapse import CollapseGuard

Pos = Tuple[int, int]
Action = str  # "UP"|"DOWN"|"LEFT"|"RIGHT"

DIRS: List[Action] = ["UP", "DOWN", "LEFT", "RIGHT"]
LEFT_OF = {"UP": "LEFT", "LEFT": "DOWN", "DOWN": "RIGHT", "RIGHT": "UP"}
RIGHT_OF = {v: k for k, v in LEFT_OF.items()}  # inverse

@dataclass
class COMazeCfg:
    A: int = 8
    L_hist: int = 128
    ema_beta: float = 0.9
    theta_on: float = 0.6
    theta_off: float = 0.4
    cooldown: int = 20
    seed: int = 0

@dataclass
class COMazeAgent:
    """
    CO-aligned maze agent using only (obs, reward, done) stream.
    Learns local 'blocked' actions by detecting stationary outcomes; never peeks the map.
    """
    cfg: COMazeCfg
    rng: Random = field(init=False)

    # header state over reward stream
    rew_hist: List[int] = field(default_factory=list)
    score: float = field(default=0.0, init=False)
    mode_exploit: bool = field(default=False, init=False)
    dwell: int = field(default=0, init=False)
    flips: MetaFlip = field(default_factory=MetaFlip)
    guard: CollapseGuard = field(default_factory=CollapseGuard)

    # episodic state
    t: int = field(default=0, init=False)
    pos: Optional[Pos] = field(default=None, init=False)
    last_pos: Optional[Pos] = field(default=None, init=False)
    last_act: Optional[Action] = field(default=None, init=False)

    # learned local topology: at position p -> set of blocked actions
    blocked: Dict[Pos, set] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.rng = Random(self.cfg.seed)

    def start_episode(self, init_obs: Pos) -> None:
        self.rew_hist.clear()
        self.score = 0.0
        self.mode_exploit = False
        self.dwell = 0
        self.flips.reset()
        self.guard.reset()

        self.t = 0
        self.pos = init_obs
        self.last_pos = init_obs
        self.last_act = None
        self.blocked.clear()

    # --- headers on reward stream ---
    def _push_reward(self, reward: float) -> None:
        # bin: -1 -> 0, 0 -> 1 (goal)
        r_bin = 1 if reward >= -1e-12 else 0
        self.rew_hist.append(r_bin)

        # density/loop-score update
        _, dens = compute_density_signals(
            self.rew_hist[-self.cfg.L_hist:],
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

    def _mark_blocked_if_needed(self, new_pos: Pos) -> None:
        if self.last_act is None or self.last_pos is None:
            return
        if new_pos == self.last_pos:
            s = self.blocked.setdefault(self.last_pos, set())
            s.add(self.last_act)

    def _ordered_actions(self) -> List[Action]:
        # First step: random heading
        if self.last_act is None:
            base = DIRS[:]
            self.rng.shuffle(base)
            return base

        if self.mode_exploit:
            # Prefer keeping heading, then right, then left, then back
            straight = self.last_act
            right = RIGHT_OF[self.last_act]
            left = LEFT_OF[self.last_act]
            back = RIGHT_OF[right]  # 180°
            return [straight, right, left, back]
        else:
            # Exploration: rotate canonical order by flip count (no map access)
            k = self.flips.count() % 4
            base = DIRS[:]
            return base[k:] + base[:k]

    def select(self) -> Action:
        self.t += 1
        # collapse guard: cadence is 'safe' during exploit or early ramp
        step_ok = self.mode_exploit or (self.t < max(5, self.cfg.L_hist // 8))
        self.guard.note(step_ok)

        cand = self._ordered_actions()
        bset = self.blocked.get(self.pos, set()) if self.pos is not None else set()
        for a in cand:
            if a not in bset:
                self.last_act = a
                return a
        # Cornered: pick random (env will keep pos; we’ll mark blocked; headers adapt)
        self.last_act = self.rng.choice(DIRS)
        return self.last_act

    def update(self, new_obs: Pos, reward: float, done: bool) -> None:
        if self.pos is not None:
            self._mark_blocked_if_needed(new_obs)
        self._push_reward(reward)
        self.last_pos = self.pos
        self.pos = new_obs

    def budget_row(self) -> dict:
        # Keep parity with BFS runner’s simple ledger
        return {"params_bits": 6, "flops_per_step": 4, "memory_bytes": 6}
