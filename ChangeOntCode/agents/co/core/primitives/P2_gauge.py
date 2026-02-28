# agents/co/core/primitives/P2_gauge.py
from __future__ import annotations
from typing import Dict, Tuple, Any, Optional

# P2_Gauge: minimal modulation primitive. Formula remains provisional by doctrine.
DEFAULT_POLICY = "R_gated"
DEFAULT_ETA = 0.1
DEFAULT_LAM = 0.02

def warp_costs(base_costs: Dict, A_state: Dict, alpha: float) -> Dict:
    """
    Apply attention/gauge to edge/node costs.
    base_costs: mapping key->cost
    A_state: mapping key->attention weight in [-1, +1] (positive raises salience)
    alpha: cap in [0,1] controlling warp magnitude.
    """
    out = {}
    for k, c in base_costs.items():
        a = A_state.get(k, 0.0)
        # perceived cost: c + alpha * a  (cap at >= 0)
        cc = max(0.0, float(c) + float(alpha) * float(a))
        out[k] = cc
    return out

def update_gauge(A_state: Dict, signals: Dict, policy_name: str = "R_gated",
                 eta: float = 0.1, lam: float = 0.02) -> Tuple[Dict, float]:
    """
    Update attention map and produce a scalar alpha (strength).
    signals: should include z_PE (surprise), z_gain (expected gain), var_resid (stability).
    """
    z_pe = float(signals.get("z_PE", 0.0))
    z_gain = float(signals.get("z_gain", 0.0))
    var_resid = max(1e-6, float(signals.get("var_resid", 1.0)))

    if policy_name == "R_ratio":
        alpha = max(0.0, min(1.0, (z_pe / (1.0 + var_resid))))
    else:  # R_gated default
        gate = 1.0 if (z_gain > 0 and z_pe > 0) else 0.0
        alpha = max(0.0, min(1.0, gate * (eta * z_pe)))

    # Simple decay on A_state
    new_A = {k: (1.0 - lam) * v for k, v in A_state.items()}
    # Optionally highlight global salience (you can specialize per edge outside)
    new_A["__global__"] = new_A.get("__global__", 0.0) + z_pe * 0.1
    return new_A, alpha


def extract_signals(observation: Dict[str, Any], fallback: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Extract minimal gauge signals from observation (or fallback).
    Expected keys: z_PE, z_gain, var_resid.
    """
    out: Dict[str, float] = {}
    sig = observation.get("signals", {}) if isinstance(observation, dict) else {}
    if isinstance(sig, dict):
        out["z_PE"] = float(sig.get("z_PE", 0.0))
        out["z_gain"] = float(sig.get("z_gain", 0.0))
        out["var_resid"] = float(sig.get("var_resid", 1.0))
    if fallback:
        for k, v in fallback.items():
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
    """
    Update gauge state and return a scalar modulation alpha in [0,1].
    """
    if state is None:
        state = {}
    A_state = state.get("A_state", {})
    if not isinstance(A_state, dict):
        A_state = {}
    new_A, alpha = update_gauge(A_state, signals, policy_name=policy_name, eta=eta, lam=lam)
    state["A_state"] = new_A
    state["alpha"] = float(alpha)
    return state, float(alpha)


def gauge_gain(signals: Dict[str, float],
               state: Optional[Dict[str, Any]] = None,
               policy_name: str = DEFAULT_POLICY,
               eta: float = DEFAULT_ETA,
               lam: float = DEFAULT_LAM,
               min_gain: float = 0.0,
               max_gain: float = 2.0) -> Tuple[Dict[str, Any], float]:
    """
    Return a multiplicative gain derived from gauge alpha.
    gain = 1 + alpha (clamped to [min_gain, max_gain]).
    """
    state, alpha = gauge_step(signals, state=state, policy_name=policy_name, eta=eta, lam=lam)
    gain = 1.0 + float(alpha)
    if min_gain is not None:
        gain = max(float(min_gain), gain)
    if max_gain is not None:
        gain = min(float(max_gain), gain)
    return state, float(gain)
