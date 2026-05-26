# agents/co/core/elements/_shared.py
from __future__ import annotations
from typing import Any
from agents.co.runtime.support.scope_keys import resolve_decision_scope

def publish_signal(bus: Any, key: str, value: float) -> None:
    """Best-effort scalar publish into signal_bus; tolerates dict/attr/method styles."""
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

def publish_candidate_votes(bus: Any, observation: dict, primitives: dict, header: Any, votes: dict[str, float], source: str, channel: str = "base") -> None:
    """Best-effort candidate publication to KernelSignalBus using canonical scope resolution."""
    if bus is None or not hasattr(bus, "publish"):
        return
    scope_key = resolve_decision_scope(observation, primitives, header)
    for a, w in votes.items():
        try:
            bus.publish(scope_key=scope_key, action=a, weight=float(w), channel=channel, source=source)
        except Exception:
            continue


def get_semantic(primitives: Any) -> dict:
    """Fetch semantic combinators registry from primitives."""
    try:
        sem = primitives.get("_semantic", {})
        if isinstance(sem, dict):
            return sem
    except Exception:
        pass
    return {}
