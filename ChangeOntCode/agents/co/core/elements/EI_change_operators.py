# agents/co/core/elements/EI_change_operators.py
from __future__ import annotations
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

def _kgrams(seq: Tuple, k: int) -> List[Tuple]:
    out = []
    n = len(seq)
    for i in range(0, max(0, n - k + 1)):
        out.append(tuple(seq[i:i + k]))
    return out

@dataclass
class EI_ChangeOps:
    k: int = 3

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.k = int(params.get("k", self.k))
        return self

    def _run_core(self, history: Tuple) -> Dict[str, Any]:
        grams = _kgrams(history, self.k)
        motif_counts: Dict[Tuple, int] = {}
        for g in grams:
            motif_counts[g] = motif_counts.get(g, 0) + 1
        comp_counts: Dict[Tuple[Tuple, Tuple], int] = {}
        for i in range(len(grams) - 1):
            pair = (grams[i], grams[i + 1])
            comp_counts[pair] = comp_counts.get(pair, 0) + 1
        return {"motif_counts": motif_counts, "comp_counts": comp_counts}

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        eps = float(getattr(getattr(header, "state", object()), "eps_eff", 0.0))
        hist = tuple(observation.get("history", ()))
        out = self._run_core(hist)
        out["eps"] = eps
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)