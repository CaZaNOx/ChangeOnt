# agents/co/core/elements/EJ_order_arisal.py
from __future__ import annotations
from typing import Any, Dict, Iterable, List
from agents.co.core.contracts.signals import normalize_scores
from ._shared import publish_signal, push_votes

class EJ_OrderAsymmetry:
    """
    Element wrapper for P15 (OrderArisal):
      - publishes loop/arisal to co_bus under namespaced keys
      - pushes a per-action vote (penalizes backtracks/2-cycles) into co_bus
    """
    def __init__(self):
        self.params: Dict[str, Any] = {}
        self.tag: str = "EJ_OrderAsymmetry"
        self.enabled: bool = True
        self.lambda_loop: float = 0.5
        self.write_bus: bool = True
        self._last: Dict[str, Any] = {}

    def configure(self, params: Dict, context: Dict):
        p = params or {}
        self.enabled     = bool(p.get("enabled", True))
        self.lambda_loop = float(p.get("lambda_loop", 0.5))
        self.write_bus   = bool(p.get("write_bus", True))
        self.tag         = str(p.get("tag", "EJ_OrderAsymmetry"))
        self.params = {
            "enabled": self.enabled,
            "lambda_loop": self.lambda_loop,
            "write_bus": self.write_bus,
            "tag": self.tag,
        }
        return self

    def _get_actions(self, observation: Dict[str, Any]) -> List[Any]:
        actions = observation.get("action_space")
        if actions is None:
            if "n_arms" in observation:
                n = int(observation.get("n_arms", 0))
                return list(range(max(0, n)))
            if "A" in observation:
                n = int(observation.get("A", 0))
                return list(range(max(0, n)))
            return []
        return list(actions)

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        # learning-free; nothing to do here for now
        return {}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        if not self.enabled:
            return {}
        actions = self._get_actions(observation)
        p15 = primitives.get("P15")
        bus = primitives.get("co_bus")
        family = str(observation.get("family", "")).lower()

        out: Dict[str, Any] = {}
        if p15 is None or not actions:
            out[f"{self.tag}.status"] = "unavailable"
            self._last = out
            return out

        try:
            pen_map: Dict[Any, float] = p15.penalty_for_actions(actions, observation)
        except Exception:
            pen_map = {a: 0.0 for a in actions}

        raw_vote = {a: max(0.0, 1.0 - float(pen_map.get(a, 0.0))) for a in actions}
        vote_map = normalize_scores(raw_vote)

        if self.lambda_loop not in (None, 0.0):
            vote_map = {a: (1.0 - self.lambda_loop) * 0.5 + self.lambda_loop * v for a, v in vote_map.items()}

        try:
            metrics = p15.metrics()
        except Exception:
            metrics = {"loopiness": 0.0, "arisal": 0.0}

        if self.write_bus and bus is not None:
            publish_signal(bus, f"{self.tag}.loopiness", float(metrics.get("loopiness", 0.0)))
            publish_signal(bus, f"{self.tag}.arisal",    float(metrics.get("arisal", 0.0)))
            avg_pen = 0.0
            if pen_map:
                try: avg_pen = sum(float(x) for x in pen_map.values()) / max(1, len(pen_map))
                except Exception: avg_pen = 0.0
            publish_signal(bus, f"{self.tag}.avg_penalty", float(avg_pen))
            # push votes so ActionHead sees them via bus
            push_votes(bus, family, vote_map, source=self.tag)

        out[f"{self.tag}.loopiness"]    = float(metrics.get("loopiness", 0.0))
        out[f"{self.tag}.arisal"]       = float(metrics.get("arisal", 0.0))
        out[f"{self.tag}.avg_penalty"]  = float(sum(pen_map.values()) / max(1, len(pen_map)) if pen_map else 0.0)
        out[f"{self.tag}.penalty_map"]  = pen_map
        out[f"{self.tag}.vote_map"]     = vote_map
        self._last = out
        return out

    def report(self) -> Dict[str, Any]:
        return dict(self._last)