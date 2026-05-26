# agents/co/core/elements/EH_breadth_depth.py
from __future__ import annotations
from typing import Any, Dict
from ..primitives.P8_loopiness import loopiness, suggest_p_breadth
from ._shared import get_semantic

class EH_BreadthDepth:
    """
    Schedule exploration breadth vs. depth from 'loopiness' and header dyn.
    """
    PRIMITIVE_DEPS = ("P8_Loopiness",)
    COMBINATOR_FORM = "local bounded breadth-depth blend"
    COMBINATOR_DEPS = ()
    FORMULA_STATUS = "provisional"

    def __init__(self):
        self.params: Dict[str, Any] = {}
        self.last_p: float = 0.2

    def configure(self, params: Dict, context: Dict):
        self.params = params or {}
        self.params.setdefault("mix_mode", "dyn_blend")
        self.params.setdefault("fixed_p", 0.3)
        self.params.setdefault("depth_hint", 6)
        return self

    def fit(self, stream_or_env_view=None):
        return self

    def _compute(self, hs: Any, primitives: Dict[str, Any], frontier, path) -> Dict[str, float]:
        L = 0.0
        if frontier is not None:
            L = loopiness(frontier)
        elif path is not None:
            L = loopiness(path)

        debt = 0.0
        rigidity = 0.0
        bus = primitives.get("signal_bus")
        try:
            if bus is not None and hasattr(bus, "signals"):
                sig = dict(bus.signals() or {})
                debt = float(sig.get("EC_Identity.adaptation_debt", 0.0) or 0.0)
                rigidity = float(sig.get("EC_Identity.rigidity_pressure", 0.0) or 0.0)
        except Exception:
            debt = 0.0
            rigidity = 0.0
        breadth_drive = max(float(L), 0.85 * float(debt) + 0.15 * float(rigidity))

        mix_mode = self.params["mix_mode"]
        if mix_mode == "fixed":
            p = float(self.params["fixed_p"])
        else:
            p_loop = suggest_p_breadth(breadth_drive, self.params["depth_hint"])
            if mix_mode == "loop_only":
                p = p_loop
            else:  # dyn_blend
                # Local bounded blend only; this investigatory element does
                # not depend on a separate weighted-selection readout.
                p = (1 - hs.dyn) * 0.5 * p_loop + (hs.dyn) * p_loop

        p = max(0.1, min(0.9, p))
        hs.p_breadth = p
        self.last_p = p
        return {"p_breadth": float(p), "loopiness": float(L), "adaptation_debt": float(debt), "breadth_drive": float(breadth_drive)}

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        hs = getattr(header, "state", header)
        frontier = observation.get("frontier")
        path = observation.get("path")
        return self._compute(hs, primitives, frontier, path)

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)

    def report(self) -> Dict[str, float]:
        return {"p_breadth": float(self.last_p)}
