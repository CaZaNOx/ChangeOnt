# P5_temporal_ops.py
from typing import Callable, Any, Iterable

class TemporalOps:
    """
    CO P05: Temporal operators over a finite path graph under bend-tolerant costs.
    X (next), F (eventually <=k), G (always), U (until) — skeletons that accept
    user-provided reachability/cost predicates. Non-throwing defaults.
    """
    def __init__(self, epsilon: float = 0.0):
        self.epsilon = max(0.0, float(epsilon))

    def X(self, reachable: Callable[[Any], Iterable[Any]], state: Any,
          pred: Callable[[Any], bool]) -> bool:
        for s in reachable(state):
            try:
                if pred(s):
                    return True
            except Exception:
                continue
        return False

    def F_le_k(self, reachable_k: Callable[[Any, int], Iterable[Any]],
               state: Any, k: int, accept: Callable[[Any], bool]) -> bool:
        k = max(0, int(k))
        for s in reachable_k(state, k):
            try:
                if accept(s):
                    return True
            except Exception:
                continue
        return False

    def G(self, reachable_k: Callable[[Any, int], Iterable[Any]],
          state: Any, k: int, safe: Callable[[Any], bool]) -> bool:
        k = max(0, int(k))
        for s in reachable_k(state, k):
            try:
                if not safe(s):
                    return False
            except Exception:
                return False
        return True

    def U(self, reachable_k: Callable[[Any, int], Iterable[Any]],
          state: Any, k: int,
          until_ok: Callable[[Any], bool],
          maintain: Callable[[Any], bool]) -> bool:
        """Maintain holds on all prefixes until until_ok holds at some state within k."""
        k = max(0, int(k))
        for s in reachable_k(state, k):
            try:
                if until_ok(s):
                    return True
                if not maintain(s):
                    return False
            except Exception:
                return False
        return False

__all__ = ["TemporalOps"]
