# agents/co/core/primitives/state_naming.py
from __future__ import annotations
from typing import Iterable, List

def humanize_states(states: Iterable[int], prefix: str = "S") -> List[str]:
    """
    Map integer state IDs -> strings like 'S0', 'S1', ...
    """
    out: List[str] = []
    for s in states:
        s2 = int(s)
        if s2 < 0:
            raise ValueError(f"state id must be non-negative, got {s2}")
        out.append(f"{prefix}{s2}")
    return out
