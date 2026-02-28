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
        "primitives": {"p10": {"class": "ChangeOpsCore", "params": {...}}, ...},
        "combinators": {"pipeline": {"class": "C_Pipeline", "params": {...}}, ...}
      }
    """
    # 1) Header
    h_params = combo_cfg.get("header", {}).get("params", {})
    header = header_cls(**h_params)

    # 2) Primitives
    prim_cfg: Dict[str, Dict[str, Any]] = combo_cfg.get("primitives", {})
    primitives: Dict[str, Any] = {}
    def _init_primitive(cls: Any, params: Dict[str, Any]) -> Any:
        if cls is None:
            return None
        if callable(cls):
            try:
                return cls(**params)
            except Exception:
                try:
                    return cls()
                except Exception:
                    return cls
        return cls

    for key, spec in prim_cfg.items():
        cls = primitive_classes.get(spec.get("class"))
        if cls is None:
            continue
        params = spec.get("params", {})
        primitives[key] = _init_primitive(cls, params)

    # ensure canonical primitives exist when classes are available
    if "co_bus" not in primitives and "co_bus" in primitive_classes:
        primitives["co_bus"] = _init_primitive(primitive_classes.get("co_bus"), {})
    if "P1" not in primitives and "P1" in primitive_classes:
        primitives["P1"] = _init_primitive(primitive_classes.get("P1"), {})
    if "P2" not in primitives and "P2" in primitive_classes:
        primitives["P2"] = _init_primitive(primitive_classes.get("P2"), {})
    if "P3" not in primitives and "P3" in primitive_classes:
        primitives["P3"] = _init_primitive(primitive_classes.get("P3"), {})
    if "p10" not in primitives and "p10" in primitive_classes:
        primitives["p10"] = _init_primitive(primitive_classes.get("p10"), {})
    if "p12" not in primitives and "p12" in primitive_classes:
        primitives["p12"] = _init_primitive(primitive_classes.get("p12"), {})
    if "id_mem" not in primitives and "id_mem" in primitive_classes:
        primitives["id_mem"] = _init_primitive(primitive_classes.get("id_mem"), {})
    if "birth_count" not in primitives:
        primitives["birth_count"] = 0

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
