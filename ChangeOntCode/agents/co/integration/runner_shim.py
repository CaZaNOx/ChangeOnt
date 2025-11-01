# agents/co/integration/runner_shim.py
from __future__ import annotations
from typing import Any, Dict, Optional, Tuple

def step_agent(agent: Any, observation: Optional[Dict[str, Any]], default_action: Any) -> Tuple[Any, Dict[str, Any]]:
    """
    Normalizes agent step across STOA & CO adapters.
    - If agent has .select(obs) returning dict with 'action', use it and return (action, metrics_dict).
    - Else if agent has .act(obs) or .select(obs) returning action, treat it as raw action; metrics empty.
    """
    # CO adapter path
    if hasattr(agent, "select"):
        out = agent.select(observation)
        if isinstance(out, dict) and "action" in out:
            action = out.get("action", default_action)
            metrics = {k: v for k, v in out.items() if k != "action"}
            return action, metrics
        # stoa-like 'select' returning raw action
        return out, {}

    # alternate STOA interface
    for method in ("act", "__call__"):
        if hasattr(agent, method):
            try:
                action = getattr(agent, method)(observation)
                return action, {}
            except Exception:
                break
    return default_action, {}
