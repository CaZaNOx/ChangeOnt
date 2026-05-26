from __future__ import annotations
from typing import Dict, Any, Iterable, Tuple

ActionScores = Dict[Any, float]

class C_Fuse:
    """Small bounded score-combination utility used inside canonical surfaces.

    This is not a runtime architecture layer and not a baseline/rescue route.
    It only combines already-published CO evidence maps. Unsupported methods
    fail closed rather than silently changing behavior.
    """

    def __init__(self, method: str = "bounded_add", tau: float = 1.0, clamp: bool = True):
        m = str(method or "bounded_add").lower()
        # Backward-compatible alias: existing canonical config may still pass
        # add, but the semantics are bounded additive CO evidence combination.
        if m == "add":
            m = "bounded_add"
        if m not in {"bounded_add", "minplus", "softminplus"}:
            raise ValueError(f"Unsupported certified CO fusion method: {method!r}")
        self.method = m
        self.tau = max(1e-6, float(tau))
        self.clamp = bool(clamp)

    @staticmethod
    def _bounded_add(parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        out: ActionScores = {}
        for scores, w in parts:
            if not scores or w == 0.0:
                continue
            for a, s in scores.items():
                out[a] = out.get(a, 0.0) + float(w) * float(s)
        return {a: max(0.0, min(1.0, float(v))) for a, v in out.items()}

    @staticmethod
    def _minplus(parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
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
        import math
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
            m = max(zs)
            acc = sum(math.exp(z - m) for z in zs)
            out[a] = -self.tau * (math.log(acc) + m)
        return out

    def fuse(self, parts: Iterable[Tuple[ActionScores, float]]) -> ActionScores:
        if self.method == "bounded_add":
            return self._bounded_add(parts)
        if self.method == "minplus":
            return self._minplus(parts)
        if self.method == "softminplus":
            return self._softminplus(parts)
        raise RuntimeError(f"Unsupported certified CO fusion method: {self.method!r}")
