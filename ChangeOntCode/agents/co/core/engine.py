# engine.py
from __future__ import annotations
from typing import Any, Dict, List
from .pipeline import COAgentCore

# Imports are intentionally local-safe; engine receives ready classes from registry.
def build_core(combo_cfg: Dict[str, Any],
               header_cls: Any,
               element_classes: Dict[str, Any],
               primitive_classes: Dict[str, Any],
               combinator_classes: Dict[str, Any]) -> COAgentCore:
    """
    Build a full CO core from a combo config + resolved classes.
    combo_cfg schema (minimal):
      {
        "name": "CO_full",
        "header": {"type": "SSI", "params": {...}},
        "math_policy": "co"|"classical",
        "elements": [{"key": "A", "class": "EA_HAQ", "params": {...}}, ...],
        "primitives": {"P10": {"class": "ChangeOpsCore", "params": {...}}, ...},
        "combinators": {"pipeline": {"class": "C_Pipeline", "params": {...}}, ...}
      }
    """
    # 1) Header
    h_params = combo_cfg.get("header", {}).get("params", {})
    header = header_cls(**h_params)

    # 2) Primitives
    prim_cfg: Dict[str, Dict[str, Any]] = combo_cfg.get("primitives", {})
    primitives: Dict[str, Any] = {}
    for key, spec in prim_cfg.items():
        cls = primitive_classes.get(spec.get("class"))
        if cls is None:
            continue
        params = spec.get("params", {})
        try:
            primitives[key] = cls(**params)
        except Exception:
            primitives[key] = cls()  # safe default

    # 3) Elements
    elems: List[Any] = []
    for e in combo_cfg.get("elements", []):
        cls = element_classes.get(e.get("class"))
        if cls is None:
            continue
        params = e.get("params", {})
        try:
            elems.append(cls(**params))
        except Exception:
            elems.append(cls())

    # 4) Combinators
    comb_cfg = combo_cfg.get("combinators", {})
    combinators: Dict[str, Any] = {}
    for name, spec in comb_cfg.items():
        cls = combinator_classes.get(spec.get("class"))
        if cls is None:
            continue
        params = spec.get("params", {})
        try:
            combinators[name] = cls(**params)
        except Exception:
            combinators[name] = cls()

    math_policy = combo_cfg.get("math_policy", "co")
    name = combo_cfg.get("name", "CO_core")
    return COAgentCore(header, elems, primitives, combinators, math_policy=math_policy, name=name)
