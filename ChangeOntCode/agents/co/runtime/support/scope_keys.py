from __future__ import annotations
from typing import Any, Dict


def _runtime_contract(prims: Dict[str, Any], header: Any) -> Dict[str, Any]:
    core = getattr(header, 'core', None)
    if core is not None and hasattr(core, 'export_runtime_contract'):
        try:
            data = core.export_runtime_contract()
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    if isinstance(prims, dict):
        data = prims.get('_runtime_contract')
        if isinstance(data, dict):
            return data
    return {}


def resolve_decision_scope(observation: Dict[str, Any], primitives: Dict[str, Any], header: Any) -> str:
    for key in ('_decision_scope', 'decision_scope', 'episode_scope', 'problem_scope'):
        val = str(observation.get(key, '') or '').strip().lower()
        if val:
            return val
    contract = _runtime_contract(primitives, header)
    if isinstance(contract, dict):
        problem = contract.get('problem_contract', {})
        if isinstance(problem, dict):
            scope = str(problem.get('decision_scope', '') or '').strip().lower()
            if scope:
                return scope
    return 'default'
