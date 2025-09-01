from future import annotations  
from dataclasses import dataclass  
from typing import List  
import random

@dataclass  
class BanditConfig:  
    arms: int = 4  
    T_max: int = 1000  
    seed: int = 123  
    change_points: List[int] = None # e.g., [300, 600]  
    means_grid: List[List[float]] = None # one list per regime, len==arms

class NonStationaryBandit:  
    """  
    Minimal drifting-bandit scaffold (for future rung).  
    Not yet wired into experiments; included to stabilize imports.  
    """  
    def init(self, cfg: BanditConfig):  
        self.cfg = cfg  
        self.rng = random.Random(cfg.seed)  
        self.t = 0  
        self.done = False  
        self.regime_idx = 0  
        if cfg.change_points is None: cfg.change_points = []  
        if cfg.means_grid is None: cfg.means_grid = [[0.5]*cfg.arms]  
        assert len(cfg.means_grid[0]) == cfg.arms


    def _current_means(self):
        return self.cfg.means_grid[self.regime_idx]

    def step(self, action: int):
        if self.done: raise StopIteration
        # regime switch?
        if self.regime_idx < len(self.cfg.change_points) and self.t >= self.cfg.change_points[self.regime_idx]:
            self.regime_idx += 1
            self.regime_idx = min(self.regime_idx, len(self.cfg.means_grid)-1)
        # reward
        means = self._current_means()
        p = max(0.0, min(1.0, means[action % self.cfg.arms]))
        reward = 1.0 if self.rng.random() < p else 0.0
        self.t += 1
        self.done = (self.t >= self.cfg.T_max)
        return None, reward, self.done, {}
    

    ----

    from **future** import annotations  
import math  
import random  
from dataclasses import dataclass  
from typing import Tuple, Dict, Any

@dataclass  
class BanditCfg:  
K:int=5  
T:int=1000  
drift_amp: float = 0.4 # amplitude of sinusoidal drift  
drift_period: float = 200 # steps per cycle  
base: float = 0.4  
noise: float = 0.05  
seed:int=1729

class DriftingBandit:  
"""  
K-armed bandit with nonstationary Bernoulli means:  
p_t(a) = base + drift_amp * sin(2π (t + phase_a)/period) + noise  
"""  
def **init**(self, cfg: BanditCfg):  
self.cfg = cfg  
self.rng = random.Random(cfg.seed)  
self.t = 0  
self.phases = [self.rng.random() * cfg.drift_period for _ in range(cfg.K)]

```
def reset(self) -> Tuple[int, float, bool, Dict[str, Any]]:
    self.t = 0
    return 0, 0.0, False, {}

def step(self, action: int) -> Tuple[int, float, bool, Dict[str, Any]]:
    self.t += 1
    a = max(0, min(self.cfg.K - 1, int(action)))
    p = self._p(a, self.t)
    reward = 1.0 if self.rng.random() < p else 0.0
    done = (self.t >= self.cfg.T)
    return 0, reward, done, {"p": p, "a": a}

def _p(self, a: int, t: int) -> float:
    s = math.sin(2.0 * math.pi * (t + self.phases[a]) / self.cfg.drift_period)
    p = self.cfg.base + self.cfg.drift_amp * s + self.rng.uniform(-self.cfg.noise, self.cfg.noise)
    return float(min(0.99, max(0.01, p)))