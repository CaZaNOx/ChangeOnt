# agents/co/core/elements/EH_breadth_depth.py
from __future__ import annotations
from typing import Any, Dict
from ..primitives.P8_loopiness import loopiness, suggest_p_breadth

class EH_BreadthDepth:
    """
    Schedule exploration breadth vs. depth from 'loopiness' and header dyn.
    """
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

    def _compute(self, hs: Any, frontier, path) -> Dict[str, float]:
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
                p = (1 - hs.dyn) * 0.5 * p_loop + (hs.dyn) * p_loop

        p = max(0.1, min(0.9, p))
        hs.p_breadth = p
        self.last_p = p
        return {"p_breadth": float(p), "loopiness": float(L)}

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        hs = getattr(header, "state", header)
        frontier = observation.get("frontier")
        path = observation.get("path")
        return self._compute(hs, frontier, path)

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)

    def report(self) -> Dict[str, float]:
        return {"p_breadth": float(self.last_p)}