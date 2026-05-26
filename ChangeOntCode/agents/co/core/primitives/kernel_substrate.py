from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional


def _freeze(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): _freeze(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_freeze(v) for v in x]
    return x


class KernelSubstrate:
    """
    Explicit runtime object for the kernel substrate.

    This is not a hidden full world-state. It is the bounded local unfolding
    currently held by the running local structure: a compact, rolling view of
    local traces, current comparison/admissibility signals, regime indicators,
    and actionable continuation context.
    """

    def __init__(self, history_len: int = 32, signal_limit: int = 96) -> None:
        self.history_len = max(4, int(history_len))
        self.signal_limit = max(16, int(signal_limit))
        self.state: Dict[str, Any] = {
            "step": 0,
            "family": None,
            "observation": {},
            "feedback": {},
            "history_tail": [],
            "trace_tail": [],
            "signals": {},
            "comparison": {},
            "admissibility": {},
            "regime": {},
            "regime_signature": {},
            "operative_invariants": [],
            "representation": {},
            "continuation": {},
            "header": {},
        }

    def _tail(self, seq: Iterable[Any]) -> List[Any]:
        xs = list(seq)[-self.history_len :]
        return [_freeze(v) for v in xs]

    def pre_update(self, observation: Optional[Dict[str, Any]], feedback: Optional[Dict[str, Any]], header: Any) -> Dict[str, Any]:
        obs = dict(observation or {})
        fb = dict(feedback or {})
        self.state["step"] = int(self.state.get("step", 0) or 0) + 1
        self.state["family"] = obs.get("family", self.state.get("family"))
        # bounded local hold only
        self.state["observation"] = {
            "family": obs.get("family"),
            "t": obs.get("t", obs.get("step")),
            "action_space": list(obs.get("action_space", []))[:32],
            "observation": _freeze(obs.get("observation")),
        }
        self.state["feedback"] = {
            "action": _freeze(fb.get("action")),
            "reward": fb.get("reward"),
        }
        if "history" in obs:
            self.state["history_tail"] = self._tail(obs.get("history", []))
        elif "trace" in obs:
            self.state["history_tail"] = self._tail(obs.get("trace", []))
        if "trace" in obs:
            self.state["trace_tail"] = self._tail(obs.get("trace", []))
        elif "history" in obs:
            self.state["trace_tail"] = self._tail(obs.get("history", []))
        self.state["header"] = _freeze(getattr(header, "state", {})) if header is not None else {}
        bus = None
        signals = {}
        try:
            bus = getattr(header, "primitives", None)
        except Exception:
            bus = None
        controller = None
        if isinstance(feedback, dict):
            pass
        return self.snapshot()

    def post_update(self, primitives: Dict[str, Any], metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        bus = primitives.get("signal_bus")
        signals = bus.signals() if bus is not None and hasattr(bus, "signals") else {}
        if len(signals) > self.signal_limit:
            # keep the most recent lexicographically-stable subset for boundedness
            keys = sorted(signals.keys())[-self.signal_limit :]
            signals = {k: float(signals[k]) for k in keys}
        self.state["signals"] = dict(signals)
        self.state["comparison"] = {
            "continuity_conf": float(signals.get("EC_Identity.continuity_conf", 0.0)),
            "fracture_pressure": float(signals.get("EC_Identity.fracture_pressure", 0.0)),
            "reid_frequency": float(signals.get("EC_Identity.reid_frequency", 0.0)),
            "directional_burden": float(signals.get("P1_Bend.directional_burden", 0.0)),
        }
        self.state["admissibility"] = {
            "identity_admissibility": float(signals.get("Identity.admissibility", 0.0)),
            "admissible_loss": float(signals.get("EE_Compressibility.admissible_loss", 0.0)),
            "closure_stability": float(signals.get("EE_Compressibility.closure_stability", 0.0)),
        }
        self.state["regime"] = {
            "gauge_coherence": float(signals.get("P2_Gauge.transport_coherence", 0.0)),
            "gauge_gain": float(signals.get("EA_HAQ.gauge_gain", 0.0)),
            "router_dyn": float(signals.get("EF_RouterGIL.dynamicity", 0.0)),
            "reeval_pressure": float(signals.get("P16_RemainingBurden.reachability_deficit", 0.0)),
            "frame_shift": float(signals.get("EC_Identity.fit_mismatch", 0.0)),
        }
        self.state["continuation"] = {
            "remaining_transformation_burden": float(signals.get("P16_RemainingBurden.transformation_burden", 0.0)),
            "reachability_deficit": float(signals.get("P16_RemainingBurden.reachability_deficit", 0.0)),
            "admissibility_deficit": float(signals.get("P16_RemainingBurden.admissibility_deficit", 0.0)),
        }
        controller = primitives.get("operative_relevance") if isinstance(primitives, dict) else None
        if controller is not None and hasattr(controller, "assess"):
            try:
                obs = dict(self.state.get("observation", {}) or {})
                obs.update({
                    "family": self.state.get("family"),
                    "history": list(self.state.get("history_tail", [])),
                    "trace": list(self.state.get("trace_tail", [])),
                })
                assessed = controller.assess(obs, signals, advance=True)
                self.state["regime_signature"] = dict(assessed.get("regime_signature", {}))
                self.state["operative_invariants"] = list(assessed.get("operative_invariants", []))
                self.state["representation"] = dict(assessed.get("representation", {}))
                if bus is not None and hasattr(bus, "set"):
                    rs = assessed.get("regime_signature", {}) or {}
                    bus.set("OperativeRelevance.operative_difference", float(assessed.get("operative_difference", 0.0)))
                    bus.set("OperativeRelevance.burden_accumulation", float(rs.get("burden_accumulation", 0.0)))
                    bus.set("OperativeRelevance.admissibility_decay", float(rs.get("admissibility_decay", 0.0)))
                    bus.set("OperativeRelevance.history_dependence", float(rs.get("history_dependence", 0.0)))
                    bus.set("OperativeRelevance.invariant_stability", float(rs.get("invariant_stability", 0.0)))
                    bus.set("OperativeRelevance.scalarizability", float(rs.get("scalarizability", 0.0)))
                    bus.set("OperativeRelevance.collapse_readiness", float(rs.get("collapse_readiness", 0.0)))
            except Exception:
                pass
        if isinstance(metrics, dict):
            self.state["metrics"] = {str(k): _freeze(v) for k, v in list(metrics.items())[:64]}
        return self.snapshot()

    def snapshot(self) -> Dict[str, Any]:
        return {k: _freeze(v) for k, v in self.state.items()}


# Backward-compatible registry alias
BoundedLocalUnfoldingSubstrate = KernelSubstrate
