# agents/co/core/combinators/C_pipeline.py

from __future__ import annotations
from typing import Any, Dict, List
from agents.co.core.contracts.signals import merge_signals

class C_Pipeline:
    def __init__(self, order: List[str] | None = None):
        self.order = order or []

    def run(
        self,
        elements: list,
        primitives: dict,
        header: any,
        observation: dict,
        feedback: dict | None,
    ) -> dict:
        out: dict = {}
        # 0) Header update so ActionHead sees co_weight/dyn
        try:
            hrec = header.update(observation)
            if isinstance(hrec, dict):
                out.update(hrec)
        except Exception:
            pass

        # 1) Everything except ActionHead
        head = None
        for e in elements:
            if e.__class__.__name__.lower().endswith("actionhead"):
                head = e
                continue

            if hasattr(e, "update"):
                try:
                    u = e.update(observation, primitives, header, feedback)
                    if isinstance(u, dict) and u:
                        out.update(u)
                except Exception:
                    pass

            if hasattr(e, "step"):
                try:
                    s = e.step(observation, primitives, header, feedback)
                    if isinstance(s, dict) and s:
                        out.update(s)
                except Exception:
                    pass

            if hasattr(e, "metrics"):
                try:
                    m = e.metrics()
                    if isinstance(m, dict) and m:
                        out.update(m)
                except Exception:
                    pass

        # 2) ActionHead exactly once, last
        if head is not None and hasattr(head, "step"):
            try:
                sel = head.step(observation, primitives, header, feedback)
                if isinstance(sel, dict) and sel:
                    out.update(sel)
                    return out
            except Exception:
                pass

        return out

    def run_update(
        self,
        elements: list,
        primitives: dict,
        header: any,
        observation: dict,
        feedback: dict | None,
    ) -> dict:
        """Learning-only pass. IMPORTANT: do **not** invoke ActionHead.step()."""
        out: dict = {}
        try:
            hrec = header.update(observation)
            if isinstance(hrec, dict):
                out.update(hrec)
        except Exception:
            pass

        for e in elements:
            if e.__class__.__name__.lower().endswith("actionhead"):
                continue  # skip the head on update pass

            if hasattr(e, "update"):
                try:
                    u = e.update(observation, primitives, header, feedback)
                    if isinstance(u, dict) and u:
                        out.update(u)
                except Exception:
                    pass

            # NOTE: in update pass we intentionally do *not* call e.step(...)
            # to avoid publishing/consuming votes and accidentally draining the bus.

            if hasattr(e, "metrics"):
                try:
                    m = e.metrics()
                    if isinstance(m, dict) and m:
                        out.update(m)
                except Exception:
                    pass

        return out