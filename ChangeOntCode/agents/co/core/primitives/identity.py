# agents/co/core/primitives/identity.py
from __future__ import annotations
from typing import Iterable, List, Tuple, Deque, Any
from collections import deque
from .P1_bend_metric import bend_distance, closure

def same(path: Iterable, other: Iterable, eps: float) -> bool:
    return bend_distance(path, other) <= eps

class TraceMemory:
    """Small FIFO memory of recent traces for identity checks."""
    def __init__(self, maxlen: int = 16):
        self.maxlen = max(1, int(maxlen))
        self._buf: Deque[Tuple[Any, ...]] = deque(maxlen=self.maxlen)
        self.last_action: Any | None = None

    def push(self, trace: Tuple[Any, ...]) -> None:
        if trace:
            self._buf.append(tuple(trace))

    def traces(self) -> List[Tuple[Any, ...]]:
        return list(self._buf)

__all__ = ["bend_distance", "same", "closure", "TraceMemory"]
