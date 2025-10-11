# C_pipeline.py
from typing import Any, Dict, List

class C_Pipeline:
    """
    Executes elements in sequence; each element may expose a well-known method.
    Collects and merges returned metrics dicts.
    """
    def __init__(self, order: List[str] | None = None):
        self.order = order or []  # optional element names; if empty, preserves given order

    def run(self, elements: List[Any], primitives: Dict[str, Any], header: Any,
            observation: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
        metrics: Dict[str, Any] = {}
        # preserve given order (or filter by self.order if provided)
        for e in elements:
            try:
                # Discover standard hooks
                if hasattr(e, "update"):
                    m = e.update(observation, primitives, header, feedback)  # type: ignore
                    if isinstance(m, dict): metrics.update(m)
                if hasattr(e, "step"):
                    m = e.step(observation, primitives, header, feedback)    # type: ignore
                    if isinstance(m, dict): metrics.update(m)
                if hasattr(e, "metrics"):
                    m = e.metrics()                                          # type: ignore
                    if isinstance(m, dict): metrics.update(m)
            except Exception:
                metrics[e.__class__.__name__] = "failed"
        return metrics
