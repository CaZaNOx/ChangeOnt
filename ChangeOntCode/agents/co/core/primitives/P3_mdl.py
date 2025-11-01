# agents/co/core/primitives/P3_mdl.py
from typing import Dict, List, Tuple
import math

def mdl_code_len(model_state: Dict) -> float:
    """
    Very small MDL surrogate:
      L = c1 * (#prototypes) + c2 * (mean within-cluster distortion) + c3 * (#params)
    Provide defaults if missing.
    """
    m = int(model_state.get("n_prototypes", 0))
    dist = float(model_state.get("mean_distortion", 0.0))
    p = int(model_state.get("n_params", m))
    c1, c2, c3 = 1.0, 1.0, 0.25
    return c1*m + c2*dist + c3*p

def mdl_delta(prev: float, curr: float) -> float:
    """Negative deltas mean improvement."""
    return float(curr - prev)

def mdl_slope(history: List[float], window: int = 5) -> float:
    """
    Simple finite-difference slope over the last window.
    Negative slope suggests compression improving.
    """
    if not history:
        return 0.0
    vals = history[-window:]
    if len(vals) < 2:
        return 0.0
    diffs = [vals[i] - vals[i-1] for i in range(1, len(vals))]
    return sum(diffs) / len(diffs)
