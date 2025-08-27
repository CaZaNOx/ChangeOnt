import math

def loop_score(c_leave: float, c_stay: float, eps: float = 1e-6) -> float:
    """
    s = (c_leave - c_stay) / (|c_leave| + |c_stay| + eps)
    Returns 0.0 if inputs are non-finite or denominator is degenerate.
    """
    if not (is_finite(c_leave) and is_finite(c_stay)):
        return 0.0
    denom = abs(c_leave) + abs(c_stay) + eps
    if denom <= 0.0 or not math.isfinite(denom):
        return 0.0
    return (c_leave - c_stay) / denom

def is_finite(x) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False