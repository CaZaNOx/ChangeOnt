from __future__ import annotations

class FSMCounterBaseline:  
    """  
    Budget-matched toy baseline:  
    - Keeps a local step counter (agent-internal).  
    - Attempts an exit every 'period' steps (default 12) up to k_cap.  
    - No access to plant oracles; purely local cadence.

    ```
    This is intentionally simple (and weak) to contrast with HAQ’s adaptive behavior.
    """
def __init__(self, period: int = 12, k_cap: int = 24):
    self.period = int(period)
    self.k_cap = int(k_cap)
    self.t = 0
    self.exits_used = 0

def reset(self) -> None:
    self.t = 0
    self.exits_used = 0

def act(self, obs: int, t_global: int = 0) -> int:
    # try a bounded number of exits to avoid degenerate “always exit”
    self.t += 1
    if self.exits_used >= self.k_cap:
        return 0
    if self.t % self.period == 0:
        self.exits_used += 1
        return 1
    return 0

---

from **future** import annotations

class FSMCounter:  
"""  
A tiny hand-coded policy: exit every K steps.  
Acts as a classical baseline for the renewal/marker family.  
"""  
def **init**(self, period: int = 12):  
self.period = int(max(1, period))  
self.t = 0

```
def reset(self):
    self.t = 0

def act(self, obs):
    self.t += 1
    return 1 if (self.t % self.period == 0) else 0