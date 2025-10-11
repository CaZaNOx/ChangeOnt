# P12_closure_quotient.py
from typing import Iterable, Dict, Any, Callable, Set, Tuple

class ClosureQuotient:
    """
    CO P12: ε-closure & HAQ quotient (≈_{A,ε}).
    Builds equivalence classes under a tolerance and (optionally) a gauge-weighted distance.
    """
    def __init__(self, epsilon: float = 0.0):
        self.epsilon = max(0.0, float(epsilon))

    def closure(self,
                items: Iterable[Any],
                dist: Callable[[Any, Any], float]) -> Dict[Any, Set[Any]]:
        """Return map: representative -> class members"""
        items = list(items)
        classes: Dict[Any, Set[Any]] = {}
        seen: Set[Any] = set()
        for x in items:
            if x in seen:
                continue
            rep = x
            cls = {x}
            for y in items:
                if y in seen:
                    continue
                try:
                    if dist(x, y) <= self.epsilon:
                        cls.add(y)
                except Exception:
                    continue
            for y in cls:
                seen.add(y)
            classes[rep] = cls
        return classes

    def quotient(self,
                 edges: Iterable[Tuple[Any, Any]],
                 dist: Callable[[Any, Any], float]) -> Dict[Any, Set[Any]]:
        """Treat nodes as items; ignores edge labels here; safe skeleton."""
        nodes = set()
        for u, v in edges:
            nodes.add(u); nodes.add(v)
        return self.closure(nodes, dist)

__all__ = ["ClosureQuotient"]
