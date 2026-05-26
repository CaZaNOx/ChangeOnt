"""Problem-packet schema checks for the adapter-to-kernel boundary.

The schema records public action/candidate/history fields required by the
current kernel path without adding policy advice or hidden solver information.
"""
from __future__ import annotations
from typing import Any, Dict, List, Mapping, MutableMapping

REQUIRED_PACKET_KEYS = (
    "family", "step_idx", "action_space", "current_observation", "history", "trace",
    "feedback", "residuals", "probes", "signals", "constraints", "family_payload",
    "candidates", "goal_field", "problem_contract",
)

def validate_problem_packet(packet: Mapping[str, Any]) -> List[str]:
    missing = [k for k in REQUIRED_PACKET_KEYS if k not in packet]
    problems: List[str] = []
    if missing:
        problems.append("missing_keys=" + ",".join(missing))
    if not isinstance(packet.get("action_space", []), list):
        problems.append("action_space_not_list")
    if not isinstance(packet.get("candidates", []), list):
        problems.append("candidates_not_list")
    for k in ("history", "trace"):
        if not isinstance(packet.get(k, []), list):
            problems.append(f"{k}_not_list")
    for k in ("feedback", "residuals", "probes", "signals", "constraints", "family_payload", "goal_field", "problem_contract"):
        if not isinstance(packet.get(k, {}), dict):
            problems.append(f"{k}_not_dict")
    if "field_update" in packet and not isinstance(packet.get("field_update", {}), dict):
        problems.append("field_update_not_dict")
    return problems

def validate_problem_update(update: Mapping[str, Any]) -> List[str]:
    problems: List[str] = []
    if not isinstance(update, Mapping):
        return ["field_update_not_mapping"]
    if update and "realized_candidate" not in update:
        problems.append("missing_realized_candidate")
    if "unrealized_candidates" in update and not isinstance(update.get("unrealized_candidates"), list):
        problems.append("unrealized_candidates_not_list")
    return problems

def attach_contract_debug(out: MutableMapping[str, Any], packet: Mapping[str, Any], warnings: List[str]) -> None:
    out.setdefault("family_packet_keys", sorted(list(packet.keys())))
    out.setdefault("family_packet_warnings", list(warnings))
    out.setdefault("family_packet_ok", len(warnings) == 0)
