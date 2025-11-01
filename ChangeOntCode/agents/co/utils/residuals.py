# agents/co/utils/residuals.py
from typing import Dict, Sequence

def residuals_from_prediction(y_true: Sequence[float], y_pred: Sequence[float]) -> Dict[str, float]:
    """
    Build a simple residual map for GHVC:
      - 'mse' global
      - top-k absolute residual bins as named features
    """
    n = min(len(y_true), len(y_pred))
    if n == 0: return {}
    abs_err = [abs(y_true[i] - y_pred[i]) for i in range(n)]
    mse = sum(e*e for e in abs_err) / n
    order = sorted(range(n), key=lambda i: abs_err[i], reverse=True)[:5]
    out = {f"abs_resid_{i}": abs_err[i] for i in order}
    out["mse"] = mse
    return out
