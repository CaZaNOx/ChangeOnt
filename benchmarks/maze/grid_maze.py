from future import annotations  
from dataclasses import dataclass  
from typing import Tuple

@dataclass  
class MazeConfig:  
    width: int = 7  
    height: int = 7  
    seed: int = 7

class GridMaze:  
    """  
    Placeholder maze (not wired into experiments yet).  
    """  
    def init(self, cfg: MazeConfig):  
        self.cfg = cfg  
        self.t = 0


        -----

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