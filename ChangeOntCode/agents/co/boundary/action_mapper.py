"""Project a certified kernel commitment packet back to the native action field.

This boundary helper is intentionally thin: it does not choose or repair an
action, it only reads the action already emitted by CommitmentSurface.
"""
from __future__ import annotations
from typing import Any, Dict

def project_native_action(decision: Dict[str, Any], _observation: Dict[str, Any]) -> Any:
    return decision.get("action")
