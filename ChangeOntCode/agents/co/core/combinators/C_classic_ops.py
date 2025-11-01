# C_classic_ops.py
from typing import Iterable

class C_ClassicOps:
    """Classical arithmetic helpers."""
    @staticmethod
    def add(xs: Iterable[float]) -> float:
        s = 0.0
        for x in xs:
            try: s += float(x)
            except Exception: continue
        return s

    @staticmethod
    def mul(xs: Iterable[float]) -> float:
        p = 1.0
        for x in xs:
            try: p *= float(x)
            except Exception: continue
        return p
