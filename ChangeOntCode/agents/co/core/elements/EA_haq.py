# agents/co/core/elements/EA_haq.py
from __future__ import annotations
from typing import Dict, Any, Optional
from dataclasses import dataclass
from ._shared import publish_signal

def _get_bus(primitives: Dict[str, Any]):
    return primitives.get("co_bus", None)

@dataclass
class EA_HAQ:
    """
    EA_HAQ (v1): history-adaptive modulation.
    Primitive deps (intended): P2_Gauge (primary), optional history/state support, optional P7_Precision later.
    Combinator form (intended): SC_MultiplicativeCoupling (primary), optional SC_AdditiveBlend.
    Formula status: provisional.
    """
    PRIMITIVE_DEPS = ("P2_Gauge", "history/state support (optional)", "P7_Precision (optional)")
    COMBINATOR_FORM = "SC_MultiplicativeCoupling (+ optional SC_AdditiveBlend)"
    FORMULA_STATUS = "provisional"

    alpha: float = 0.0
    kappa: float = 0.2  # learning stiffness

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.alpha = float(params.get("alpha0", 0.0))
        self.kappa = float(params.get("kappa", self.kappa))
        return self

    def _update_alpha(self, z_pe: float, z_gain: float, cap: float):
        target = max(0.0, min(cap, z_pe + z_gain))
        self.alpha += self.kappa * (target - self.alpha)
        self.alpha = max(0.0, min(cap, self.alpha))

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        return {}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        hs = getattr(header, "state", header)
        cap = float(getattr(hs, "alpha_cap", 1.0))

        # Intended primitive: P2_Gauge. Current v1 uses z_PE / z_gain as a proxy modulation input.
        # Keep this minimal and stable; exact gauge coupling is still provisional.
        z_pe = 0.0
        z_gain = 0.0
        P1 = primitives.get("P1")  # bend/prediction error surrogate?
        P5 = primitives.get("P5")  # temporal ops / gain?

        try:
            # best-effort: many P* are modules/classes; check common hooks
            if hasattr(P1, "z_pe"):       z_pe = float(P1.z_pe(observation))
            elif hasattr(P1, "surprise"): z_pe = float(P1.surprise(observation))
        except Exception:
            pass

        try:
            if hasattr(P5, "gain"):       z_gain = float(P5.gain(observation))
            elif hasattr(P5, "z_gain"):   z_gain = float(P5.z_gain(observation))
        except Exception:
            pass

        # fallback to signals in observation (if adapters set them)
        sig = observation.get("signals", {})
        z_pe   = float(sig.get("z_PE", z_pe))
        z_gain = float(sig.get("z_gain", z_gain))

        self._update_alpha(z_pe, z_gain, cap)

        # publish a simple novelty scalar (translator reads EA_HAQ.novelty)
        bus = _get_bus(primitives)
        publish_signal(bus, "EA_HAQ.novelty", float(self.alpha))

        return {"haq_alpha": float(self.alpha), "z_PE": float(z_pe), "z_gain": float(z_gain)}
