# agents/co/core/elements/EC_identity.py
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from ..primitives.identity import same, bend_distance, closure

@dataclass
class EC_Identity:
    def configure(self, params, context):
        return self

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        eps = float(getattr(state["header_state"], "eps_eff", 0.0))
        hist = list(state.get("history", ()))
        ok = True
        dist = 0.0
        if len(hist) >= 2:
            ok = same(hist[-2:], hist[-2:], eps)
            dist = bend_distance(hist[-2:], hist[-2:])
        return {"eps": eps, "identity_ok": ok, "last_d": dist}
