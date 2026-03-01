from __future__ import annotations
from typing import Optional


class SC_GatedThreshold:
    """
    Semantic combinator: gated threshold.
    Pure function: activates when value crosses threshold (gte by default).
    """
    @staticmethod
    def activate(
        value: float,
        threshold: float,
        gate_ok: bool = True,
        direction: str = "gte",
    ) -> bool:
        if not gate_ok:
            return False
        v = float(value)
        t = float(threshold)
        if direction == "lte":
            return v <= t
        return v >= t

    @staticmethod
    def gated_value(
        value: float,
        threshold: float,
        gate_ok: bool = True,
        direction: str = "gte",
        off_value: float = 0.0,
    ) -> float:
        return float(value) if SC_GatedThreshold.activate(value, threshold, gate_ok, direction) else float(off_value)
