# agents/co/registries/factories.py
from __future__ import annotations
from importlib import import_module
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import yaml
from pathlib import Path

@dataclass
class HeaderBundle:
    name: str
    header_state: Any
    math_context: Any
    guards: Dict[str, bool]

def _dynload(spec: str):
    """
    spec = "pkg.mod:ClassName"
    """
    mod, cls = spec.split(":")
    m = import_module(mod)
    return getattr(m, cls)

def load_registry(registry_path: str | Path) -> Dict:
    with open(registry_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_header(reg: Dict, name: str, family: str, overrides: Dict | None = None) -> HeaderBundle:
    spec = reg["headers"][name]
    HeaderClass = _dynload(spec)
    hdr = HeaderClass(family=family, overrides=overrides or {})
    hdr.apply_static()
    hdr.derive_effective()
    return HeaderBundle(
        name=name,
        header_state=hdr.state,
        math_context=hdr.math,
        guards=hdr.guards(),
    )

def build_elements(reg: Dict, elems_cfg: List[Dict]) -> List[Any]:
    built = []
    for e in elems_cfg:
        if not e.get("enabled", True): 
            continue
        name = e["name"]
        params = e.get("params", {})
        spec = reg["elements"][name]
        Cls = _dynload(spec)
        inst = Cls().configure(params, context={})
        built.append(inst)
    return built

def get_adapter_class(reg: Dict, env_adapter_name: str):
    spec = reg["adapters"][env_adapter_name]
    return _dynload(spec)
