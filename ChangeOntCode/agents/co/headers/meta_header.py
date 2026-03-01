from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict


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
        out = dict(self.priors)
        if self.family is not None:
            out["family"] = self.family
        return out
