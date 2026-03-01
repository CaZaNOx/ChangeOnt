# agents/co/core/combinators/C_pipeline.py

from __future__ import annotations
from typing import Any, Dict, List
import re
from agents.co.core.contracts.signals import merge_signals

class C_Pipeline:
    def __init__(self, order: List[str] | None = None):
        self.order = order or []
        self._dep_checked = False
        self._dep_warnings: List[str] = []

    def _normalize_primitive_dep(self, dep: str) -> List[str]:
        d = dep.strip()
        low = d.lower()
        if "optional" in low:
            return []
        if "identity memory" in low:
            return ["id_mem"]
        if "visit_tracker" in low:
            return ["visit_tracker"]
        if "co_bus" in low:
            return ["co_bus"]
        if "bandit_stats" in low:
            return ["bandit_stats"]
        if "ngram_model" in low:
            return ["ngram_model"]
        if "budget" in low:
            return ["budget"]
        if "history/state" in low:
            return []
        m = re.match(r"^(P\d+)", d)
        if m:
            key = m.group(1)
            if key == "P10":
                return ["p10"]
            if key == "P12":
                return ["p12"]
            return [key]
        # allow direct keys
        if d in ("p10", "p12", "id_mem", "visit_tracker"):
            return [d]
        return []

    def _check_deps(self, elements: list, primitives: dict) -> None:
        if self._dep_checked:
            return
        warnings: List[str] = []
        sem = {}
        try:
            sem = primitives.get("_semantic", {}) or {}
        except Exception:
            sem = {}
        for e in elements:
            name = e.__class__.__name__
            # Explicit element declarations
            if not hasattr(e, "PRIMITIVE_DEPS"):
                warnings.append(f"{name} missing PRIMITIVE_DEPS declaration")
            if not hasattr(e, "COMBINATOR_DEPS"):
                warnings.append(f"{name} missing COMBINATOR_DEPS declaration")
            # Primitive deps
            for dep in getattr(e, "PRIMITIVE_DEPS", ()) or ():
                for key in self._normalize_primitive_dep(str(dep)):
                    if key and key not in primitives:
                        warnings.append(f"{name} missing primitive '{key}' (declared: {dep})")
            # Combinator deps
            for dep in getattr(e, "COMBINATOR_DEPS", ()) or ():
                dep_key = str(dep)
                if not sem:
                    warnings.append(f"{name} missing semantic combinator registry (_semantic)")
                    continue
                if dep_key and dep_key not in sem:
                    warnings.append(f"{name} missing semantic combinator '{dep_key}'")
        self._dep_warnings = warnings
        self._dep_checked = True
        if warnings:
            try:
                import os
                if os.environ.get("CO_STRICT_DEPS", "") == "1":
                    raise RuntimeError("Dependency check failed: " + "; ".join(warnings))
            except Exception:
                pass

    def run(
        self,
        elements: list,
        primitives: dict,
        header: any,
        observation: dict,
        feedback: dict | None,
    ) -> dict:
        out: dict = {}
        self._check_deps(elements, primitives)
        if self._dep_warnings:
            out.setdefault("dep_warnings", list(self._dep_warnings))
        # 0) NOTE: Header update is owned by run_update (learning pass).
        # Decision pass must read existing header.state only (no update here).

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
        self._check_deps(elements, primitives)
        if self._dep_warnings:
            out.setdefault("dep_warnings", list(self._dep_warnings))
        obs_for_header = observation or {}
        if feedback is not None:
            try:
                if "feedback" not in obs_for_header:
                    obs_for_header = dict(obs_for_header)
                    obs_for_header["feedback"] = feedback
            except Exception:
                pass
        obs = obs_for_header
        try:
            hrec = header.update(obs_for_header)
            if isinstance(hrec, dict):
                out.update(hrec)
            # debug counter (off by default): track header updates per env step
            try:
                import os
                if os.environ.get("CO_DEBUG_HEADER", "") == "1":
                    state = getattr(header, "state", None)
                    if state is not None:
                        try:
                            cur = int(getattr(state, "_debug_header_updates", 0))
                            setattr(state, "_debug_header_updates", cur + 1)
                        except Exception:
                            try:
                                cur = int(state.get("_debug_header_updates", 0))
                                state["_debug_header_updates"] = cur + 1
                            except Exception:
                                pass
            except Exception:
                pass
        except Exception:
            pass

        for e in elements:
            if e.__class__.__name__.lower().endswith("actionhead"):
                continue  # skip the head on update pass

            if hasattr(e, "update"):
                try:
                    u = e.update(obs, primitives, header, feedback)
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
