# agents/co/core/C_pipeline.py
from typing import Any, Dict, List

class C_Pipeline:
    """
    Executes elements in sequence; collects/merges metrics.
    Elements that declare `force_last = True` are executed after all others,
    so they can deterministically win key collisions (e.g., 'action').
    """
    def __init__(self, order: List[str] | None = None):
        self.order = order or []

    def run(
        self,
        elements: List[Any],
        primitives: Dict[str, Any],
        header: Any,
        observation: Dict[str, Any],
        feedback: Dict[str, Any],
    ) -> Dict[str, Any]:
        metrics: Dict[str, Any] = {}

        heads = [e for e in elements if getattr(e, "force_last", False)]
        rest  = [e for e in elements if not getattr(e, "force_last", False)]

        # optional: respect a given order filter (by element class name)
        if self.order:
            name = lambda e: e.__class__.__name__
            rest  = [e for e in rest  if name(e) in self.order]
            heads = [e for e in heads if name(e) in self.order]

        def _run_block(block: List[Any]) -> None:
            nonlocal metrics
            for e in block:
                try:
                    if hasattr(e, "update"):
                        m = e.update(observation, primitives, header, feedback)  # type: ignore
                        if isinstance(m, dict): metrics.update(m)
                    if hasattr(e, "step"):
                        m = e.step(observation, primitives, header, feedback)    # type: ignore
                        if isinstance(m, dict): metrics.update(m)
                    if hasattr(e, "metrics"):
                        m = e.metrics()                                           # type: ignore
                        if isinstance(m, dict): metrics.update(m)
                except Exception:
                    metrics[e.__class__.__name__] = "failed"

        _run_block(rest)
        _run_block(heads)   # <- heads always win

        return metrics