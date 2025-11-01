# agents/co/integration/suite_hooks.py
from __future__ import annotations
from typing import Any, Dict, List, Tuple
from pathlib import Path
from .loader import load_registry, load_combos, resolve_classes

DEFAULT_REG_PATH = Path("agents/co/registries/registry.yaml")
DEFAULT_COMBOS_GLOB = Path("agents/co/combos/*.yaml")

def enumerate_co_agents_for_family(
    family: str,
    registry_path: str | Path = DEFAULT_REG_PATH,
    combos_glob: str | Path = DEFAULT_COMBOS_GLOB
) -> List[Tuple[str, Any]]:
    """
    Build (combo_name, adapter_instance) for a given family.
    The adapter exposes .select(observation) -> { action, ... }.
    """
    reg = load_registry(registry_path)
    classes = resolve_classes(reg)
    builder = classes["engine"]["builder"]

    # pick adapter by family
    adapter_cls = classes["adapters"].get(family)
    if adapter_cls is None:
        # family not supported
        return []

    header_classes   = classes["headers"]
    element_classes  = classes["elements"]
    primitive_classes= classes["primitives"]
    combinator_classes = classes["combinators"]

    agents: List[Tuple[str, Any]] = []
    for combo_name, combo_cfg in load_combos(combos_glob):
        # Resolve header class type
        header_type = combo_cfg.get("header", {}).get("type", "SSI")
        header_cls  = header_classes.get(header_type)
        if header_cls is None:
            # skip unknown header
            continue
        core = builder(
            combo_cfg=combo_cfg,
            header_cls=header_cls,
            element_classes=element_classes,
            primitive_classes=primitive_classes,
            combinator_classes=combinator_classes
        )
        adapter = adapter_cls(core=core, name=combo_name)
        agents.append((combo_name, adapter))
    return agents
