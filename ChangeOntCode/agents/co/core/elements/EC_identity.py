# agents/co/core/elements/EC_identity.py
from __future__ import annotations
from typing import Dict, Any, Iterable, List
from dataclasses import dataclass
from ..primitives.identity import bend_distance, closure, TraceMemory
from ..primitives.P1_bend_metric import L as P1_L, PAD_TOKEN as P1_PAD_TOKEN
from ._shared import publish_signal

@dataclass
class EC_Identity:
    """
    EC_Identity (v1): local identity judgment under bend distance.
    Primitive deps (intended): P1_BendMetric, canonical identity memory; optional P12_ClosureQuotient later.
    Combinator form (intended): SC_GatedThreshold (primary).
    Formula status: provisional (threshold structure binding).
    """
    PRIMITIVE_DEPS = ("P1_BendMetric", "identity memory", "P12_ClosureQuotient (optional)")
    COMBINATOR_FORM = "SC_GatedThreshold"
    FORMULA_STATUS = "provisional"

    mem_len: int = 64
    trace_len: int = P1_L

    def configure(self, params, context):
        try:
            self.mem_len = int(params.get("mem_len", self.mem_len))
            self.trace_len = int(params.get("trace_len", self.trace_len))
        except Exception:
            pass
        return self

    def _normalize_trace(self, trace: Iterable[Any]) -> List[Any]:
        t = list(trace)
        if self.trace_len > 0 and len(t) > self.trace_len:
            t = t[-self.trace_len:]
        if self.trace_len > 0 and len(t) < self.trace_len:
            t = [P1_PAD_TOKEN] * (self.trace_len - len(t)) + t
        return t

    def _get_eps(self, header: Any) -> float:
        eps_id = getattr(getattr(header, "state", object()), "eps_id", None)
        if eps_id is None:
            return 0.20
        try:
            return float(eps_id)
        except Exception:
            return 0.20

    def _run_core(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any) -> Dict[str, Any]:
        eps = self._get_eps(header)
        hist = list(observation.get("history", ()))
        trace = observation.get("trace", hist)
        if isinstance(trace, (list, tuple)):
            trace = self._normalize_trace(trace)
        else:
            trace = self._normalize_trace(hist)

        mem = primitives.get("id_mem")
        if mem is None:
            mem = TraceMemory(maxlen=self.mem_len)
            primitives["id_mem"] = mem

        prev = mem.traces()
        last_d = 1.0
        identity_ok = False
        bend_trigger = 0
        if prev and trace:
            last_d = min(float(bend_distance(trace, p)) for p in prev)
            identity_ok = bool(last_d <= eps)
            bend_trigger = 1 if (last_d > eps) else 0

        # compute class count from closure over recent traces
        classes = closure(prev + ([tuple(trace)] if trace else []), eps) if (prev or trace) else []
        class_count = len(classes)

        # update memory after computing distance
        if trace:
            mem.push(tuple(trace))

        return {
            "eps": eps,
            "identity_ok": identity_ok,
            "last_d": float(last_d),
            "bend_trigger": int(bend_trigger),
            "class_count": int(class_count),
        }

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        # Update pass only records the last action for trace construction.
        if feedback:
            try:
                act = feedback.get("action", None)
            except Exception:
                act = None
            if act is not None:
                mem = primitives.get("id_mem")
                if mem is None:
                    mem = TraceMemory(maxlen=self.mem_len)
                    primitives["id_mem"] = mem
                mem.last_action = act
        return {}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        obs = dict(observation or {})
        # If no explicit history/trace provided, use last action from id_mem (if any).
        if "history" not in obs and "trace" not in obs:
            mem = primitives.get("id_mem")
            act = getattr(mem, "last_action", None) if mem is not None else None
            obs["history"] = [] if act is None else [act]

        out = self._run_core(obs, primitives, header)
        bus = primitives.get("co_bus")
        publish_signal(bus, "EC_Identity.same",   1.0 if out["identity_ok"] else 0.0)
        publish_signal(bus, "EC_Identity.last_d", out["last_d"])
        publish_signal(bus, "bend_triggers", float(out.get("bend_trigger", 0)))
        return out
