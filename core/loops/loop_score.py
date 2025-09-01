# FILE: core/loops/loop_score.py
import numpy as np

def loop_score(cost_leave: float, cost_stay: float, eps: float = 1e-6) -> np.float32:
    """(C_leave - C_stay) / (|C_leave|+|C_stay|+eps)"""
    num = np.float32(cost_leave) - np.float32(cost_stay)
    den = np.abs(np.float32(cost_leave)) + np.abs(np.float32(cost_stay)) + np.float32(eps)
    return np.float32(num / den)

class EMA:
    def __init__(self, beta: float = 0.90):
        self.beta = np.float32(beta)
        self.val = np.float32(0.0)
        self.initialized = False

    def update(self, x: float) -> np.float32:
        x = np.float32(x)
        if not self.initialized:
            self.val = x
            self.initialized = True
        else:
            self.val = self.beta * self.val + (1.0 - self.beta) * x
        return self.val


from **future** import annotations

class LoopScoreEMA:  
"""  
Loop-score with EMA smoothing as specified:  
s_raw = (C_leave - C_stay) / (|C_leave| + |C_stay| + eps)  
s_ema <- gamma*s_ema + (1-gamma)*s_raw  
"""  
def **init**(self, gamma: float = 0.90, eps: float = 1e-6):  
self.gamma = float(gamma)  
self.eps = float(eps)  
self._ema = 0.0

```
@property
def value(self) -> float:
    return self._ema

def update(self, C_leave: float, C_stay: float) -> float:
    denom = abs(C_leave) + abs(C_stay) + self.eps
    s_raw = (C_leave - C_stay) / denom
    self._ema = self.gamma * self._ema + (1.0 - self.gamma) * float(s_raw)
    return self._ema