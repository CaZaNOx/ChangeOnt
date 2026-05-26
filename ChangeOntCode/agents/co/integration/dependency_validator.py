"""Validate declared component dependencies for the assembled CO runtime.

These checks keep primitive/element/surface requirements explicit so missing
carriers do not become silent runtime drift.
"""
from __future__ import annotations
from typing import Any, Dict

def validate_runtime_contract(primitives: Dict[str, Any]) -> Dict[str, Any]:
    return {"has_runtime_contract": isinstance(primitives.get("_runtime_contract"), dict)}
