"""Canonical CO runtime pipeline.

Owns the ordered update path from boundary/candidate publication through field
and certificate telemetry into the final CommitmentSurface readout.  The
pipeline is the orchestrator; runtime surfaces should not silently reroute or
replace this sequence.
"""

# agents/co/core/combinators/C_pipeline.py

from __future__ import annotations
from typing import Any, Dict, List, Tuple
import os
import re


class C_Pipeline:
    """Canonical CO execution pipeline.

    The certified docs require the decision pass to run all non-readout surfaces
    before a single final CommitmentSurface invocation.  Old publication/readout class-name routing is intentionally not used here.
    """

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
        if "signal_bus" in low:
            return ["signal_bus"]
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
        if d in ("p10", "p12", "id_mem", "visit_tracker"):
            return [d]
        return []

    def _is_commitment_surface(self, element: Any) -> bool:
        for cls in element.__class__.mro():
            if cls.__name__ == "CommitmentSurface" and cls.__module__.endswith("runtime.surfaces.commitment_surface"):
                return True
        return False

    def _partition_elements(self, elements: list) -> Tuple[list, Any | None]:
        commitment = [e for e in elements if self._is_commitment_surface(e)]
        if len(commitment) > 1:
            raise RuntimeError("Canonical CO pipeline requires exactly one CommitmentSurface at most")
        head = commitment[0] if commitment else None
        non_head = [e for e in elements if e is not head]
        return non_head, head

    def _record_error(self, out: dict, where: str, exc: Exception) -> None:
        out.setdefault("errors", []).append({"where": where, "err": repr(exc)})
        out.setdefault("engineering_safety_triggered", True)
        out.setdefault("co_evidence_valid_for_step", False)
        out.setdefault("safety_kind", "surface_error")
        if os.environ.get("CO_STRICT_ERRORS", "") == "1":
            raise exc

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
            if not hasattr(e, "PRIMITIVE_DEPS"):
                warnings.append(f"{name} missing PRIMITIVE_DEPS declaration")
            if not hasattr(e, "COMBINATOR_DEPS"):
                warnings.append(f"{name} missing COMBINATOR_DEPS declaration")
            for dep in getattr(e, "PRIMITIVE_DEPS", ()) or ():
                for key in self._normalize_primitive_dep(str(dep)):
                    if key and key not in primitives:
                        warnings.append(f"{name} missing primitive '{key}' (declared: {dep})")
            for dep in getattr(e, "COMBINATOR_DEPS", ()) or ():
                dep_key = str(dep)
                if not sem:
                    warnings.append(f"{name} missing semantic combinator registry (_semantic)")
                    continue
                if dep_key and dep_key not in sem:
                    warnings.append(f"{name} missing semantic combinator '{dep_key}'")
        self._dep_warnings = warnings
        self._dep_checked = True
        if warnings and os.environ.get("CO_STRICT_DEPS", "") == "1":
            raise RuntimeError("Dependency check failed: " + "; ".join(warnings))

    def run(self, elements: list, primitives: dict, header: Any, observation: dict, feedback: dict | None) -> dict:
        out: dict = {}
        self._check_deps(elements, primitives)
        if self._dep_warnings:
            out.setdefault("dep_warnings", list(self._dep_warnings))
        non_head, head = self._partition_elements(elements)
        out.setdefault("canonical_pipeline_order", "non_readout_surfaces_then_commitment_surface")

        for e in non_head:
            if hasattr(e, "update"):
                try:
                    u = e.update(observation, primitives, header, feedback)
                    if isinstance(u, dict) and u:
                        out.update(u)
                except Exception as ex:
                    self._record_error(out, f"{e.__class__.__name__}.update", ex)

            if hasattr(e, "step"):
                try:
                    s = e.step(observation, primitives, header, feedback)
                    if isinstance(s, dict) and s:
                        out.update(s)
                except Exception as ex:
                    self._record_error(out, f"{e.__class__.__name__}.step", ex)

            if hasattr(e, "metrics"):
                try:
                    m = e.metrics()
                    if isinstance(m, dict) and m:
                        out.update(m)
                except Exception as ex:
                    self._record_error(out, f"{e.__class__.__name__}.metrics", ex)

        if head is not None and hasattr(head, "step"):
            try:
                sel = head.step(observation, primitives, header, feedback)
                if isinstance(sel, dict) and sel:
                    out.update(sel)
                    return out
            except Exception as ex:
                self._record_error(out, f"{head.__class__.__name__}.step", ex)
        return out

    def run_update(self, elements: list, primitives: dict, header: Any, observation: dict, feedback: dict | None) -> dict:
        """Learning-only pass; never invokes CommitmentSurface.step()."""
        out: dict = {}
        self._check_deps(elements, primitives)
        if self._dep_warnings:
            out.setdefault("dep_warnings", list(self._dep_warnings))
        obs_for_header = observation or {}
        if feedback is not None and "feedback" not in obs_for_header:
            obs_for_header = dict(obs_for_header)
            obs_for_header["feedback"] = feedback
        obs = obs_for_header
        try:
            core = getattr(header, "core", None)
            meta = getattr(core, "meta_header", None) if core is not None else None
            if meta is not None:
                obs = dict(obs_for_header)
                obs.setdefault("meta_header", meta.to_dict(obs_for_header))
            hrec = header.update(obs)
            if isinstance(hrec, dict):
                out.update(hrec)
            if os.environ.get("CO_DEBUG_HEADER", "") == "1":
                state = getattr(header, "state", None)
                if state is not None:
                    cur = int(getattr(state, "_debug_header_updates", 0))
                    setattr(state, "_debug_header_updates", cur + 1)
        except Exception as ex:
            self._record_error(out, "header.update", ex)

        non_head, _head = self._partition_elements(elements)
        for e in non_head:
            if hasattr(e, "update"):
                try:
                    u = e.update(obs, primitives, header, feedback)
                    if isinstance(u, dict) and u:
                        out.update(u)
                except Exception as ex:
                    self._record_error(out, f"{e.__class__.__name__}.update", ex)
            if hasattr(e, "metrics"):
                try:
                    m = e.metrics()
                    if isinstance(m, dict) and m:
                        out.update(m)
                except Exception as ex:
                    self._record_error(out, f"{e.__class__.__name__}.metrics", ex)
        return out
