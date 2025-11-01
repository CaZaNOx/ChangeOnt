# J3_attention_warp.py
from typing import Callable, Any

def warp_cost(base_cost: Callable[[Any, Any], float],
              gauge: Callable[[Any, Any], float] | None,
              alpha: float = 0.0) -> Callable[[Any, Any], float]:
    """
    Wrap a cost with attention/gauge: c' = max(0, c - alpha * A).
    Returns a callable; safe for None gauge.
    """
    a = max(0.0, float(alpha))
    def _c(u: Any, v: Any) -> float:
        try:
            c = float(base_cost(u, v))
        except Exception:
            c = float("inf")
        g = 0.0
        if gauge is not None:
            try:
                g = float(gauge(u, v))
            except Exception:
                g = 0.0
        return max(0.0, c - a * g)
    return _c
