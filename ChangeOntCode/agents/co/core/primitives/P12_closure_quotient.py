# P12_closure_quotient.py
from __future__ import annotations
from typing import Dict, Set, Any, Iterable

from agents.co.core.primitives.P1_bend_metric import d_bend


class ClosureQuotient:
    """
    P12: minimal equivalence closure over prototypes (v1).
    Incremental assignment using P1 d_bend and fixed τmerge.
    """
    def __init__(self, epsilon: float | None = None) -> None:
        # epsilon accepted for compatibility but ignored in v1
        self.tau_merge = 0.20
        self.classes: Dict[int, Set[int]] = {}
        self.rep: Dict[int, int] = {}
        self._next_unassigned = 0

    def _assign_one(self, new_id: int, protos: list[Any]) -> None:
        if new_id < 0 or new_id >= len(protos):
            return

        # no existing classes: create first
        if not self.classes:
            self.classes[new_id] = {new_id}
            self.rep[new_id] = new_id
            return

        new_trace = protos[new_id]
        best_class = None
        best_d = None
        for class_id, rep_id in self.rep.items():
            try:
                rep_trace = protos[rep_id]
            except Exception:
                continue
            try:
                d = float(d_bend(list(new_trace), list(rep_trace)))
            except Exception:
                continue
            if d <= self.tau_merge:
                if (best_d is None) or (d < best_d) or (d == best_d and class_id < best_class):
                    best_d = d
                    best_class = class_id

        if best_class is None:
            # create new class; representative is first (new_id)
            self.classes[new_id] = {new_id}
            self.rep[new_id] = new_id
        else:
            self.classes.setdefault(best_class, set()).add(new_id)
            # representative remains first in class (do not change)
            if best_class not in self.rep:
                self.rep[best_class] = min(self.classes[best_class])

    def assign(self, new_id: int, primitives: Dict[str, Any] | None = None) -> int:
        """
        Incrementally assign a single new prototype id from primitives["p10"].prototypes.
        Returns 1 if assigned, 0 otherwise.
        """
        if primitives is None:
            return 0
        p10 = primitives.get("p10")
        prototypes = list(getattr(p10, "prototypes", [])) if p10 is not None else []
        if not prototypes:
            return 0
        try:
            idx = int(new_id)
        except Exception:
            return 0
        if idx < 0 or idx >= len(prototypes):
            return 0
        self._assign_one(idx, prototypes)
        self._next_unassigned = max(self._next_unassigned, idx + 1)
        return 1

    # Compatibility shim (unused by v1 wiring)
    def closure(self, prototypes: Iterable[Any]) -> Dict[int, Set[int]]:
        protos = list(prototypes)
        self.classes = {}
        self.rep = {}
        self._next_unassigned = 0
        for idx in range(len(protos)):
            self._assign_one(idx, protos)
        self._next_unassigned = len(protos)
        return dict(self.classes)


__all__ = ["ClosureQuotient"]
