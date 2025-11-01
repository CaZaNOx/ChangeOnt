# ChangeOntCode\agents\co\core\pipeline.py
from __future__ import annotations
from typing import Any, Dict, List, Optional

class COAgentCore:
    """
    Orchestrates header + elements + primitives. Safe no-throw step().
    Exposes a stable surface for adapters: step(observation, feedback) -> metrics dict.
    """
    def __init__(self,
                 header: Any,
                 elements: List[Any],
                 primitives: Dict[str, Any],
                 combinators: Dict[str, Any],
                 math_policy: str = "co",
                 name: str = "CO_core"):
        self.header = header
        self.elements = elements
        self.primitives = primitives
        self.combinators = combinators
        self.math_policy = math_policy
        self.name = name
        self._step = 0

    def step(self, observation: Optional[Dict[str, Any]] = None,
             feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._step += 1
        obs = observation or {}
        fb  = feedback or {}

        # 1) Header update (reads obs/signals; sets ε/τ/gauge, route)
        header_metrics = {}
        try:
            if hasattr(self.header, "update"):
                header_metrics = self.header.update(obs)
        except Exception:
            header_metrics = {"header_update": "failed"}

        # 2) Pipeline execution via combinator
        metrics: Dict[str, Any] = {"core": self.name, "step": self._step}
        metrics.update(header_metrics)

        pipeline = self.combinators.get("pipeline")
        if pipeline is not None and hasattr(pipeline, "run"):
            try:
                block_metrics = pipeline.run(self.elements, self.primitives, self.header, obs, fb)
                if isinstance(block_metrics, dict):
                    metrics.update(block_metrics)
            except Exception:
                metrics["pipeline"] = "failed"

        # 3) Optional router/gate (e.g., choose classical vs CO algebra for a block)
        gate = self.combinators.get("gate")
        if gate is not None and hasattr(gate, "route"):
            try:
                route = gate.route(self.header, metrics)
                metrics["route"] = route
            except Exception:
                metrics["route"] = "error"

        # 4) Math policy (recorded for downstream)
        metrics["math_policy"] = self.math_policy
        return metrics
