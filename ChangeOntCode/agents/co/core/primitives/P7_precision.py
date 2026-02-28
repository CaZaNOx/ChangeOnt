# agents/co/core/primitives/P7_precision.py
from typing import Dict, Optional

def precision_schedule(stats: Dict, mode: str = "fixed") -> int:
    """
    Return r' (rounding precision or discretization level).
    Modes: 'fixed' -> 1, 'coarse' -> 0, 'adaptive' -> changes with surprise.
    """
    if mode == "coarse": return 0
    if mode == "adaptive":
        z = float(stats.get("surprise", 0.0))
        return 0 if z > 1.0 else 1
    return 1


class P7_Precision:
    """
    Minimal precision scheduling primitive wrapper.
    Holds last precision and exposes a small runtime API for elements.
    """
    def __init__(self, mode: str = "fixed", r_static: int = 1):
        self.mode = str(mode)
        self.r_static = int(r_static)
        self.last_r = int(r_static)

    def configure(self, params: Optional[Dict] = None):
        if params:
            if "mode" in params:
                self.mode = str(params["mode"])
            if "r_static" in params:
                self.r_static = int(params["r_static"])
        return self

    def schedule(self, stats: Dict, mode: Optional[str] = None, r_static: Optional[int] = None) -> int:
        use_mode = self.mode if mode is None else str(mode)
        if r_static is not None:
            self.r_static = int(r_static)
        # keep scheduling law centralized here
        r_p = precision_schedule(stats, use_mode)
        self.last_r = int(r_p)
        return int(r_p)

def tighten(spreads: Dict[str, tuple], kappa: float) -> Dict[str, tuple]:
    """Shrink depth spread; placeholder no-op except scale by (1-kappa)."""
    out = {}
    for k, (mu, b, d) in spreads.items():
        out[k] = (mu, b, max(0.0, d * (1.0 - kappa)))
    return out

def loosen(spreads: Dict[str, tuple], kappa: float) -> Dict[str, tuple]:
    """Increase depth spread; placeholder scale by (1+kappa)."""
    out = {}
    for k, (mu, b, d) in spreads.items():
        out[k] = (mu, b, d * (1.0 + kappa))
    return out
