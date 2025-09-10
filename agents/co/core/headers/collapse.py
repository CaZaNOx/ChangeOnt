from __future__ import annotations

from dataclasses import dataclass
from typing import Deque, Iterable, Tuple
from collections import deque
import math

@dataclass
class CollapseConfig:
    window: int = 200
    entropy_bits_thresh: float = 0.10
    var_rel_thresh: float = 0.05  # relative to mean
    unfreeze_violations: int = 2  # consecutive violations to unfreeze

class CollapseHeader:
    """
    Freeze topology edits (merges/splits) when conditional entropy and variance are low.
    """
    def __init__(self, cfg: CollapseConfig):
        self.cfg = cfg
        self._y_window: Deque[int] = deque(maxlen=cfg.window)
        self._frozen: bool = False
        self._violations: int = 0

    def _entropy_bits(self, counts: Iterable[int]) -> float:
        total = sum(counts)
        if total <= 0:
            return 0.0
        ent = 0.0
        for c in counts:
            if c <= 0:
                continue
            p = c / total
            ent -= p * math.log2(p)
        return ent

    def _variance_rel(self, values: Iterable[float]) -> float:
        xs = list(values)
        if not xs:
            return 0.0
        m = sum(xs) / len(xs)
        if m == 0.0:
            return 0.0
        var = sum((x - m) ** 2 for x in xs) / len(xs)
        return var / abs(m)

    def update(self, class_ids: Iterable[int]) -> Tuple[bool, float, float]:
        """
        Append latest class IDs and recompute freeze state.
        Returns (is_frozen, entropy_bits, var_rel).
        """
        for cid in class_ids:
            self._y_window.append(cid)

        if len(self._y_window) < self.cfg.window:
            return self._frozen, 1.0, 1.0  # not enough data yet

        counts = {}
        for cid in self._y_window:
            counts[cid] = counts.get(cid, 0) + 1

        ent_bits = self._entropy_bits(counts.values())
        var_rel = self._variance_rel(counts.values())

        if (ent_bits <= self.cfg.entropy_bits_thresh) and (var_rel <= self.cfg.var_rel_thresh):
            self._frozen = True
            self._violations = 0
        else:
            if self._frozen:
                self._violations += 1
                if self._violations >= self.cfg.unfreeze_violations:
                    self._frozen = False
                    self._violations = 0
            else:
                self._violations = 0

        return self._frozen, ent_bits, var_rel

    @property
    def frozen(self) -> bool:
        return self._frozen

# Backward-compat alias for older code
CollapseGuard = CollapseHeader

__all__ = ["CollapseHeader", "CollapseConfig", "CollapseGuard"]
