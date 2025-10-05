# PATH: agents/co/core/headers/meta_flip.py
from __future__ import annotations
from typing import List, Optional

class MetaFlip:
    """
    Minimal flip registry for CO headers.
    - add(t): record a flip at logical step t
    - count(): number of flips so far
    - parity(): 0/1 parity of flips
    - last(): most recent flip index (or None)
    - reset(): clear state
    """
    def __init__(self) -> None:
        self._idx: List[int] = []

    def add(self, t: int) -> None:
        self._idx.append(int(t))

    def count(self) -> int:
        return len(self._idx)

    def parity(self) -> int:
        return len(self._idx) & 1

    def last(self) -> Optional[int]:
        return self._idx[-1] if self._idx else None

    def reset(self) -> None:
        self._idx.clear()
