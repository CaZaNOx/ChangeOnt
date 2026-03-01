# agents/co/core/elements/EA_haq.py
from __future__ import annotations
from typing import Dict, Any, Optional
from dataclasses import dataclass
from ._shared import publish_signal, get_semantic

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
    COMBINATOR_DEPS = ("SC_MultiplicativeCoupling", "SC_AdditiveBlend")
    FORMULA_STATUS = "provisional"

    alpha: float = 0.0
    kappa: float = 0.2  # learning stiffness
    gauge_policy: str = "R_gated"
    gauge_eta: float = 0.1
    gauge_lam: float = 0.02

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.alpha = float(params.get("alpha0", 0.0))
        self.kappa = float(params.get("kappa", self.kappa))
        self.gauge_policy = str(params.get("gauge_policy", self.gauge_policy))
        self.gauge_eta = float(params.get("gauge_eta", self.gauge_eta))
        self.gauge_lam = float(params.get("gauge_lam", self.gauge_lam))
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

        # Primary primitive: P2_Gauge. Use it as the explicit modulation source.
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

        gain = 1.0
        P2 = primitives.get("P2")
        if P2 is None:
            raise RuntimeError("EA_HAQ requires primitives['P2'] (P2_Gauge) but it is missing.")
        try:
            p2_state = primitives.get("p2_state")
            if p2_state is None:
                p2_state = {}
                primitives["p2_state"] = p2_state
            signals = {"z_PE": float(z_pe), "z_gain": float(z_gain)}
            if isinstance(sig, dict) and "var_resid" in sig:
                signals["var_resid"] = float(sig.get("var_resid", 1.0))
            # Prefer explicit P2 API if present.
            if hasattr(P2, "gauge_gain"):
                p2_state, gain = P2.gauge_gain(
                    signals,
                    state=p2_state,
                    policy_name=self.gauge_policy,
                    eta=self.gauge_eta,
                    lam=self.gauge_lam,
                )
            elif hasattr(P2, "gauge_step"):
                p2_state, alpha = P2.gauge_step(
                    signals,
                    state=p2_state,
                    policy_name=self.gauge_policy,
                    eta=self.gauge_eta,
                    lam=self.gauge_lam,
                )
                gain = 1.0 + float(alpha)
            elif hasattr(P2, "update_gauge"):
                A_state = p2_state.get("A_state", {})
                A_state, alpha = P2.update_gauge(
                    A_state,
                    signals,
                    policy_name=self.gauge_policy,
                    eta=self.gauge_eta,
                    lam=self.gauge_lam,
                )
                p2_state["A_state"] = A_state
                gain = 1.0 + float(alpha)
            else:
                raise RuntimeError("P2_Gauge has no supported API (gauge_gain/gauge_step/update_gauge).")
            primitives["p2_state"] = p2_state
        except Exception:
            raise

        # Multiplicative modulation: P2 gain modulates base (z_pe + z_gain).
        sem = get_semantic(primitives)
        sc_mul = sem.get("SC_MultiplicativeCoupling")
        sc_add = sem.get("SC_AdditiveBlend")
        if sc_mul is None or sc_add is None:
            raise RuntimeError("EA_HAQ requires semantic combinators SC_MultiplicativeCoupling and SC_AdditiveBlend.")

        z_pe_mod = sc_mul.couple(z_pe, gain)
        z_gain_mod = sc_mul.couple(z_gain, gain)
        combined = sc_add.combine([z_pe_mod, z_gain_mod])
        self._update_alpha(z_pe_mod, z_gain_mod, cap)

        # publish a simple novelty scalar (translator reads EA_HAQ.novelty)
        bus = _get_bus(primitives)
        publish_signal(bus, "EA_HAQ.novelty", float(self.alpha))

        return {"haq_alpha": float(self.alpha), "z_PE": float(z_pe), "z_gain": float(z_gain), "z_combined": float(combined)}
