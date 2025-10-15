# agents/co/core/combinators/C_fuse.py
from __future__ import annotations
from typing import Dict, Any, Iterable, Tuple
import math

ActionScores = Dict[Any, float]

class C_Fuse:
    """
    Small fusion combinator for per-action scores.
    Methods: 'add', 'mul', 'softmax'
    """

    def __init__(self, method: str = "add", tau: float = 1.0, clamp: bool = True):
        self.method = str(method).lower()
        self.tau = max(1e-6, float(tau))
        self.clamp = bool(clamp)

    @staticmethod
    def _add(parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        out: ActionScores = {}
        for scores, w in parts:
            if not scores or w == 0.0:
                continue
            for a, s in scores.items():
                out[a] = out.get(a, 0.0) + float(w) * float(s)
        return out

    @staticmethod
    def _mul(parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        out: ActionScores = {}
        first = True
        for scores, w in parts:
            if not scores or w == 0.0:
                continue
            if first:
                out = {a: (1.0 + float(w) * float(s)) for a, s in scores.items()}
                first = False
            else:
                for a, s in scores.items():
                    out[a] = out.get(a, 1.0) * (1.0 + float(w) * float(s))
        return out

    def _softmax(self, parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        add = self._add(parts)
        if not add:
            return {}
        # temperature softmax
        exps = {a: math.exp(float(s) / self.tau) for a, s in add.items()}
        z = sum(exps.values()) or 1.0
        return {a: v / z for a, v in exps.items()}

    def fuse(self, parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        m = self.method
        if m == "add":
            return self._add(parts)
        if m == "mul":
            return self._mul(parts)
        if m == "softmax":
            return self._softmax(parts)
        # default
        return self._add(parts)