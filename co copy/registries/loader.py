# agents/co/registries/loader.py
from __future__ import annotations
import importlib
from pathlib import Path
import yaml

def _import_callable(path: str):
    module, attr = path.rsplit(".", 1)
    return getattr(importlib.import_module(module), attr)

def load_registry(registry_path: str | Path) -> dict:
    return yaml.safe_load(Path(registry_path).read_text(encoding="utf-8")) or {}

def make_element(reg: dict, key: str, params: dict | None = None):
    """Construct a callable element by name from registry['elements'][key]."""
    path = reg["elements"][key]
    factory = _import_callable(path)
    return factory(params or {})
