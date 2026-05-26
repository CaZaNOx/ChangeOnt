from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

import yaml  # type: ignore

from agents.co.integration.core_builder import build_co_core


DEFAULT_CANONICAL_MANIFEST = Path("experiments/configs/co_agents/co_agents_canonical_core.yaml")
DEFAULT_CANONICAL_AGENT_NAME = "CO_canonical_core"


class InvalidCOEvaluation(RuntimeError):
    """Raised when a performance study tries to evaluate an inert or invalid CO core."""


def load_co_manifest_params(
    manifest_path: str | Path = DEFAULT_CANONICAL_MANIFEST,
    agent_name: str = DEFAULT_CANONICAL_AGENT_NAME,
) -> Dict[str, Any]:
    path = Path(manifest_path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    agents = list(raw.get("co_agents", []) or [])
    if not agents:
        raise InvalidCOEvaluation(f"no co_agents found in manifest: {path.as_posix()}")
    for agent in agents:
        if str(agent.get("name", "")) == str(agent_name):
            params = dict(agent.get("params", {}) or {})
            if not params:
                raise InvalidCOEvaluation(f"agent {agent_name!r} has empty params in manifest: {path.as_posix()}")
            return params
    names = [str(a.get("name", "")) for a in agents]
    raise InvalidCOEvaluation(
        f"agent {agent_name!r} not found in manifest {path.as_posix()}; available={names}"
    )


def build_validated_co_core(
    params: Dict[str, Any],
    *,
    study_name: str,
    manifest_path: str | Path | None = None,
    agent_name: str | None = None,
):
    core = build_co_core(params)
    element_names = [e.__class__.__name__ for e in getattr(core, "elements", [])]
    if not element_names:
        src = f" manifest={manifest_path} agent={agent_name}" if manifest_path or agent_name else ""
        raise InvalidCOEvaluation(
            f"{study_name}: CO core has no active elements.{src} This is an inert-shell evaluation and is invalid for performance studies."
        )
    if not any(name.lower().endswith("commitmentsurface") for name in element_names):
        raise InvalidCOEvaluation(
            f"{study_name}: CO core has active elements {element_names} but no CommitmentSurface; this path is not valid for end-to-end policy evaluation."
        )
    return core


def assert_valid_co_rollout(
    *,
    study_name: str,
    signal_bus_votes: Iterable[int],
    co_policies: Iterable[str],
) -> None:
    votes = [int(v) for v in signal_bus_votes]
    policies = [str(p) for p in co_policies]
    if votes and all(v == 0 for v in votes) and policies and all(p == "bandit:safe_default" for p in policies):
        raise InvalidCOEvaluation(
            f"{study_name}: CO rollout never produced votes and stayed on safe_default for the whole run; performance result is invalid."
        )


def load_validated_canonical_core(
    study_name: str,
    manifest_path: str | Path = DEFAULT_CANONICAL_MANIFEST,
    agent_name: str = DEFAULT_CANONICAL_AGENT_NAME,
) -> Tuple[Dict[str, Any], Any]:
    params = load_co_manifest_params(manifest_path=manifest_path, agent_name=agent_name)
    core = build_validated_co_core(
        params,
        study_name=study_name,
        manifest_path=manifest_path,
        agent_name=agent_name,
    )
    return params, core
