from future import annotations
from dataclasses import dataclass

@dataclass
class MetaFlip:
    """
    Depth↔Breadth meta-policy flip on EMA of (breadth - depth).
    Enforces hysteresis, cooldown, and min-hold.
    """
    beta: float = 0.90
    on: float = 0.20
    off: float = 0.10
    min_hold: int = 15
    cooldown: int = 20
    max_rate: int = 50 # max 1 flip per 50 steps
    ema: float = 0.0
    mode: str = "mixed"
    _hold: int = 0
    _cool: int = 0
    _since_flip: int = 10**9

    def step(self, breadth: float, depth: float) -> tuple[str, bool]:
        delta = float(breadth - depth)
        self.ema = float(self.beta * self.ema + (1.0 - self.beta) * delta)
        flipped = False
        self._hold = max(0, self._hold - 1)
        self._cool = max(0, self._cool - 1)
        self._since_flip += 1

        def can_flip() -> bool:
            return self._hold == 0 and self._cool == 0 and self._since_flip >= self.max_rate

        if self.mode != "breadth" and self.ema >= self.on and can_flip():
            self.mode = "breadth"; flipped = True
            self._hold = self.min_hold; self._cool = self.cooldown; self._since_flip = 0
        elif self.mode != "depth" and self.ema <= -self.on and can_flip():
            self.mode = "depth"; flipped = True
            self._hold = self.min_hold; self._cool = self.cooldown; self._since_flip = 0
        elif self.mode == "breadth" and self.ema <= self.off and can_flip():
            self.mode = "mixed"; flipped = True
            self._hold = self.min_hold; self._cool = self.cooldown; self._since_flip = 0
        elif self.mode == "depth" and self.ema >= -self.off and can_flip():
            self.mode = "mixed"; flipped = True
            self._hold = self.min_hold; self._cool = self.cooldown; self._since_flip = 0

        return self.mode, flipped


from **future** import annotations  
from typing import Literal

class MetaFlipController:  
"""  
Depth↔Breadth meta-flip controller:  
- EMA over Δ = b - d with β=0.9  
- trigger if |Δ| >= 0.20  
- min-hold 15, hysteresis 0.10, cooldown 20, max 1 per 50 steps  
"""  
def **init**(self,  
beta: float = 0.90,  
on_abs: float = 0.20,  
hysteresis: float = 0.10,  
min_hold: int = 15,  
cooldown: int = 20,  
max_per_window: int = 50):  
self.beta = float(beta)  
self.on_abs = float(on_abs)  
self.hysteresis = float(hysteresis)  
self.min_hold = int(min_hold)  
self.cooldown = int(cooldown)  
self.max_per_window = int(max_per_window)

```
    self._ema = 0.0
    self._mode: Literal["breadth", "depth", "mixed"] = "mixed"
    self._since_flip = 0
    self._cool_left = 0
    self._window_countdown = 0  # enforce at most 1 per 50

@property
def mode(self) -> str:
    return self._mode

def step(self, b: float, d: float) -> str:
    self._ema = self.beta * self._ema + (1.0 - self.beta) * float(b - d)
    self._since_flip += 1
    if self._cool_left > 0:
        self._cool_left -= 1
    if self._window_countdown > 0:
        self._window_countdown -= 1

    trigger = abs(self._ema) >= self.on_abs
    if trigger and self._since_flip >= self.min_hold and self._cool_left == 0 and self._window_countdown == 0:
        # flip direction with hysteresis bias
        if self._ema >= (self.on_abs + self.hysteresis):
            self._mode = "breadth"
        elif self._ema <= -(self.on_abs + self.hysteresis):
            self._mode = "depth"
        else:
            self._mode = "mixed"
        self._since_flip = 0
        self._cool_left = self.cooldown
        self._window_countdown = self.max_per_window

    return self._mode
