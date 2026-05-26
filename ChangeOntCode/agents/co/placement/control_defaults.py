"""Default control values for six-question placement projection.

Defaults are neutral public-regime placeholders and must not encode family
policies or benchmark tuning.
"""
from __future__ import annotations

from typing import Any, Dict


def apply_runtime_control_defaults(overrides: Dict[str, Any] | None = None, **kwargs: Any) -> Dict[str, Any]:
    """Generic control defaults for the live header path.

    These defaults are family-blind. Similar problems should differ through
    shared placement/regime estimates, not through family-local control tables.
    """
    out: Dict[str, Any] = dict(overrides or {})
    out.update(kwargs)
    out.setdefault("tau_range", (0.0, 1.5))
    out.setdefault("eps_range", (0.0, 0.25))
    out.setdefault("alpha_cap_range", (0.0, 0.9))
    out.setdefault("gamma_range", (0.01, 0.10))
    out.setdefault("cooldown_range", (5, 30))
    out.setdefault("dyn_prior", 0.0)
    out.setdefault("thinness_prior", 1.0)
    out.setdefault("co_base", 0.25)
    out.setdefault("anneal_beta", 0.005)
    out.setdefault("dyn_alpha", 0.25)
    out.setdefault("pressure_alpha", 0.20)
    return out
