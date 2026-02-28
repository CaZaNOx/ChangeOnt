# agents/co/core/elements/EB_ghvc.py
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from ._shared import publish_signal

@dataclass
class EB_GHVC:
    """
    EB_GHVC (v1): birth/admission mechanism.
    Primitive deps (intended): P3_MDL, P10_ChangeOpsCore, optional P12_ClosureQuotient.
    Combinator form (intended): SC_GatedThreshold (primary), SC_AdditiveBlend inside trigger score.
    Formula status: provisional (threshold structure binding).
    """
    PRIMITIVE_DEPS = ("P3_MDL", "P10_ChangeOpsCore", "P12_ClosureQuotient (optional)")
    COMBINATOR_FORM = "SC_GatedThreshold (+ SC_AdditiveBlend inside score)"
    FORMULA_STATUS = "provisional"

    birth_threshold: float = 2.0
    mdl_lambda: float = 1.0
    cooldown: int = 5
    last_birth_t: int = -10
    _last_out: Dict[str, Any] | None = None
    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.birth_threshold = float(params.get("birth_threshold", params.get("gamma", self.birth_threshold)))
        self.mdl_lambda = float(params.get("mdl_lambda", params.get("lambda", self.mdl_lambda)))
        self.cooldown = int(params.get("cooldown", self.cooldown))
        return self

    def _sum_abs(self, values) -> float:
        total = 0.0
        for v in values:
            try:
                total += abs(float(v))
            except Exception:
                continue
        return total

    def _run_core(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any,
                  feedback: Dict[str, Any] | None = None) -> Dict[str, Any]:
        t     = int(observation.get("t", 0))
        res   = observation.get("residuals", {}) or {}
        probes= observation.get("probes", {}) or {}
        fb    = observation.get("feedback", {}) or {}
        if (not fb) and isinstance(feedback, dict):
            fb = feedback
        budget= primitives.get("budget")

        if res:
            pressure = self._sum_abs(res.values())
        elif probes:
            pressure = self._sum_abs(probes.values())
        else:
            pressure = 0.0
            if isinstance(fb, dict) and "reward" in fb:
                try:
                    pressure = abs(float(fb.get("reward", 0.0))) * 4.5
                except Exception:
                    pressure = 0.0

        k_new = 1 if (res or probes) else 0
        mse = pressure
        P3 = primitives.get("P3")
        if P3 is None:
            raise RuntimeError("EB_GHVC requires primitives['P3'] (P3_MDL) but it is missing.")
        if hasattr(P3, "mdl_gain"):
            mdl_gain = float(P3.mdl_gain(mse, k_new=k_new, mdl_lambda=self.mdl_lambda))
        else:
            raise RuntimeError("P3_MDL has no supported API (mdl_gain).")
        if self.cooldown <= 0:
            cooldown_ok = True
        else:
            cooldown_ok = (t - int(self.last_birth_t)) >= int(self.cooldown)
        birth_suggest = int((pressure >= self.birth_threshold) and (mdl_gain > 0.0) and cooldown_ok)

        born = False
        cap_hits = 0
        if birth_suggest:
            if budget is None:
                born = True
            else:
                try:
                    if budget.allow_move("birth") and budget.commit("birth"):
                        born = True
                    else:
                        cap_hits = 1
                except Exception:
                    pass
        if born:
            self.last_birth_t = t

        return {
            "born_variable": born,
            "birth_suggest": birth_suggest,
            "pressure": pressure,
            "mdl_gain": mdl_gain,
            "cap_hits": int(cap_hits),
        }

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        no_inputs = not (observation.get("residuals") or observation.get("probes") or observation.get("feedback") or feedback)
        out = self._run_core(observation, primitives, header, feedback)
        try:
            from agents.co.core.primitives.P10_change_ops_core import ChangeOpsCore
        except Exception:
            ChangeOpsCore = None

        # ensure canonical primitives exist
        if "birth_count" not in primitives:
            primitives["birth_count"] = 0
        p10 = primitives.get("p10")
        if p10 is None and out.get("born_variable"):
            if ChangeOpsCore is None:
                raise RuntimeError("EB_GHVC birth accepted but primitives['p10'] is missing.")
            p10 = ChangeOpsCore(k=4, epsilon=1.0)
            primitives["p10"] = p10

        # wire birth into a concrete state mutation (p10/p12), minimal + safe
        if out.get("born_variable") and p10 is not None:
            hist = observation.get("history", None)
            trace = observation.get("trace", hist if hist is not None else [])
            if not isinstance(trace, list):
                try:
                    trace = list(trace)
                except Exception:
                    trace = []
            proto = None
            try:
                k = max(1, int(getattr(p10, "k", 1)))
                if trace:
                    proto = tuple(trace[-k:]) if len(trace) >= k else tuple(trace)
            except Exception:
                proto = None
            if proto is None:
                proto = (f"born_{observation.get('family','')}", int(observation.get("t", 0)))
            try:
                if hasattr(p10, "prototypes") and proto not in p10.prototypes:
                    p10.prototypes.append(proto)
            except Exception:
                pass

            # optional incremental closure update if p12 is wired
            p12 = primitives.get("p12")
            if p12 is not None and hasattr(p12, "assign"):
                try:
                    proto_id = None
                    try:
                        proto_id = len(getattr(p10, "prototypes", [])) - 1
                    except Exception:
                        proto_id = None
                    if proto_id is not None and proto_id >= 0:
                        try:
                            p12.assign(new_id=proto_id, primitives=primitives)
                        except TypeError:
                            p12.assign(proto_id, primitives)
                except Exception:
                    pass

        # compute current counts (even if no birth) for telemetry
        prototype_count = len(getattr(p10, "prototypes", [])) if p10 is not None else 0
        class_count = 0
        p12 = primitives.get("p12")
        if p12 is not None:
            try:
                class_count = len(getattr(p12, "classes", {}) or {})
            except Exception:
                class_count = 0

        out["birth_events"] = 1 if out.get("born_variable") else 0
        out["prototype_count"] = int(prototype_count)
        out["class_count"] = int(class_count)
        # merge/split are not fully modeled; log minimal counters
        out["merge_events"] = max(0, int(prototype_count) - int(class_count)) if class_count else 0
        out["split_events"] = 0
        # monotonic birth counter for QA evidence
        try:
            birth_count = int(primitives.get("birth_count", 0))
        except Exception:
            birth_count = 0
        if out.get("born_variable"):
            birth_count += 1
        primitives["birth_count"] = birth_count
        out["birth_count"] = int(birth_count)
        if out.get("born_variable"):
            out["birth_suggest"] = 1
        bus = primitives.get("co_bus")
        publish_signal(bus, "EB_GHVC.pressure",  out.get("pressure", 0.0))
        publish_signal(bus, "EB_GHVC.mdl_gain",  out.get("mdl_gain", 0.0))
        publish_signal(bus, "EB_GHVC.birth_suggest", float(out.get("birth_suggest", 0)))
        publish_signal(bus, "birth_events", float(out.get("birth_events", 0)))
        publish_signal(bus, "merge_events", float(out.get("merge_events", 0)))
        publish_signal(bus, "split_events", float(out.get("split_events", 0)))
        publish_signal(bus, "prototype_count", float(out.get("prototype_count", 0)))
        publish_signal(bus, "class_count", float(out.get("class_count", 0)))
        publish_signal(bus, "cap_hits", float(out.get("cap_hits", 0)))
        publish_signal(bus, "birth_count", float(out.get("birth_count", 0)))
        if not no_inputs:
            self._last_out = dict(out)
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        if self._last_out is None:
            return self.update(observation, primitives, header, feedback)
        bus = primitives.get("co_bus")
        publish_signal(bus, "EB_GHVC.pressure",  self._last_out.get("pressure", 0.0))
        publish_signal(bus, "EB_GHVC.mdl_gain",  self._last_out.get("mdl_gain", 0.0))
        publish_signal(bus, "EB_GHVC.birth_suggest", float(self._last_out.get("birth_suggest", 0)))
        publish_signal(bus, "birth_events", float(self._last_out.get("birth_events", 0)))
        publish_signal(bus, "merge_events", float(self._last_out.get("merge_events", 0)))
        publish_signal(bus, "split_events", float(self._last_out.get("split_events", 0)))
        publish_signal(bus, "prototype_count", float(self._last_out.get("prototype_count", 0)))
        publish_signal(bus, "class_count", float(self._last_out.get("class_count", 0)))
        publish_signal(bus, "cap_hits", float(self._last_out.get("cap_hits", 0)))
        publish_signal(bus, "birth_count", float(self._last_out.get("birth_count", 0)))
        return dict(self._last_out)
