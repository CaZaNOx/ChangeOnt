from __future__ import annotations
from typing import Iterable, Sequence, Optional


class SC_AdditiveBlend:
    """
    Semantic combinator: additive accumulation of primitive-derived scalars.
    Pure function: sum_i (w_i * x_i).
    """
    @staticmethod
    def combine(values: Iterable[float], weights: Optional[Sequence[float]] = None) -> float:
        vals = list(values)
        if not vals:
            return 0.0
        if weights is None:
            return float(sum(float(v) for v in vals))
        w = list(weights)
        if len(w) != len(vals):
            # fallback: ignore weights if mismatch
            return float(sum(float(v) for v in vals))
        return float(sum(float(v) * float(wi) for v, wi in zip(vals, w)))
