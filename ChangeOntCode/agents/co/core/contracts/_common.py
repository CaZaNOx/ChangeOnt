from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Mapping, Optional

ALLOWED_SCOPES = {
    "anchor",
    "hypothesis_over_anchor",
    "emergent_profile",
    "mixed",
    "unspecified",
}
HORIZON_FIXITY = {"fixed", "slow", "active", "mixed", "unknown"}
DRIFT_PROFILE = {"none", "fixed", "slow", "active", "mixed", "unknown"}
OBSERVABILITY = {"direct", "partial", "indirect", "mixed", "unknown"}
REVERSIBILITY = {"reversible", "partly_reversible", "irreversible", "unknown"}
COMMITMENT_COST = {"low", "low_to_medium", "medium", "medium_to_high", "high", "unknown"}


def bounded01(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        fv = float(value)
    except Exception:
        return None
    if fv < 0.0:
        return 0.0
    if fv > 1.0:
        return 1.0
    return fv


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def clean_list(value: Any) -> List[str]:
    if not isinstance(value, (list, tuple)):
        return []
    out: List[str] = []
    for item in value:
        text = clean_text(item)
        if text:
            out.append(text)
    return out


def copy_mapping(raw: Any) -> Dict[str, Any]:
    if isinstance(raw, Mapping):
        return dict(raw)
    return {}


def choice(value: Any, allowed: set[str], default: str) -> str:
    text = clean_text(value).lower() or default
    return text if text in allowed else default


def deep_export_bundle(contract: Any, keys: List[str]) -> Dict[str, Any]:
    if not isinstance(contract, Mapping):
        return {}
    return deepcopy({k: copy_mapping(contract.get(k)) for k in keys})
