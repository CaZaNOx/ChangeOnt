# J4a_reid_closure.py
from typing import Tuple, Any, Callable

def within_epsilon(a: Tuple[Any, ...],
                   b: Tuple[Any, ...],
                   epsilon: float,
                   dist: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float]) -> bool:
    try:
        return dist(a, b) <= max(0.0, float(epsilon))
    except Exception:
        return False
