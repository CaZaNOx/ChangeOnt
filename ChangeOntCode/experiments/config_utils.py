from __future__ import annotations

from typing import Any, Dict, Optional


def normalize_agent_config(agent: Any, default_algo: str) -> Dict[str, Any]:
    """
    Normalize agent config for runners.
    Accepts either canonical schema:
      agent: {type: "stoa"|"co", name: "<algo_or_variant>", params: {}}
    or legacy schema:
      agent: {type: "<algo>", name?: "<alias>", params?: {}}
      agent: "<algo>"
    Returns a legacy-friendly dict with `type` set to the algorithm name or "co".
    """
    if isinstance(agent, str):
        return {"type": agent.lower(), "params": {}}
    if not isinstance(agent, dict):
        return {"type": default_algo, "params": {}}

    agent_type = str(agent.get("type", "")).lower()
    agent_name = agent.get("name")
    agent_params = dict(agent.get("params", {}))

    if agent_type in ("stoa", "co"):
        if agent_type == "co":
            return {"type": "co", "name": agent_name, "params": agent_params}
        algo = str(agent_name or agent_params.get("algo") or default_algo).lower()
        return {"type": algo, "name": agent_name, "params": agent_params}

    # Legacy: treat type as algorithm
    return {"type": agent_type or default_algo, "name": agent_name, "params": agent_params}


def extract_env_params(env: Any) -> Dict[str, Any]:
    if not isinstance(env, dict):
        return {}
    params = env.get("params")
    if isinstance(params, dict):
        return params
    return env


def extract_env_spec(env: Any) -> Dict[str, Any]:
    if not isinstance(env, dict):
        return {}
    spec = env.get("spec")
    if isinstance(spec, dict):
        return spec
    return {}
