from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any

try:
    # Prefer project schedule if present
    from agents.co.core.rm import alpha_t as _alpha_t  # type: ignore
except Exception:  # pragma: no cover
    _alpha_t = None  # fallback below


@dataclass
class HAQState:
    """Minimal state for HAQ gauge updates."""
    t: int = 0
    weights: float = 0.0  # aggregate attention weight (0..1)
    leak: float = 1e-3    # leakage toward 0


def _default_alpha(t: int) -> float:
    # Conservative Robbins–Monro-ish fallback
    return (t + 50) ** -0.6


def alpha_for_step(t: int) -> float:
    if _alpha_t is not None:
        try:
            return float(_alpha_t(t))
        except Exception:
            pass
    return _default_alpha(t)


def clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def update_haq(
    state: HAQState,
    perceived_error: float,
    expected_utility: float,
    *,
    leak: Optional[float] = None,
    extras: Optional[Dict[str, Any]] = None,
) -> HAQState:
    """
    Cost-only gauge adaptation (does not touch topology).

    - Updates 'weights' as a contraction toward a target formed from (1 - PE) and EU.
    - Applies small leak toward 0 to avoid saturation.
    - NEVER changes edge sets or merges classes. That remains the job of headers/quotient.
    """
    state.t += 1
    a = alpha_for_step(state.t)
    lk = state.leak if leak is None else float(leak)

    pe = clamp01(perceived_error)
    eu = clamp01(expected_utility)

    # Simple, bounded target: higher when EU high and PE low.
    target = clamp01(0.5 * (1.0 - pe) + 0.5 * eu)

    # Robbins–Monro style update with leak
    w = state.weights * (1.0 - a) + a * target
    w = (1.0 - lk) * w

    state.weights = clamp01(w)
    if extras is not None:
        extras["alpha"] = a
        extras["target"] = target
        extras["leak_used"] = lk
    return state
