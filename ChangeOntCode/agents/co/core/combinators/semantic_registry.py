from __future__ import annotations
from typing import Dict, Any

from .SC_additive_blend import SC_AdditiveBlend
from .SC_multiplicative_coupling import SC_MultiplicativeCoupling
from .SC_gated_threshold import SC_GatedThreshold
from .SC_weighted_selection import SC_WeightedSelection
from .SC_order_sensitive_sequential import SC_OrderSensitiveSequential

SEMANTIC_SPECS: Dict[str, Dict[str, Any]] = {
    "SC_AdditiveBlend": {"role": "semantic", "kind": "blend", "status": "core"},
    "SC_MultiplicativeCoupling": {"role": "semantic", "kind": "coupling", "status": "core"},
    "SC_GatedThreshold": {"role": "semantic", "kind": "gate", "status": "core"},
    "SC_WeightedSelection": {"role": "semantic", "kind": "selection", "status": "optional"},
    "SC_OrderSensitiveSequential": {"role": "semantic", "kind": "sequence", "status": "optional"},
}


def build_semantic_registry() -> Dict[str, Any]:
    return {
        "SC_AdditiveBlend": SC_AdditiveBlend,
        "SC_MultiplicativeCoupling": SC_MultiplicativeCoupling,
        "SC_GatedThreshold": SC_GatedThreshold,
        "SC_WeightedSelection": SC_WeightedSelection,
        "SC_OrderSensitiveSequential": SC_OrderSensitiveSequential,
    }
