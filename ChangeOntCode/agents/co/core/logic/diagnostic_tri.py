# agents/co/core/logic/diagnostic_tri.py
from enum import IntEnum

class Tri(IntEnum):
    BOT = 0  # false
    UNK = 1  # unknown/within tolerance
    TOP = 2  # true

def meet(a: Tri, b: Tri) -> Tri:
    return Tri(min(int(a), int(b)))

def join(a: Tri, b: Tri) -> Tri:
    return Tri(max(int(a), int(b)))

def neg(a: Tri) -> Tri:
    return {Tri.TOP: Tri.BOT, Tri.BOT: Tri.TOP}.get(a, Tri.UNK)
