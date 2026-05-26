from __future__ import annotations
from typing import Dict, Tuple, Any, Optional
import math

DEFAULT_POLICY = "R_gated"
DEFAULT_ETA = 0.1
DEFAULT_LAM = 0.02

_FEATURES = (
    "continuity_conf",
    "identity_admissibility",
    "fracture_pressure",
    "remaining_burden",
    "directional_burden",
    "frame_shift",
    "reeval_pressure",
)


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _frame_vector(signals: Dict[str, float]) -> Dict[str, float]:
    return {
        "continuity_conf": _clamp01(signals.get("continuity_conf", signals.get("continuity", 0.0))),
        "identity_admissibility": _clamp01(signals.get("identity_admissibility", signals.get("admissibility", 0.0))),
        "fracture_pressure": _clamp01(signals.get("fracture_pressure", 0.0)),
        "remaining_burden": _clamp01(signals.get("remaining_burden", signals.get("reachability_deficit", 0.0))),
        "directional_burden": _clamp01(signals.get("directional_burden", 0.0)),
        "frame_shift": _clamp01(signals.get("frame_shift", 0.0)),
        "reeval_pressure": _clamp01(signals.get("reeval_pressure", 0.0)),
    }


def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
    dot = sum(float(a.get(k, 0.0)) * float(b.get(k, 0.0)) for k in _FEATURES)
    na = math.sqrt(sum(float(a.get(k, 0.0)) ** 2 for k in _FEATURES))
    nb = math.sqrt(sum(float(b.get(k, 0.0)) ** 2 for k in _FEATURES))
    if na <= 1e-9 or nb <= 1e-9:
        return 1.0
    return _clamp01(dot / (na * nb))


def _predicted_frame(state: Optional[Dict[str, Any]]) -> Dict[str, float]:
    if not state:
        return {k: 0.0 for k in _FEATURES}
    prev = dict(state.get("prev_frame", {}) or {})
    drift = dict(state.get("drift", {}) or {})
    bias = dict(state.get("transport_bias", {}) or {})
    out: Dict[str, float] = {}
    for k in _FEATURES:
        out[k] = _clamp01(float(prev.get(k, 0.0)) + float(drift.get(k, 0.0)) + 0.25 * float(bias.get(k, 0.0)))
    return out


def warp_costs(base_costs: Dict, A_state: Dict, alpha: float) -> Dict:
    out = {}
    g = float(A_state.get("__global__", 0.0))
    for k, c in base_costs.items():
        a = float(A_state.get(k, g))
        cc = max(0.0, float(c) * (1.0 + float(alpha) * a))
        out[k] = cc
    return out


def transport_coherence(signals: Dict[str, float], state: Optional[Dict[str, Any]] = None) -> float:
    cur = _frame_vector(signals)
    pred = _predicted_frame(state)
    cosine = _cosine(cur, pred)
    residual = sum(abs(cur[k] - pred[k]) for k in _FEATURES) / float(len(_FEATURES))
    continuity = cur["continuity_conf"]
    admiss = cur["identity_admissibility"]
    fracture = cur["fracture_pressure"]
    burden = cur["remaining_burden"]
    bend = cur["directional_burden"]
    shift = cur["frame_shift"]
    reeval = cur["reeval_pressure"]
    raw = (
        0.24 * cosine
        + 0.18 * continuity
        + 0.18 * admiss
        + 0.12 * (1.0 - residual)
        + 0.10 * (1.0 - fracture)
        + 0.08 * (1.0 - burden)
        + 0.05 * (1.0 - bend)
        + 0.03 * (1.0 - shift)
        + 0.02 * (1.0 - reeval)
    )
    return _clamp01(raw)


def update_gauge(A_state: Dict, signals: Dict, policy_name: str = DEFAULT_POLICY,
                 eta: float = DEFAULT_ETA, lam: float = DEFAULT_LAM, state: Optional[Dict[str, Any]] = None) -> Tuple[Dict, float, Dict[str, Any]]:
    z_pe = float(signals.get("z_PE", 0.0))
    z_gain = float(signals.get("z_gain", 0.0))
    var_resid = max(1e-6, float(signals.get("var_resid", 1.0)))

    cur = _frame_vector(signals)
    if state is None:
        state = {}
    pred = _predicted_frame(state)
    coherence = transport_coherence(signals, state=state)

    if policy_name == "R_ratio":
        alpha = _clamp01(coherence * (max(0.0, z_pe) / (1.0 + var_resid)))
    else:
        gate = 1.0 if (z_gain > 0 and z_pe > 0) else 0.0
        alpha = _clamp01(gate * coherence * (eta * max(0.0, z_pe)))

    new_A = {k: (1.0 - lam) * float(v) for k, v in (A_state or {}).items()}
    global_prev = float(new_A.get("__global__", 0.0))
    new_A["__global__"] = (1.0 - lam) * global_prev + lam * coherence + 0.10 * max(0.0, z_pe)
    for k in _FEATURES:
        prev_w = float(new_A.get(k, global_prev))
        # Features that indicate instability increase local modulation pressure.
        instability = cur[k] if k in {"fracture_pressure", "remaining_burden", "directional_burden", "frame_shift", "reeval_pressure"} else (1.0 - cur[k])
        new_A[k] = _clamp01((1.0 - lam) * prev_w + lam * instability)
    new_A["__coherence__"] = float(coherence)

    new_state = dict(state)
    prev_frame = dict(state.get("prev_frame", {}) or {})
    drift = {k: _clamp01(cur[k] - prev_frame.get(k, 0.0) + 0.5) - 0.5 for k in _FEATURES}
    new_state["prev_frame"] = dict(cur)
    new_state["drift"] = drift
    new_state["transport_bias"] = {
        k: _clamp01(0.8 * float(state.get("transport_bias", {}).get(k, 0.0)) + 0.2 * (pred[k] - cur[k] + 0.5)) - 0.5
        for k in _FEATURES
    }
    new_state["residual"] = float(sum(abs(cur[k] - pred[k]) for k in _FEATURES) / float(len(_FEATURES)))
    new_state["coherence_ema"] = _clamp01(0.85 * float(state.get("coherence_ema", coherence)) + 0.15 * coherence)
    return new_A, alpha, new_state


