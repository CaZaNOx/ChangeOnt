# agents/co/core/primitives/P9_variable_birth.py
from typing import Dict, Tuple

def propose_new_variable(phi: Dict[str, float], residuals: Dict[str, float], mdl: float) -> Dict:
    """
    Very simple heuristic: if residual mass sits on a consistent pair count,
    propose a new prototype/feature named after that pair.
    """
    # pick largest residual feature, if any
    if not residuals:
        return {"proposal": None, "delta_mdl": 0.0}
    best_key = max(residuals.keys(), key=lambda k: residuals[k])
    gain = residuals[best_key]
    # crude MDL delta: assume adding 1 prototype costs +1 but gain ~ residual
    delta_mdl = 1.0 - gain
    return {"proposal": {"name": f"proto_{best_key}", "source": best_key, "estimated_gain": gain},
            "delta_mdl": float(delta_mdl)}

def accept_birth(delta_mdl: float, residual_gain: float, gamma: float, cooldown_state: Dict) -> bool:
    """
    Accept if MDL improves (delta_mdl < -gamma) and cooldown allows.
    """
    steps_left = int(cooldown_state.get("steps_left", 0))
    if steps_left > 0:
        cooldown_state["steps_left"] = steps_left - 1
        return False
    ok = (delta_mdl <= -float(gamma)) and (residual_gain > 0)
    if ok:
        cooldown_state["steps_left"] = int(cooldown_state.get("cooldown", 10))
    return ok
