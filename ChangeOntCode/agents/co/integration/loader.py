# agents/co/integration/loader.py
from __future__ import annotations
import importlib
import yaml
from pathlib import Path
from typing import Any, Dict, List, Tuple

def _resolve(symbol: str):
    """
    'pkg.mod:Name' -> object
    """
    mod, name = symbol.split(":")
    return getattr(importlib.import_module(mod), name)

def load_registry(registry_path: str | Path) -> Dict[str, Dict[str, str]]:
    with open(registry_path, "r", encoding="utf-8") as f:
        reg = yaml.safe_load(f)
    assert isinstance(reg, dict), "registry.yaml must map sections -> symbols"
    return reg

def load_combos(glob_pattern: str | Path) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Returns list of (combo_name, combo_cfg)
    """
    combos = []
    for p in sorted(Path(glob_pattern).parent.glob(Path(glob_pattern).name)):
        with open(p, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        name = cfg.get("name", p.stem)
        combos.append((name, cfg))
    return combos

def resolve_classes(reg: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    """
    Import all classes/functions referenced in registry.yaml.
    Returns dict buckets keyed by registry sections.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for section, mapping in reg.items():
        if not isinstance(mapping, dict): 
            continue
        resolved = {}
        for k, sym in mapping.items():
            try:
                resolved[k] = _resolve(sym)
            except Exception as e:
                raise RuntimeError(f"Failed to resolve [{section}.{k}] -> {sym}: {e}") from e
        out[section] = resolved
    return out
