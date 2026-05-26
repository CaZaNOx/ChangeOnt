"""Build and validate public problem packets for the canonical CO runtime.

This module is the adapter boundary guard: it constructs the public packet,
attaches contract diagnostics, and rejects missing or invalid kernel actions
instead of allowing adapter-side fallback.
"""
from __future__ import annotations
from typing import Any, Dict, List, Mapping, MutableMapping, Optional
from agents.co.core.contracts.problem_contract import normalize_problem_contract
from agents.co.boundary.packet_schema import REQUIRED_PACKET_KEYS

def make_problem_packet(*, family:str, step_idx:int, action_space:List[Any], current_observation:Mapping[str,Any], history:Optional[List[Any]]=None, trace:Optional[List[Any]]=None, feedback:Optional[Mapping[str,Any]]=None, residuals:Optional[Mapping[str,Any]]=None, probes:Optional[Mapping[str,Any]]=None, signals:Optional[Mapping[str,Any]]=None, constraints:Optional[Mapping[str,Any]]=None, family_payload:Optional[Mapping[str,Any]]=None, goal_field:Optional[Mapping[str,Any]]=None, problem_contract:Optional[Mapping[str,Any]]=None, memory_view:Optional[Mapping[str,Any]]=None, measurement_evidence:Optional[Mapping[str,Any]]=None, candidates:Optional[List[Any]]=None, field_update:Optional[Mapping[str,Any]]=None, dyn_hint:Optional[float]=None, co_conf_hint:Optional[float]=None, support_evidence:Optional[float]=None) -> Dict[str,Any]:
    packet={"family":str(family),"step_idx":int(step_idx),"action_space":list(action_space),"current_observation":dict(current_observation or {}),"history":list(history or []),"trace":list(trace or []),"feedback":dict(feedback or {}),"residuals":dict(residuals or {}),"probes":dict(probes or {}),"signals":dict(signals or {}),"constraints":dict(constraints or {}),"family_payload":dict(family_payload or {}),"goal_field":dict(goal_field or {}),"problem_contract":normalize_problem_contract(problem_contract or {}),"memory_view":dict(memory_view or {}),"measurement_evidence":dict(measurement_evidence or {}),"candidates":list(candidates or action_space),"field_update":dict(field_update or {})}
    if dyn_hint is not None:
        try: packet["dyn_hint"]=float(dyn_hint)
        except Exception: pass
    if co_conf_hint is not None:
        try: packet["co_conf_hint"]=float(co_conf_hint)
        except Exception: pass
    if support_evidence is not None:
        try: packet["support_evidence"]=float(support_evidence)
        except Exception: pass
    packet["t"]=int(step_idx)
    cur=packet["current_observation"]; fam=packet["family_payload"]
    packet["obs"]=cur.get("obs", cur.get("value", cur))
    for k in ("n_arms","A","L_win","action_space","pos","goal","height","width","grid"):
        if k not in packet:
            if k in cur: packet[k]=cur.get(k)
            elif k in fam: packet[k]=fam.get(k)
    return packet

def validate_problem_packet(packet:Mapping[str,Any])->List[str]:
    missing=[k for k in REQUIRED_PACKET_KEYS if k not in packet]; problems=[]
    if missing: problems.append("missing_keys="+','.join(missing))
    if not isinstance(packet.get('action_space',[]), list): problems.append('action_space_not_list')
    if not isinstance(packet.get('candidates',[]), list): problems.append('candidates_not_list')
    for k in ('history','trace'):
        if not isinstance(packet.get(k,[]), list): problems.append(f'{k}_not_list')
    for k in ('feedback','residuals','probes','signals','constraints','family_payload','goal_field','problem_contract','memory_view','measurement_evidence'):
        if not isinstance(packet.get(k,{}), dict): problems.append(f'{k}_not_dict')
    if 'field_update' in packet and not isinstance(packet.get('field_update',{}), dict): problems.append('field_update_not_dict')
    return problems

def validate_problem_update(update:Mapping[str,Any])->List[str]:
    if not isinstance(update, Mapping): return ['field_update_not_mapping']
    problems=[]
    if update and 'realized_candidate' not in update: problems.append('missing_realized_candidate')
    if 'unrealized_candidates' in update and not isinstance(update.get('unrealized_candidates'), list): problems.append('unrealized_candidates_not_list')
    return problems

def attach_contract_debug(out:MutableMapping[str,Any], packet:Mapping[str,Any], warnings:List[str])->None:
    out.setdefault('problem_packet_keys', sorted(list(packet.keys())))
    out.setdefault('problem_packet_warnings', list(warnings))
    out.setdefault('problem_packet_ok', len(warnings)==0)

def _action_in_domain(action: Any, legal_actions: Optional[List[Any]]) -> bool:
    if legal_actions is None:
        return True
    return any(action == candidate for candidate in list(legal_actions))

def require_kernel_action(
    out: Optional[Mapping[str, Any]],
    *,
    legal_actions: Optional[List[Any]] = None,
    family: str = "adapter",
) -> Dict[str, Any]:
    """Require a kernel-produced native action and reject adapter-side rescue.

    This is the boundary-side guard for the no-classical-fallback rule.  The
    adapter may project a kernel action back to the environment only when the
    kernel actually emitted an action and, when a native action domain is
    supplied, that action is in the public native domain.  Invalid or missing
    actions are errors; the adapter must not coerce them into first-legal,
    default, random, or family-specific replacement actions.
    """
    resp = dict(out or {})
    if "action" not in resp:
        raise RuntimeError(
            "Kernel returned no action; canonical CO path forbids adapter-side fallback."
        )
    action = resp.get("action")
    if not _action_in_domain(action, legal_actions):
        raise RuntimeError(
            f"Kernel returned invalid {family} action {action!r}; canonical CO path "
            "forbids adapter-side fallback or coercion."
        )
    return resp
