# J1_bend_substitution.py
from typing import Tuple, Any, Callable

def bend_cost_between(a: Tuple[Any, ...],
                      b: Tuple[Any, ...],
                      local_cost: Callable[[Any, Any], float]) -> float:
    """
    Simple edit-like alignment cost between tuples a,b using substitution-only skeleton.
    Safe: falls back to length diff when local_cost throws.
    """
    if len(a) != len(b):
        return float(abs(len(a) - len(b)))
    total = 0.0
    for x, y in zip(a, b):
        try:
            total += float(local_cost(x, y))
        except Exception:
            total += 1.0 if x != y else 0.0
    return total
