# agents/co/core/elements/EE_compressibility.py
from __future__ import annotations
from typing import Iterable, Any, Dict, List
from ._shared import publish_signal

class EE_Compressibility:
    """
    Element E: Memory compressibility → robustness predictor.
    Simple LZ-ish distinct-subsequence counter in a sliding window.
    """
    def __init__(self, window: int = 32):
        self.window = max(4, int(window))
        self._last: Dict[str, float] = {}

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        if params:
            self.window = max(4, int(params.get("window", self.window)))
        return self

    def _lz_counter(self, seq: Iterable[Any]) -> float:
        buf: List[Any] = []
        seen = set()
        k = self.window
        for x in seq:
            buf.append(x)
            if len(buf) > k:
                buf.pop(0)
            seen.add(tuple(buf))
        return float(len(seen))

    def _predict(self, seq: Iterable[Any]) -> Dict[str, float]:
        lz = self._lz_counter(seq)
        robustness = 1.0 / (1.0 + lz) if lz > 0 else 0.0  # monotone map
        return {"lz": lz, "robustness_pred": robustness}

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        hist = observation.get("history", [])
        out = self._predict(hist)
        bus = primitives.get("co_bus")
        publish_signal(bus, "EE_Compressibility.robustness", out["robustness_pred"])
        self._last = out
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)

    def report(self) -> Dict[str, float]:
        return dict(self._last)