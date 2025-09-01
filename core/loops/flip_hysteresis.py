from future import annotations
from dataclasses import dataclass

@dataclass
class FlipState:
    """
    Hysteresis + cooldown state machine.
    mode ∈ {"EXPLORE","EXPLOIT"}
    """
    theta_on: float = 0.25
    theta_off: float = 0.15
    cooldown_steps: int = 10
    mode: str = "EXPLORE"
    _cooldown_left: int = 0

    def step(self, loop_score_ema: float) -> tuple[str, bool]:
        flipped = False
        if self._cooldown_left > 0:
            self._cooldown_left -= 1
            return self.mode, flipped
        if self.mode == "EXPLORE" and loop_score_ema >= self.theta_on:
            self.mode = "EXPLOIT"
            self._cooldown_left = self.cooldown_steps
            flipped = True
        elif self.mode == "EXPLOIT" and loop_score_ema <= self.theta_off:
            self.mode = "EXPLORE"
            self._cooldown_left = self.cooldown_steps
            flipped = True
        return self.mode, flipped
    

    from **future** import annotations  
from typing import Literal, Optional, List, Tuple

Mode = Literal["EXPLORE", "EXPLOIT"]

class FlipController:  
"""  
Hysteresis flip controller with cooldown as specified:  
- theta_on = 0.25, theta_off = 0.15  
- cooldown steps after flip  
- track flips (time, new_mode)  
MC-debt check is supplied by caller (boolean).  
"""  
def **init**(self,  
theta_on: float = 0.25,  
theta_off: float = 0.15,  
cooldown: int = 10):  
self.theta_on = float(theta_on)  
self.theta_off = float(theta_off)  
self.cooldown = int(cooldown)  
self.mode: Mode = "EXPLORE"  
self._cool_left: int = 0  
self.flips: List[Tuple[int, Mode]] = []

```
def step(self, t: int, loop_score_ema: float, mc_debt_ok: bool) -> Mode:
    # Handle cooldown
    if self._cool_left > 0:
        self._cool_left -= 1
        return self.mode

    if self.mode == "EXPLORE":
        if loop_score_ema >= self.theta_on and mc_debt_ok:
            self.mode = "EXPLOIT"
            self._cool_left = self.cooldown
            self.flips.append((t, self.mode))
    else:  # EXPLOIT
        if loop_score_ema <= self.theta_off:
            self.mode = "EXPLORE"
            self._cool_left = self.cooldown
            self.flips.append((t, self.mode))

    return self.mode