# agents/co/core/elements/EA_haq.py
from __future__ import annotations
from typing import Dict, Any, Optional
from dataclasses import dataclass
from ._shared import publish_signal, get_semantic

def _get_bus(primitives: Dict[str, Any]):
    return primitives.get("signal_bus", None)

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
    pe_weight: float = 1.0
    gain_weight: float = 1.0
    resid_weight: float = 0.25
    history_len: int = 64
    ema_alpha: float = 0.2

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.alpha = float(params.get("alpha0", 0.0))
        self.kappa = float(params.get("kappa", self.kappa))
        self.gauge_policy = str(params.get("gauge_policy", self.gauge_policy))
        self.gauge_eta = float(params.get("gauge_eta", self.gauge_eta))
        self.gauge_lam = float(params.get("gauge_lam", self.gauge_lam))
        self.pe_weight = float(params.get("pe_weight", self.pe_weight))
        self.gain_weight = float(params.get("gain_weight", self.gain_weight))
        self.resid_weight = float(params.get("resid_weight", self.resid_weight))
        self.history_len = max(1, int(params.get("history_len", self.history_len)))
        self.ema_alpha = float(params.get("ema_alpha", self.ema_alpha))
        return self

    def _update_alpha(self, z_pe: float, z_gain: float, cap: float):
        target = max(0.0, min(cap, z_pe + z_gain))
        rate = max(0.0, min(1.0, self.kappa * self.ema_alpha))
        self.alpha += rate * (target - self.alpha)
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

        # auxiliary public signals in observation (if adapters set them)
        sig = observation.get("signals", {})
        z_pe   = float(sig.get("z_PE", z_pe))
        z_gain = float(sig.get("z_gain", z_gain))
        var_resid = float(sig.get("var_resid", 0.0))

        gain = 1.0
        coherence = 0.0
        P2 = primitives.get("P2")
        if P2 is None:
            raise RuntimeError("EA_HAQ requires primitives['P2'] (P2_Gauge) but it is missing.")
        try:
            p2_state = primitives.get("p2_state")
            if p2_state is None:
                p2_state = {}
                primitives["p2_state"] = p2_state
            bus = primitives.get("signal_bus")
            bus_sig = bus.signals() if bus is not None and hasattr(bus, "signals") else {}
            auxiliary = {
                "continuity_conf": float(bus_sig.get("EC_Identity.continuity_conf", 0.0) or 0.0),
                "fracture_pressure": float(bus_sig.get("EC_Identity.fracture_pressure", 0.0) or 0.0),
                "frame_shift": float(bus_sig.get("EF_RouterGIL.dynamicity", 0.0) or 0.0),
                "remaining_burden": float(bus_sig.get("P16_RemainingBurden.transformation_burden", 0.0) or 0.0),
                "identity_admissibility": float(bus_sig.get("Identity.admissibility", 0.0) or 0.0),
                "directional_burden": float(bus_sig.get("P1_Bend.directional_burden", 0.0) or 0.0),
            }
            if hasattr(P2, "extract_signals"):
                signals = P2.extract_signals(observation, auxiliary=auxiliary)
            else:
                signals = {"z_PE": float(z_pe), "z_gain": float(z_gain), "var_resid": float(var_resid), **auxiliary}
            # Prefer stateful gauge-step API when present.
            if hasattr(P2, "gauge_step"):
                p2_state, alpha = P2.gauge_step(
                    signals,
                    state=p2_state,
                    policy_name=self.gauge_policy,
                    eta=self.gauge_eta,
                    lam=self.gauge_lam,
                )
                coherence_local = float(p2_state.get("coherence", 0.0) or 0.0)
                gain = 1.0 + 0.65 * float(alpha) + 0.35 * coherence_local
            elif hasattr(P2, "gauge_gain"):
                gain_only = P2.gauge_gain(
                    signals,
                    state=p2_state,
                    policy_name=self.gauge_policy,
                    eta=self.gauge_eta,
                    lam=self.gauge_lam,
                )
                gain = 1.0 + float(gain_only)
            elif hasattr(P2, "update_gauge"):
                A_state = p2_state.get("A_state", {})
                res = P2.update_gauge(
                    A_state,
                    signals,
                    policy_name=self.gauge_policy,
                    eta=self.gauge_eta,
                    lam=self.gauge_lam,
                    state=p2_state,
                )
                if isinstance(res, tuple) and len(res) == 3:
                    A_state, alpha, p2_state = res
                else:
                    A_state, alpha = res
                p2_state["A_state"] = A_state
                gain = 1.0 + float(alpha)
            else:
                raise RuntimeError("P2_Gauge has no supported API (gauge_step/gauge_gain/update_gauge).")
            primitives["p2_state"] = p2_state
            coherence = float(p2_state.get("coherence", 0.0) or 0.0)
        except Exception:
            raise

        # Multiplicative modulation: P2 gain modulates base (z_pe + z_gain).
        sem = get_semantic(primitives)
        sc_mul = sem.get("SC_MultiplicativeCoupling")
        sc_add = sem.get("SC_AdditiveBlend")
        if sc_mul is None or sc_add is None:
            raise RuntimeError("EA_HAQ requires semantic combinators SC_MultiplicativeCoupling and SC_AdditiveBlend.")

        z_pe_mod = sc_mul.couple(z_pe * self.pe_weight, gain)
        z_gain_mod = sc_mul.couple(z_gain * self.gain_weight, gain)
        resid_mod = max(0.0, float(var_resid) * self.resid_weight)
        combined = sc_add.combine([z_pe_mod, z_gain_mod, resid_mod])
        self._update_alpha(z_pe_mod, z_gain_mod, cap)

        # publish richer EA contract for translators and diagnostics
        bus = _get_bus(primitives)
        publish_signal(bus, "EA_HAQ.novelty", float(self.alpha))
        publish_signal(bus, "EA_HAQ.holonomy_defect", float(z_pe_mod))
        publish_signal(bus, "EA_HAQ.gauge_gain", float(gain))
        publish_signal(bus, "P2_Gauge.transport_coherence", float(coherence))
        publish_signal(bus, "EA_HAQ.modulated_pe", float(z_pe_mod))
        publish_signal(bus, "EA_HAQ.modulated_gain", float(z_gain_mod))
        publish_signal(bus, "EA_HAQ.warp_strength", float(combined))

        return {"haq_alpha": float(self.alpha), "z_PE": float(z_pe), "z_gain": float(z_gain), "z_combined": float(combined), "haq_gain": float(gain), "haq_resid": float(var_resid)}
