# experiments/env.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict, Any, List
import random

@dataclass
class EnvCfg:
    A: int = 8          # alphabet size |Σ|
    L_win: int = 6      # code length / window
    p_ren: float = 0.02 # renewal probability
    p_merge: float = 0.0
    p_split: float = 0.0
    p_noise: float = 0.0
    p_adv: float = 0.0
    T_max: int = 1000
    k: int = 6          # kept for compatibility

class CodebookRenewalEnvW:
    """
    Finite renewal/codebook environment (STOA, CO-independent).
    Observation: current symbol x_t ∈ {0..A-1}
    Action: predicted next symbol â_t ∈ {0..A-1}
    Reward: 1 if â_t == x_{t+1}, else 0
    """
    def __init__(self, cfg: EnvCfg, seed: int = 7):
        self.cfg = cfg
        self._rng = random.Random(seed)
        self._t = 0
        self._code: List[int] = self._new_code()
        self._idx = 0
        self._obs = self._code[0]

    def reset(self) -> Tuple[int, float, bool, Dict[str, Any]]:
        self._t = 0
        self._code = self._new_code()
        self._idx = 0
        self._obs = self._code[0]
        return self._obs, 0.0, False, {"t": self._t}

    def step(self, action: int) -> Tuple[int, float, bool, Dict[str, Any]]:
        c = self.cfg
        # renewal event
        if self._rng.random() < c.p_ren:
            self._code = self._new_code()
            self._idx = 0
        # nominal next symbol
        nxt = self._code[(self._idx + 1) % c.L_win]
        # optional noise
        if self._rng.random() < c.p_noise:
            nxt = self._rng.randrange(0, c.A)
        reward = 1.0 if int(action) == nxt else 0.0
        # advance
        self._idx = (self._idx + 1) % c.L_win
        self._obs = nxt
        self._t += 1
        done = self._t >= c.T_max
        info = {"t": self._t}
        return self._obs, reward, done, info

    def _new_code(self) -> List[int]:
        return [self._rng.randrange(0, self.cfg.A) for _ in range(self.cfg.L_win)]
