# agents/co/core/combinators/C_fuse.py
from __future__ import annotations
from typing import Dict, Any, Iterable, Tuple
import math

ActionScores = Dict[Any, float]

class C_Fuse:
    """
    Fusion combinator for per-action maps.
    Supported:
      - "add", "mul", "softmax"     (legacy / classical)
      - "minplus", "softminplus"    (CO: cost-space, (min,+))
    """

    def __init__(self, method: str = "add", tau: float = 1.0, clamp: bool = True):
        self.method = str(method).lower()
        self.tau = max(1e-6, float(tau))
        self.clamp = bool(clamp)

    # ------------- legacy (keep) -------------
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
        exps = {a: math.exp(float(s) / self.tau) for a, s in add.items()}
        z = sum(exps.values()) or 1.0
        return {a: v / z for a, v in exps.items()}

    # ------------- CO (new) ------------------
    @staticmethod
    def _minplus(parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        """
        For each action a: out[a] = min_i ( w_i + s_i[a] )
        Assumes scores are costs (lower = better).
        """
        best: ActionScores = {}
        for scores, w in parts:
            if not scores:
                continue
            w = float(w)
            for a, s in scores.items():
                c = w + float(s)
                prev = best.get(a)
                if prev is None or c < prev:
                    best[a] = c
        return best

    def _softminplus(self, parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        """
        Smooth (min,+): out[a] = -tau * log sum_i exp( - (w_i + s_i[a]) / tau )
        """
        # accumulate log-sum-exp in negative space for each action
        buckets: Dict[Any, list] = {}
        for scores, w in parts:
            if not scores:
                continue
            w = float(w)
            for a, s in scores.items():
                buckets.setdefault(a, []).append(-(w + float(s)) / self.tau)

        out: ActionScores = {}
        for a, zs in buckets.items():
            if not zs:
                continue
            m = max(zs)              # for numerical stability
            acc = sum(math.exp(z - m) for z in zs)
            out[a] = -self.tau * (math.log(acc) + m)
        return out

    # ------------- router --------------------
    def fuse(self, parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        m = self.method
        if m == "add":
            return self._add(parts)
        if m == "mul":
            return self._mul(parts)
        if m == "softmax":
            return self._softmax(parts)
        if m == "minplus":
            return self._minplus(parts)
        if m == "softminplus":
            return self._softminplus(parts)
        return self._add(parts)