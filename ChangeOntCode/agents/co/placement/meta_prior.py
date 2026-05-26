from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

_PROFILE_KEYS = (
    "rigidity",
    "volatility",
    "reversibility",
    "commitment_cost",
    "observability",
    "deformation_bandwidth",
    "stability_horizon",
)

_GENERIC_PROFILE = {
    "rigidity": 0.50,
    "volatility": 0.50,
    "reversibility": 0.50,
    "commitment_cost": 0.50,
    "observability": 0.50,
    "deformation_bandwidth": 0.50,
    "stability_horizon": 0.50,
}


def _clamp01(x: Any, default: float = 0.5) -> float:
    try:
        v = float(x)
    except Exception:
        v = float(default)
    return max(0.0, min(1.0, v))


@dataclass
class MetaHeader:
    """
    Explicit structural prior surface.

    Canonical behavior:
    - carry only explicit inherited priors into the live runtime;
    - default to a generic regime-shape profile when nothing explicit is supplied;
    - never inject benchmark-family priors or family-specific control defaults.
    """

    priors: Dict[str, Any] = field(default_factory=dict)
    family: str | None = None

    def update(self, _observation: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    def _profile_with_source(self, observation: Dict[str, Any] | None = None) -> Tuple[Dict[str, float], str]:
        obs = dict(observation or {})
        out = dict(_GENERIC_PROFILE)
        source = "generic_default"

        explicit: Dict[str, Any] = {}
        if isinstance(self.priors.get("regime_shape"), dict):
            explicit.update(self.priors.get("regime_shape") or {})
        for k in _PROFILE_KEYS:
            if k in self.priors:
                explicit[k] = self.priors[k]
        if isinstance(obs.get("regime_shape"), dict):
            explicit.update(obs.get("regime_shape") or {})

        if explicit:
            source = "explicit_override"
        for k in _PROFILE_KEYS:
            if k in explicit:
                out[k] = _clamp01(explicit.get(k), out.get(k, 0.5))
        return out, source

    def regime_profile(self, observation: Dict[str, Any] | None = None) -> Dict[str, float]:
        profile, _source = self._profile_with_source(observation)
        return profile

    def to_dict(self, observation: Dict[str, Any] | None = None) -> Dict[str, Any]:
        out = dict(self.priors)
        fam = str((observation or {}).get("family", self.family or self.priors.get("family") or "generic"))
        profile, source = self._profile_with_source(observation)
        out["family"] = fam
        out["regime_shape"] = profile
        out["regime_shape_source"] = source
        return out
