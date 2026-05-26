from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

DEFAULT_PRIORS = {
    "maze": {"stability_prior": 0.8, "change_prior": 0.2, "classicality_prior": 0.85, "monitoring_floor": 0.05},
    "bandit": {"stability_prior": 0.7, "change_prior": 0.3, "classicality_prior": 0.75, "monitoring_floor": 0.08},
    "renewal": {"stability_prior": 0.55, "change_prior": 0.45, "classicality_prior": 0.60, "monitoring_floor": 0.10},
}


@dataclass
class MetaHeader:
    """
    External prior/control layer. Holds explicit task-family priors and assumptions.
    Must remain separate from internal header logic.
    """
    priors: Dict[str, Any] = field(default_factory=dict)
    family: str | None = None

    def update(self, _observation: Dict[str, Any]) -> Dict[str, Any]:
        # Meta-header does not update from internal dynamics in v1.
        return {}

    def to_dict(self) -> Dict[str, Any]:
        base = dict(DEFAULT_PRIORS.get(str(self.family or "").lower(), {}))
        base.update(dict(self.priors))
        if self.family is not None:
            base["family"] = self.family
        return base
