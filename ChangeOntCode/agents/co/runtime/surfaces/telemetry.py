"""Telemetry helpers for inspecting runtime surface outputs and structural traces.

Telemetry is diagnostic support only; it must not feed back as a hidden policy
selector in evidence-bearing CO runs.
"""
from __future__ import annotations
from typing import Any, Dict

def attach_basic_runtime_flags(out: Dict[str, Any]) -> Dict[str, Any]:
    out.setdefault("non_co_rescue_disabled", True)
    return out
