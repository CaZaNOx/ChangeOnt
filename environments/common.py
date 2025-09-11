from __future__ import annotations  
from dataclasses import dataclass  
from typing import Dict, List, Optional, Tuple  
import random

@dataclass  
class RenewalConfig:  
    A: int = 6  
    L_win: int = 8  
    p_ren: float = 0.08  
    p_merge: float = 0.25  
    p_split: float = 0.15  
    p_noise: float = 0.02  
    p_adv: float = 0.0  
    T_max: int = 600  
    k: int = 12  
    seed: int = 1729

class CodebookRenewalEnvW:  
    """  
    Renewal-with-codebook toy plant:  
    - A visible symbols (0..A-1), latent map 'latents' -> visible heads  
    - stochastic renewals: reshuffle heads; choose new 'marker'  
    - merge/split on heads (palimpsest)  
    - noise & (optional) adversary  
    Reward semantics for this toy: agent chooses action in {0,1}; reward=1 iff it exits  
    exactly on the k-th visit to the current marker (counted since last renewal).  
    """  
    def init(self, cfg: RenewalConfig):  
        self.cfg = cfg  
        self.rng = random.Random(cfg.seed)  
        self.reset()

    
    def reset(self):
        cfg = self.cfg
        self.t = 0
        self.done = False
        # latent -> visible head
        self.latents: List[int] = list(range(cfg.A))
        self.rng.shuffle(self.latents)
        # marker latent and visit counter
        self.marker = self.rng.randrange(cfg.A)
        self.visit = 0
        # last emitted token (for observe)
        self.last_obs = self._emit_obs()
        # event log (times)
        self._event_times: List[int] = []
        return self.last_obs, 0.0, False, {"renewal": True, "kth_opportunity": False, "event_time": 0}

    # ----- internals -----
    def _renew(self):
        self.rng.shuffle(self.latents)
        self.marker = self.rng.randrange(self.cfg.A)
        self.visit = 0
        self._event_times.append(self.t)  # renewal event

    def _merge(self):
        cfg = self.cfg
        if cfg.A < 2:
            return
        i, j = self.rng.sample(range(cfg.A), 2)
        self.latents[j] = self.latents[i]

    def _split(self):
        cfg = self.cfg
        j = self.rng.randrange(cfg.A)
        self.latents[j] = self.rng.randrange(cfg.A)

    def _emit_obs(self) -> int:
        cfg = self.cfg
        latent = self.rng.randrange(cfg.A)
        token = self.latents[latent]
        # adversary (disabled by default)
        if self.rng.random() < cfg.p_adv:
            alt = self.rng.randrange(cfg.A)
            token = alt
        # noise
        if self.rng.random() < cfg.p_noise:
            token = self.rng.randrange(cfg.A)
        return token

    # ----- API -----
    def step(self, action: int):
        if self.done:
            raise StopIteration("episode finished")
        cfg = self.cfg

        # renewal?
        renewal_fired = False
        if self.rng.random() < cfg.p_ren:
            self._renew()
            renewal_fired = True

        # merge/split?
        r = self.rng.random()
        if r < cfg.p_merge:
            self._merge()
        elif r < cfg.p_merge + cfg.p_split:
            self._split()

        # emit obs
        obs = self._emit_obs()

        # opportunity count (by latent marker)
        kth = False
        # infer latent index that produced obs is hidden; we use the plant latent for marker accounting only
        # IMPORTANT: this is plant-internal; not visible to agents
        if self.latents[self.marker] == obs:
            self.visit += 1
            if self.visit == cfg.k:
                kth = True
                self._event_times.append(self.t)

        # reward on correct exit-timing only
        reward = 1.0 if (action == 1 and kth) else 0.0

        # step bookkeeping
        info = {
            "t": self.t,
            "obs": obs,
            "marker": self.marker,      # plant-internal (not for agent)
            "renewal": renewal_fired,
            "kth_opportunity": kth,
            "event_time": self.t if (renewal_fired or kth) else None,
        }
        self.t += 1
        self.last_obs = obs
        self.done = (self.t >= cfg.T_max) or (action == 1)  # episode ends on exit attempt or horizon
        return obs, reward, self.done, info

    def event_times(self) -> List[int]:
        return list(self._event_times)
    

    from __future__ import annotations  
import random  
from dataclasses import dataclass  
from typing import Optional, Tuple, Dict, Any

@dataclass  
class RenCfg:  
A:int=6; p_ren:float=0.08; p_merge:float=0.25; p_split:float=0.15  
p_noise:float=0.02; T_max:int=600; k:int=12; seed:int=1729

class CodebookRenewalEnvW:  
"""  
Renewal + palimpsest toy plant.  
obs: token head in [0..A-1], corrupted by noise.  
reward: +1 iff agent exits on the k-th visit to the (hidden) marker since last renewal.  
"""  
def **init**(self, cfg: RenCfg):  
self.cfg = cfg  
self.rng = random.Random(cfg.seed)  
self.reset()

def reset(self) -> Tuple[int, float, bool, Dict[str, Any]]:
    self.t = 0
    self.latents = list(range(self.cfg.A))
    self.rng.shuffle(self.latents)
    self.marker = self.rng.randrange(self.cfg.A)
    self.visit = 0
    self.done = False
    self._roll_obs()
    return self.obs, 0.0, False, {}

def _renew(self):
    self.rng.shuffle(self.latents)
    self.marker = self.rng.randrange(self.cfg.A)
    self.visit = 0

def _merge(self):
    i, j = self.rng.sample(range(self.cfg.A), 2)
    self.latents[j] = self.latents[i]

def _split(self):
    j = self.rng.randrange(self.cfg.A)
    self.latents[j] = self.rng.randrange(self.cfg.A)

def _emit(self) -> int:
    latent = self.rng.randrange(self.cfg.A)
    if latent == self.marker:
        self.visit += 1
    tok = self.latents[latent]
    # noise
    if self.rng.random() < self.cfg.p_noise:
        tok = self.rng.randrange(self.cfg.A)
    return tok

def _roll_obs(self):
    self.obs = self._emit()

def step(self, action: Optional[int]) -> Tuple[int, float, bool, Dict[str, Any]]:
    self.t += 1
    # renewal
    if self.rng.random() < self.cfg.p_ren:
        self._renew()
    # palimpsest edits
    r = self.rng.random()
    if r < self.cfg.p_merge:
        self._merge()
    elif r < self.cfg.p_merge + self.cfg.p_split:
        self._split()
    # emit obs
    self._roll_obs()
    # exit logic
    reward = 0.0
    if action == 1:
        reward = 1.0 if self.visit == self.cfg.k else 0.0
        self.done = True
    if self.t >= self.cfg.T_max:
        self.done = True
    return self.obs, reward, self.done, {}
