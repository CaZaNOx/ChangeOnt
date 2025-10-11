# P14_depth_breadth_flip.py
from dataclasses import dataclass

@dataclass
class Spread:
    mu: float
    breadth: float
    depth: float

class DepthBreadthFlip:
    """
    CO P14: swap (breadth, depth) under specified trigger/rate.
    Skeleton: flip partially with max_rate; always returns a Spread, never raises.
    """
    def __init__(self, max_rate: float = 0.5):
        self.max_rate = max(0.0, min(1.0, float(max_rate)))

    def flip(self, s: Spread, trigger: bool) -> Spread:
        if not trigger:
            return s
        rate = self.max_rate
        b = s.breadth
        d = s.depth
        # partial swap
        nb = (1 - rate) * b + rate * d
        nd = (1 - rate) * d + rate * b
        return Spread(mu=s.mu, breadth=nb, depth=nd)

__all__ = ["DepthBreadthFlip", "Spread"]
