from __future__ import annotations
from typing import Iterable, Sequence, Optional


class SC_MultiplicativeCoupling:
    """
    Semantic combinator: multiplicative modulation of one quantity by another.
    Pure function: product_i (x_i ^ w_i) when weights provided, else product of values.
    """
    @staticmethod
    def couple(base: float, mod: float) -> float:
        return float(base) * float(mod)

    @staticmethod
    def combine(values: Iterable[float], weights: Optional[Sequence[float]] = None) -> float:
        vals = list(values)
        if not vals:
            return 0.0
        if weights is None:
            out = 1.0
            for v in vals:
                out *= float(v)
            return float(out)
        w = list(weights)
        if len(w) != len(vals):
            out = 1.0
            for v in vals:
                out *= float(v)
            return float(out)
        out = 1.0
        for v, wi in zip(vals, w):
            out *= float(v) ** float(wi)
        return float(out)
