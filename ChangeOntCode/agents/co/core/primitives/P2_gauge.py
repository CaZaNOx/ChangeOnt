# agents/co/core/primitives/P2_gauge.py
from typing import Dict, Tuple

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
