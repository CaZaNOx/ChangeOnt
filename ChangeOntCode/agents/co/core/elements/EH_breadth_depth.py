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
    COMBINATOR_FORM = "SC_WeightedSelection (+ optional SC_GatedThreshold)"
    COMBINATOR_DEPS = ("SC_WeightedSelection",)
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

        mix_mode = self.params["mix_mode"]
        if mix_mode == "fixed":
            p = float(self.params["fixed_p"])
        else:
            p_loop = suggest_p_breadth(L, self.params["depth_hint"])
            if mix_mode == "loop_only":
                p = p_loop
            else:  # dyn_blend
                sem = get_semantic(primitives)
                sc_sel = sem.get("SC_WeightedSelection")
                if sc_sel is None:
                    # fallback to base blend if semantic combinator missing
                    p = (1 - hs.dyn) * 0.5 * p_loop + (hs.dyn) * p_loop
                else:
                    candidates = {"breadth": float(p_loop), "depth": float(1.0 - p_loop)}
                    weights = {"breadth": float(hs.dyn), "depth": float(1.0 - float(hs.dyn))}
                    sel = sc_sel.select(candidates, weights=weights, mode="blend")
                    try:
                        p = float(sel.get("score", p_loop))
                    except Exception:
                        p = p_loop

        p = max(0.1, min(0.9, p))
        hs.p_breadth = p
        self.last_p = p
        return {"p_breadth": float(p), "loopiness": float(L)}

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        hs = getattr(header, "state", header)
        frontier = observation.get("frontier")
        path = observation.get("path")
        return self._compute(hs, primitives, frontier, path)

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)

    def report(self) -> Dict[str, float]:
        return {"p_breadth": float(self.last_p)}
