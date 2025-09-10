from future import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class ComplexTurn:
    """
    Smooth turn on the breadth–depth plane.
    Maintains latent 'z' ∈ [-1,1] and momentum μ.
    Discrete φ choices approximate a rotation toward local regret gradient (handled by caller).
    """
    eta: float = 0.25
    momentum: float = 0.80
    z: float = 0.0

    def update(self, gradient: float) -> float:
        """
        gradient > 0 suggests turning toward breadth; < 0 toward depth.
        """
        self.z = float(self.momentum * self.z + self.eta * gradient)
        self.z = max(-1.0, min(1.0, self.z))
        return self.z

    @staticmethod
    def choose_phi(candidates: List[float], regret_estimates: List[float]) -> float:
        """
        Pick φ from candidates minimizing estimated short-horizon regret.
        """
        if not candidates or not regret_estimates or len(candidates) != len(regret_estimates):
            return 0.0
        i = min(range(len(candidates)), key=lambda k: regret_estimates[k])
        return float(candidates[i])
    




    from **future** import annotations  
from typing import Callable, List, Tuple

class ComplexTurn:  
"""  
Smooth turn on breadth-depth plane:  
- maintain vector z with momentum μ and step η, clip |z| <= 1  
- select φ ∈ {0, π/2, π, 3π/2} by minimizing short-horizon regret (H=20)  
Caller provides 'estimate_regret(phi_radians) -> float' for a one-step heading.  
"""  
def **init**(self,  
eta: float = 0.25,  
mu: float = 0.80,  
phi_choices: Tuple[float, ...] = (0.0, 1.57079632679, 3.14159265359, 4.71238898038),  
clip: float = 1.0):  
self.eta = float(eta)  
self.mu = float(mu)  
self.phi_choices = tuple(phi_choices)  
self.clip = float(clip)  
self.zx = 0.0  
self.zy = 0.0  
self.last_phi = 0.0

```
def _clip(self) -> None:
    mag = (self.zx * self.zx + self.zy * self.zy) ** 0.5
    if mag > self.clip and mag > 0:
        self.zx *= self.clip / mag
        self.zy *= self.clip / mag

def propose(self, dirx: float, diry: float,
            estimate_regret: Callable[[float], float]) -> float:
    """
    Update steering vector with direction (dirx, diry) (e.g., gradient in b-d plane),
    then choose φ minimizing estimated regret.
    """
    self.zx = self.mu * self.zx + self.eta * float(dirx)
    self.zy = self.mu * self.zy + self.eta * float(diry)
    self._clip()

    # evaluate regrets at discrete headings
    best_phi = self.phi_choices[0]
    best_reg = float("inf")
    for phi in self.phi_choices:
        r = float(estimate_regret(phi))
        if r < best_reg:
            best_reg = r
            best_phi = phi

    self.last_phi = float(best_phi)
    return self.last_phi