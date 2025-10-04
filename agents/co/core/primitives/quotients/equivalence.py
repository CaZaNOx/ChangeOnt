# agents/co/core/primitives/quotients/equivalence.py
from __future__ import annotations
from typing import List
from ..types import QuotientMapping

def trivial_equivalence(num_symbols: int) -> QuotientMapping:
    """
    Identity partition: each symbol is its own class (class_id = symbol).
    """
    if num_symbols <= 0:
        return QuotientMapping(classes=[])
    return QuotientMapping(classes=list(range(num_symbols)))
