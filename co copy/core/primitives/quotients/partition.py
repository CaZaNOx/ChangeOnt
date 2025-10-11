# agents/co/core/primitives/quotients/partition.py
from __future__ import annotations
from typing import Callable, List
from ..types import QuotientMapping

def build_partition(num_symbols: int, classifier: Callable[[int], int]) -> QuotientMapping:
    """
    Build a partition of {0..num_symbols-1} via a classifier that maps each symbol -> class_id.
    """
    if num_symbols <= 0:
        return QuotientMapping(classes=[])
    classes = [int(classifier(i)) for i in range(num_symbols)]
    return QuotientMapping(classes=classes)
