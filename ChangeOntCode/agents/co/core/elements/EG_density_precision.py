# agents/co/core/elements/EG_density_precision.py
from __future__ import annotations
from typing import Any, Dict, Set, Tuple
from ..primitives.P7_precision import precision_schedule
from ._shared import publish_signal

class EG_Density:
    """
    Precision / density control.
    - Maintains a simple per-episode visit-density for maze-like envs (self-contained).
    - Sets header_state.r_prime via precision_schedule (mode: fixed|coarse|adaptive).
    - Publishes EG_DensityPrecision.visit_density on co_bus for translators.
    """
    def __init__(self):
        self.params: Dict[str, Any] = {}
        self.last_r: int = 1
        self._seen: Set[Tuple[int,int]] = set()
        self._visits: int = 0

    def configure(self, params: Dict, context: Dict):
        self.params = params or {}
        self.params.setdefault("mode", "adaptive")
        self.params.setdefault("r_static", 1)
        return self

    def fit(self, stream_or_env_view=None):
        return self

    def _visit_density(self, observation: Dict[str, Any]) -> float:
        fam = str(observation.get("family", "")).lower()
        if fam != "maze":
            return 0.0
        pos = observation.get("pos")
        if isinstance(pos, (list, tuple)) and len(pos) >= 2:
            key = (int(pos[0]), int(pos[1]))
            self._visits += 1
            self._seen.add(key)
        if self._visits <= 0:
            return 0.0
        # high when many revisits: 1 - unique/total
        return max(0.0, min(1.0, 1.0 - (len(self._seen) / float(self._visits))))

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        signals = observation.get("signals", {})
        hs = getattr(header, "state", header)
        mode = self.params.get("mode", "adaptive")
        r_static = int(self.params.get("r_static", 1))

        stats = {"surprise": float(signals.get("z_PE", 0.0))}
        r_p = precision_schedule(stats, mode)
        if r_p != getattr(hs, "r_prime", r_static):
            hs.r_prime = r_p
        self.last_r = int(getattr(hs, "r_prime", r_static))

        # publish visit density
        vd = self._visit_density(observation)
        bus = primitives.get("co_bus")
        publish_signal(bus, "EG_DensityPrecision.visit_density", float(vd))

        return {"r_prime": int(self.last_r), "visit_density": float(vd)}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        # no extra step-time effects vs update
        return self.update(observation, primitives, header, feedback)

    def report(self) -> Dict:
        return {"r_prime": int(self.last_r)}