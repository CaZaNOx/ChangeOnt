# P10_change_ops_core.py
from typing import List, Tuple, Any, Callable, Dict
from .operators.J1_bend_substitution import bend_cost_between
from .operators.J4a_reid_closure import within_epsilon

class ChangeOpsCore:
    """
    CO P10: bend-tolerant merge (⊕) and composition (⊗) over k-grams.
    Safe, minimal implementation with medoid-like merge and overlap compose.
    """
    def __init__(self, k: int = 4, epsilon: float = 0.0, mdλ: float = 0.0):
        self.k = max(1, int(k))
        self.epsilon = max(0.0, float(epsilon))
        self.mdl_lambda = max(0.0, float(mdλ))
        self.prototypes: List[Tuple[Any, ...]] = []

    def kgrams(self, seq: List[Any]) -> List[Tuple[Any, ...]]:
        k = self.k
        return [tuple(seq[i:i+k]) for i in range(0, max(0, len(seq) - k + 1))]

    def merge(self, a: Tuple[Any, ...], b: Tuple[Any, ...],
              dist: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float]) -> Tuple[Any, ...] | None:
        if dist(a, b) <= self.epsilon:
            # simple medoid pick
            ca = sum(dist(a, p) for p in (a, b))
            cb = sum(dist(b, p) for p in (a, b))
            return a if ca <= cb else b
        return None

    def compose(self, p: Tuple[Any, ...], q: Tuple[Any, ...],
                dist: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float]) -> Tuple[Any, ...] | None:
        # overlap-aware concatenate
        k = len(p)
        best_r = 0
        for r in range(1, k):
            if within_epsilon(p[-r:], q[:r], self.epsilon, dist):
                best_r = r
        if best_r == 0:
            return None
        return p + q[best_r:]

    def features(self, seq: List[Any],
                 dist: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float]) -> Dict[str, float]:
        """
        Produce simple motif counts features; safe no-crash if prototypes empty.
        """
        ks = self.kgrams(seq)
        feats: Dict[str, float] = {}
        for i, p in enumerate(self.prototypes):
            cnt = 0
            for g in ks:
                if within_epsilon(g, p, self.epsilon, dist):
                    cnt += 1
            feats[f"motif_{i}"] = float(cnt)
        return feats

__all__ = ["ChangeOpsCore"]
