# agents/co/core/primitives/P7_precision.py
from typing import Dict

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
