# agents/co/core/elements/EC_identity.py
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from ..primitives.identity import same, bend_distance, closure
from ._shared import publish_signal

@dataclass
class EC_Identity:
    def configure(self, params, context):
        return self

    def _run_core(self, observation: Dict[str, Any], header: Any) -> Dict[str, Any]:
        eps = float(getattr(getattr(header, "state", object()), "eps_eff", 0.0))
        hist = list(observation.get("history", ()))
        ok = True
        dist = 0.0
        if len(hist) >= 2:
            ok = bool(same(hist[-2:], hist[-2:], eps))
            dist = float(bend_distance(hist[-2:], hist[-2:]))
        return {"eps": eps, "identity_ok": ok, "last_d": dist}

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        out = self._run_core(observation, header)
        bus = primitives.get("co_bus")
        publish_signal(bus, "EC_Identity.same",   1.0 if out["identity_ok"] else 0.0)
        publish_signal(bus, "EC_Identity.last_d", out["last_d"])
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        return self.update(observation, primitives, header, feedback)