def extract_signals(observation: Dict[str, Any], auxiliary: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    out: Dict[str, float] = {}
    sig = observation.get("signals", {}) if isinstance(observation, dict) else {}
    if isinstance(sig, dict):
        out["z_PE"] = float(sig.get("z_PE", 0.0))
        out["z_gain"] = float(sig.get("z_gain", 0.0))
        out["var_resid"] = float(sig.get("var_resid", 1.0))
        out["continuity_conf"] = float(sig.get("continuity_conf", sig.get("EC_Identity.continuity_conf", 0.0)))
        out["fracture_pressure"] = float(sig.get("fracture_pressure", sig.get("EC_Identity.fracture_pressure", 0.0)))
        out["identity_admissibility"] = float(sig.get("identity_admissibility", sig.get("Identity.admissibility", 0.0)))
        out["directional_burden"] = float(sig.get("directional_burden", sig.get("P1_Bend.directional_burden", 0.0)))
        out["remaining_burden"] = float(sig.get("remaining_burden", sig.get("P16_RemainingBurden.transformation_burden", 0.0)))
        out["frame_shift"] = float(sig.get("frame_shift", 0.0))
        out["reeval_pressure"] = float(sig.get("reeval_pressure", 0.0))
    ks = observation.get("_kernel_substrate", {}) if isinstance(observation, dict) else {}
    if isinstance(ks, dict):
        cmpf = ks.get("comparison", {}) if isinstance(ks.get("comparison", {}), dict) else {}
        admf = ks.get("admissibility", {}) if isinstance(ks.get("admissibility", {}), dict) else {}
        regf = ks.get("regime", {}) if isinstance(ks.get("regime", {}), dict) else {}
        conf = ks.get("continuation", {}) if isinstance(ks.get("continuation", {}), dict) else {}
        out.setdefault("continuity_conf", float(cmpf.get("continuity_conf", 0.0) or 0.0))
        out.setdefault("fracture_pressure", float(cmpf.get("fracture_pressure", 0.0) or 0.0))
        out.setdefault("identity_admissibility", float(admf.get("identity_admissibility", 0.0) or 0.0))
        out.setdefault("directional_burden", float(cmpf.get("directional_burden", 0.0) or 0.0))
        out.setdefault("remaining_burden", float(conf.get("remaining_transformation_burden", 0.0) or 0.0))
        out.setdefault("frame_shift", float(regf.get("router_dyn", 0.0) or 0.0))
        out.setdefault("reeval_pressure", float(regf.get("reeval_pressure", 0.0) or 0.0))
    if auxiliary:
        for k, v in auxiliary.items():
            if k not in out or out[k] == 0.0:
                try:
                    out[k] = float(v)
                except Exception:
                    continue
    return out


def gauge_step(signals: Dict[str, float],
               state: Optional[Dict[str, Any]] = None,
               policy_name: str = DEFAULT_POLICY,
               eta: float = DEFAULT_ETA,
               lam: float = DEFAULT_LAM) -> Tuple[Dict[str, Any], float]:
    if state is None:
        state = {}
    A_state = state.get("A_state", {})
    if not isinstance(A_state, dict):
        A_state = {}
    new_A, alpha, transport_state = update_gauge(A_state, signals, policy_name=policy_name, eta=eta, lam=lam, state=state)
    new_state = dict(state)
    new_state.update(transport_state)
    new_state["A_state"] = new_A
    new_state["alpha"] = float(alpha)
    new_state["coherence"] = float(new_A.get("__coherence__", transport_coherence(signals, state=state)))
    return new_state, float(alpha)


def gauge_gain(signals: Dict[str, float],
               state: Optional[Dict[str, Any]] = None,
               policy_name: str = DEFAULT_POLICY,
               eta: float = DEFAULT_ETA,
               lam: float = DEFAULT_LAM) -> float:
    state, alpha = gauge_step(signals, state=state, policy_name=policy_name, eta=eta, lam=lam)
    coherence = float(state.get("coherence", 0.0))
    return _clamp01(0.65 * alpha + 0.35 * coherence)
