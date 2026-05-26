from __future__ import annotations
from collections import deque
from statistics import mean
from typing import Any, Dict, Optional, Deque


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


class RemainingTransformationBurden:
    """
    Bounded doctrinal realization of remaining transformation / reachability burden.

    Instead of only blending current signals, this primitive maintains a running
    target continuation profile derived from recently successful / stable local states.
    Burden is then computed as the positive deficit between the current local state and
    the learned admissible target region.
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None, history_len: int = 16) -> None:
        base = {
            "continuity": 0.30,
            "admissibility": 0.30,
            "fracture": 0.20,
            "bend": 0.10,
            "frame_shift": 0.10,
        }
        if isinstance(weights, dict):
            base.update({k: float(v) for k, v in weights.items() if k in base})
        self.weights = base
        self.history_len = max(4, int(history_len))
        self._target: Dict[str, float] = {
            "continuity": 0.85,
            "admissibility": 0.80,
            "fracture": 0.15,
            "bend": 0.15,
            "frame_shift": 0.15,
        }
        self._target_hist: Deque[Dict[str, float]] = deque(maxlen=self.history_len)
        self._last: Dict[str, float] = {}

    def _signals(self, observation: Dict[str, Any], primitives: Dict[str, Any]) -> Dict[str, float]:
        bus = primitives.get("signal_bus")
        sig = bus.signals() if bus is not None and hasattr(bus, "signals") else {}
        obs_sig = dict(observation.get("signals", {})) if isinstance(observation, dict) else {}
        continuity = float(sig.get("EC_Identity.continuity_conf", obs_sig.get("continuity_conf", 0.0)))
        fracture = float(sig.get("EC_Identity.fracture_pressure", obs_sig.get("fracture_pressure", 0.0)))
        admiss = float(sig.get("Identity.admissibility", obs_sig.get("identity_admissibility", 0.0)))
        bend = float(sig.get("P1_Bend.directional_burden", obs_sig.get("directional_burden", 0.0)))
        gauge = float(sig.get("P2_Gauge.transport_coherence", obs_sig.get("gauge_coherence", 0.0)))
        frame_shift = float(obs_sig.get("frame_shift", sig.get("frame_shift", 0.0) or (1.0 - gauge)))
        return {
            "continuity": _clamp(continuity),
            "fracture": _clamp(fracture),
            "admissibility": _clamp(admiss),
            "bend": _clamp(bend),
            "frame_shift": _clamp(frame_shift),
            "gauge": _clamp(gauge),
        }

    def _successful(self, s: Dict[str, float], observation: Dict[str, Any]) -> bool:
        reward = 0.0
        fb = observation.get("feedback", {}) if isinstance(observation, dict) else {}
        if isinstance(fb, dict):
            try:
                reward = float(fb.get("reward", 0.0) or 0.0)
            except Exception:
                reward = 0.0
        return bool(s["continuity"] >= 0.60 and s["admissibility"] >= 0.55 and s["fracture"] <= 0.45 and reward >= -0.25)

    def _update_target(self, s: Dict[str, float], observation: Dict[str, Any]) -> None:
        if self._successful(s, observation):
            snap = {
                "continuity": s["continuity"],
                "admissibility": s["admissibility"],
                "fracture": s["fracture"],
                "bend": s["bend"],
                "frame_shift": s["frame_shift"],
            }
            self._target_hist.append(snap)
        if self._target_hist:
            self._target = {k: float(mean(item[k] for item in self._target_hist)) for k in self._target}

    def assess(self, observation: Dict[str, Any], primitives: Dict[str, Any]) -> Dict[str, float]:
        s = self._signals(observation, primitives)
        self._update_target(s, observation)
        continuity_deficit = max(0.0, self._target["continuity"] - s["continuity"])
        admissibility_deficit = max(0.0, self._target["admissibility"] - s["admissibility"])
        fracture_excess = max(0.0, s["fracture"] - self._target["fracture"])
        bend_excess = max(0.0, s["bend"] - self._target["bend"])
        shift_excess = max(0.0, s["frame_shift"] - self._target["frame_shift"])
        reachability_deficit = _clamp(0.45 * continuity_deficit + 0.30 * admissibility_deficit + 0.15 * bend_excess + 0.10 * shift_excess)
        burden = _clamp(
            self.weights["continuity"] * continuity_deficit
            + self.weights["admissibility"] * admissibility_deficit
            + self.weights["fracture"] * fracture_excess
            + self.weights["bend"] * bend_excess
            + self.weights["frame_shift"] * shift_excess
        )
        out = {
            "transformation_burden": float(burden),
            "reachability_deficit": float(reachability_deficit),
            "admissibility_deficit": float(admissibility_deficit),
            "continuity_deficit": float(continuity_deficit),
            "target_continuity": float(self._target["continuity"]),
            "target_admissibility": float(self._target["admissibility"]),
        }
        self._last = out
        return out

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any = None, feedback: Dict[str, Any] | None = None) -> Dict[str, float]:
        obs = dict(observation or {})
        if feedback is not None and "feedback" not in obs:
            obs["feedback"] = feedback
        out = self.assess(obs, primitives or {})
        bus = primitives.get("signal_bus") if isinstance(primitives, dict) else None
        if bus is not None and hasattr(bus, "set"):
            bus.set("P16_RemainingBurden.transformation_burden", out["transformation_burden"])
            bus.set("P16_RemainingBurden.reachability_deficit", out["reachability_deficit"])
            bus.set("P16_RemainingBurden.admissibility_deficit", out["admissibility_deficit"])
            bus.set("P16_RemainingBurden.continuity_deficit", out["continuity_deficit"])
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any = None, feedback: Dict[str, Any] | None = None) -> Dict[str, float]:
        return self.update(observation, primitives, header, feedback)

    def report(self) -> Dict[str, float]:
        return dict(self._last)
