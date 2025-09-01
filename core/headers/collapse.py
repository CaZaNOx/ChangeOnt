from future import annotations
from dataclasses import dataclass, field
from collections import deque
from math import log2
from typing import Deque, List, Tuple

def _entropy_bits(labels: List[int]) -> float:
    if not labels:
        return 0.0
    total = float(len(labels))
    counts = {}
    for x in labels:
        counts[x] = counts.get(x, 0) + 1
        H = 0.0
        for c in counts.values():
            p = c / total
        if p > 0:
            H -= p * log2(p)
    return float(H)

@dataclass
class CollapseGuard:
    """
    Collapse to 'classical' when:
    H(y|class) ≤ H_thresh bits AND variance fraction ≤ var_frac over W steps.
    """
    W: int = 200
    H_thresh: float = 0.10
    var_frac: float = 0.05
    _labels: Deque[int] = field(default_factory=lambda: deque(maxlen=200))
    _costs: Deque[float] = field(default_factory=lambda: deque(maxlen=200))
    collapsed: bool = False

    def update(self, class_label: int, perceived_cost: float) -> Tuple[bool, float, float]:
        self._labels.append(int(class_label))
        self._costs.append(float(perceived_cost))
        if len(self._labels) < self.W:
            return self.collapsed, 0.0, 1.0
        H = _entropy_bits(list(self._labels))
        costs = list(self._costs)
        mean = sum(costs) / len(costs)
        var = sum((c - mean) ** 2 for c in costs) / max(1, len(costs) - 1)
        frac = var / (abs(mean) + 1e-6)
        now_collapse = (H <= self.H_thresh) and (frac <= self.var_frac)
        # auto un-collapse when condition broken
        if now_collapse:
            self.collapsed = True
        elif self.collapsed and not now_collapse:
            self.collapsed = False
        return self.collapsed, H, frac
    

    from **future** import annotations  
from typing import Deque, Tuple, Optional  
from collections import deque  
import math

class CollapseHeader:  
"""  
Collapse-to-classical header:  
- window W=200  
- collapse if H(y|class) <= 0.10 bits AND var(cost)/|mean(cost)| <= 0.05  
- require both conditions true for the whole window  
- auto un-collapse when either bound violated twice consecutively  
"""  
def **init**(self,  
W: int = 200,  
H_bits_thresh: float = 0.10,  
var_frac_thresh: float = 0.05):  
self.W = int(W)  
self.H_bits_thresh = float(H_bits_thresh)  
self.var_frac_thresh = float(var_frac_thresh)  
self._labels: Deque[int] = deque(maxlen=W)  
self._costs: Deque[float] = deque(maxlen=W)  
self._collapsed: bool = False  
self._unfreeze_strikes: int = 0

```
@staticmethod
def _entropy_bits(labels: Deque[int]) -> float:
    if not labels:
        return 0.0
    counts = {}
    for x in labels:
        counts[x] = counts.get(x, 0) + 1
    total = float(len(labels))
    H = 0.0
    for c in counts.values():
        p = c / total
        if p > 0:
            H -= p * math.log2(p)
    return float(H)

@staticmethod
def _var_frac(costs: Deque[float]) -> float:
    n = len(costs)
    if n < 2:
        return 0.0
    mean = sum(costs) / n
    var = sum((x - mean) * (x - mean) for x in costs) / (n - 1)
    denom = abs(mean) + 1e-6
    return float(var / denom)

def update(self, class_label: int, perceived_cost: float) -> bool:
    """
    Push one observation and return current collapsed state.
    """
    self._labels.append(int(class_label))
    self._costs.append(float(perceived_cost))

    if len(self._labels) < self.W:
        return self._collapsed

    H = self._entropy_bits(self._labels)
    vf = self._var_frac(self._costs)

    should_collapse = (H <= self.H_bits_thresh) and (vf <= self.var_frac_thresh)

    if should_collapse:
        self._collapsed = True
        self._unfreeze_strikes = 0
    else:
        # if already collapsed, require two consecutive breaches to un-collapse
        if self._collapsed:
            self._unfreeze_strikes += 1
            if self._unfreeze_strikes >= 2:
                self._collapsed = False
                self._unfreeze_strikes = 0
        else:
            self._collapsed = False

    return self._collapsed