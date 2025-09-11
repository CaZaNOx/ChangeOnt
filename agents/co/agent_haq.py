from __future__ import annotations  
from dataclasses import dataclass, field  
from typing import Callable, Deque, Dict, Hashable, List, Optional, Tuple  
from collections import deque, defaultdict  
import math  
import numpy as np

from agents.co.core.quotient.merge_rules import merge_pass  
from agents.co.core.quotient.infimum_lift import lift_edge_cost, cycle_cost_with_witness  
from agents.co.core.loops.loop_measure import loop_score_ema  
from agents.co.core.loops.cycle_search import karp_min_mean_cycle, johnson_simple_cycles_limited  
from agents.co.core.loops.hysteresis_math import FlipState  
from agents.co.core.loops.mc_depth import paired_mc_delta_regret  
from agents.co.core.headers.collapse import CollapseGuard  
from agents.co.core.headers.density import compute_density_signals, density_header_decision  
from agents.co.core.headers.meta_flip import MetaFlip  
from agents.co.core.headers.complex_turn import ComplexTurn

Float = np.float32
from __future__ import annotations  
from dataclasses import dataclass  
from typing import List  
import math

@dataclass  
class HAQConfig:  
    seed: int = 31415  
    theta_on: float = 0.25  
    theta_off: float = 0.15  
    cooldown: int = 10  
    leak: float = 0.001 # Ï  
    lambda_pe: float = 1.0 # Î»  
    beta_eu: float = 0.8 # Î²  
    ema_gamma: float = 0.90 # loop_score EMA  
    # Robbinsâ€“Monro: Î±_t = (t + c)^{-p}  
    rm_c: float = 50.0  
    rm_p: float = 0.6

class EnhancedHAQAgent:  
    """  
    Minimal, CO-aligned HAQ agent:  
    - Per-token gauge g[u] updated by Robbinsâ€“Monro with PE/EU proxies.  
    - Loop score s = (C_leave - C_stay)/(abs(C_leave)+abs(C_stay)+eps) with  
    cheap surrogates tied to the gauge.  
    - Hysteresis + cooldown flip logic; logs flip times.  
    This is intentionally light so it runs in small environments; it respects  
    the specâ€™s spirit without heavy cycle enumeration (kept for later rungs).  
    """  
    def init(self, A: int, config: HAQConfig = HAQConfig()):  
        self.A = int(A)  
        self.cfg = config  
        self.g = [0.0 for _ in range(self.A)]  
        self.t = 0  
        self.mode = "EXPLORE"  
        self.cooldown_left = 0  
        self.s_ema = 0.0  
        self.flips: List[int] = []

    
# --- life-cycle ---
def reset(self) -> None:
    self.g = [0.0 for _ in range(self.A)]
    self.t = 0
    self.mode = "EXPLORE"
    self.cooldown_left = 0
    self.s_ema = 0.0
    self.flips.clear()

# --- helpers ---
def _alpha_t(self) -> float:
    return (self.t + self.cfg.rm_c) ** (-self.cfg.rm_p)

def _update_gauge(self, tok: int) -> None:
    # PE proxy: novelty = 1 - g[tok]; EU proxy: higher gauge â†’ better stay
    pe = 1.0 - max(0.0, min(1.0, self.g[tok]))
    eu = max(0.0, min(1.0, self.g[tok]))
    a = self._alpha_t()
    self.g[tok] = max(0.0, min(
        1.0,
        self.g[tok] + a * (self.cfg.lambda_pe * pe - self.cfg.beta_eu * eu - self.cfg.leak * self.g[tok])
    ))

def _loop_score(self, tok: int) -> float:
    # Surrogates tied to gauge:
    #   stay cost â†“ with gauge; leave cost ~ average complement of gauge
    eps = 1e-6
    c_stay = 1.0 - self.g[tok]
    avg_g = sum(self.g) / len(self.g) if self.g else 0.0
    c_leave = 1.0 - avg_g
    raw = (c_leave - c_stay) / (abs(c_leave) + abs(c_stay) + eps)
    self.s_ema = self.cfg.ema_gamma * self.s_ema + (1.0 - self.cfg.ema_gamma) * raw
    return self.s_ema

# --- policy ---
def act(self, obs: int, t_global: int = 0) -> int:
    # update internal time, gauge, score
    self.t += 1
    self._update_gauge(obs)
    s = self._loop_score(obs)

    # hysteresis + cooldown
    flip = False
    if self.cooldown_left > 0:
        self.cooldown_left -= 1
    else:
        if self.mode == "EXPLORE" and s >= self.cfg.theta_on:
            self.mode = "EXPLOIT"; flip = True; self.cooldown_left = self.cfg.cooldown
        elif self.mode == "EXPLOIT" and s <= self.cfg.theta_off:
            self.mode = "EXPLORE"; flip = True; self.cooldown_left = self.cfg.cooldown

    if flip:
        self.flips.append(t_global)

    # action: in EXPLOIT, attempt periodic exits (12); else, continue
    if self.mode == "EXPLOIT":
        # cadence modestly accelerated by confidence (gauge near 1 on obs)
        period = 12
        return 1 if (self.t % period == 0) else 0
    return 0
