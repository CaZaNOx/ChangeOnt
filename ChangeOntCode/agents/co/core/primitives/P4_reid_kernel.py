# P4_reid_kernel.py
from typing import Iterable, Callable, Dict, Any, Tuple

class ReIDKernel:
    """
    CO P04: Re-identification frequency / probability kernel.
    Computes how often windows re-identify with a template under a bend budget.
    Safe skeleton: returns zero if no matcher provided; never raises.
    """
    def __init__(self, epsilon: float = 0.0, window: int = 5):
        self.epsilon = max(0.0, float(epsilon))
        self.window = max(1, int(window))

    def frequency(self,
                  stream: Iterable[Any],
                  template: Iterable[Any],
                  match_cost: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float]) -> float:
        """Return fraction in [0,1]. Falls back to 0 if input is empty."""
        buf = []
        total = 0
        hits = 0
        tmpl = tuple(template)
        k = self.window
        for x in stream:
            buf.append(x)
            if len(buf) >= k:
                win = tuple(buf[-k:])
                total += 1
                try:
                    cost = match_cost(win, tmpl)
                except Exception:
                    cost = float("inf")
                if cost <= self.epsilon:
                    hits += 1
        return (hits / total) if total > 0 else 0.0

__all__ = ["ReIDKernel"]
