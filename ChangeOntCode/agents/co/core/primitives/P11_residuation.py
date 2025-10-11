# P11_residuation.py
from typing import Callable

class Residuation:
    """
    CO P11: residuated 'division' over (min,+) style costs.
    Implements implication a⇒b ≈ max(0, b - a) and a right-residual of convolution.
    """
    @staticmethod
    def imply(a: float, b: float) -> float:
        try:
            return max(0.0, float(b) - float(a))
        except Exception:
            return float("inf")

    @staticmethod
    def right_residual(f_cost: Callable[[int, int], float],
                       d_cost: Callable[[int, int], float],
                       w: int, z: int, domain: range) -> float:
        """
        h(w,z) = sup_u ( d(u,z) - f(w,u) )
        Safe: returns +inf if domain empty; no throws.
        """
        vals = []
        for u in domain:
            try:
                vals.append(d_cost(u, z) - f_cost(w, u))
            except Exception:
                continue
        return max(vals) if vals else float("inf")

__all__ = ["Residuation"]
