# agents/co/core/context/math_context.py
from dataclasses import dataclass, asdict
from typing import Literal, Dict, Any

PathAlg = Literal["classical", "minplus"]
NumArith = Literal["classic", "spread"]
LogicAlg = Literal["boolean", "quantale"]

@dataclass
class MathContext:
    """Three algebraic dials controlled by headers."""
    path_algebra: PathAlg = "classical"
    number_arith: NumArith = "classic"
    logic: LogicAlg = "boolean"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HeaderState:
    """
    Runtime header state shared across elements.
    - tag: reporting regime (CS/ID/SSI)
    - dyn: dynamicity knob in [0,1]
    - effective params are bounded by static ranges the header sets.
    """
    tag: Literal["CS","ID","SSI"] = "CS"
    dyn: float = 0.0
    # Static ranges (filled by header on configure)
    tau_range: tuple[float, float] = (0.0, 0.0)
    eps_range: tuple[float, float] = (0.0, 0.0)
    alpha_cap_range: tuple[float, float] = (0.0, 0.0)
    gamma_range: tuple[float, float] = (0.0, 0.0)
    cooldown_range: tuple[int, int] = (0, 0)

    # Effective (derived each step)
    tau_eff: float = 0.0
    eps_eff: float = 0.0
    alpha_cap: float = 0.0
    gamma_eff: float = 0.0
    cooldown_eff: int = 0
    r_prime: int = 0
    p_breadth: float = 0.0

    def derive_effective(self, r_prime_static: int = 1, p_breadth_bounds=(0.1,0.7)) -> None:
        """Map dyn∈[0,1] into effective parameters within header ranges."""
        lo, hi = self.tau_range; self.tau_eff = lo + self.dyn*(hi-lo)
        lo, hi = self.eps_range; self.eps_eff = lo + self.dyn*(hi-lo)
        lo, hi = self.alpha_cap_range; self.alpha_cap = lo + self.dyn*(hi-lo)
        lo, hi = self.gamma_range; self.gamma_eff = hi + (1-self.dyn)*(lo-hi)  # dyn↑ → lower penalty (but ≥ min)
        lo, hi = self.cooldown_range; self.cooldown_eff = int(hi + (1-self.dyn)*(lo-hi))
        pb_lo, pb_hi = p_breadth_bounds; self.p_breadth = pb_lo + self.dyn*(pb_hi-pb_lo)
        # precision policy: start finer in static, coarsen a bit for dynamic then refine adaptively (elements decide)
        self.r_prime = max(0, r_prime_static - int(self.dyn > 0.5))
