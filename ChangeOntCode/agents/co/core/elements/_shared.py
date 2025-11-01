# agents/co/core/elements/_shared.py
from __future__ import annotations
from typing import Any

def publish_signal(bus: Any, key: str, value: float) -> None:
    """Best-effort scalar publish into co_bus; tolerates dict/attr/method styles."""
    if bus is None:
        return
    try:
        bus[key] = float(value)
        return
    except Exception:
        pass
    try:
        setattr(bus, key.replace(".", "_"), float(value))
        return
    except Exception:
        pass
    try:
        if hasattr(bus, "set"):
            bus.set(key, float(value))
    except Exception:
        pass

def push_votes(bus: Any, family: str, votes: dict[str, float], source: str) -> None:
    """Best-effort vote publish to co_bus if it supports .push(family, action,...)."""
    if bus is None:
        return
    if not hasattr(bus, "push"):
        return
    for a, w in votes.items():
        try:
            bus.push(family, a, weight=float(w), source=source)
        except Exception:
            continue