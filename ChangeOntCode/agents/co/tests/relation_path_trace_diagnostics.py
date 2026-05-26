"""Diagnostics for relation-path trace quality and forbidden leakage terms."""
from __future__ import annotations

"""Relation-path trace diagnostics.

These tests are not reward/performance claims.  They verify the newly intended
runtime path:

    adapter public_effects -> kernel RelationSurface -> RCF field outputs

by comparing identical adapter observations with public_effects present vs
stripped.  If relation topology is doing real work, the relation-on trace should
show RCF field deltas even when candidate scalar evidence is otherwise held
fixed by the same adapter observation.
"""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface


FIELD_KEYS = (
    "field_debt",
    "field_viability",
    "field_grey_pressure",
    "field_recursion_budget",
    "field_collapse_readiness",
    "quotient_share_count",
    "collapse_certificate_score",
    "collapse_certificate_blocker_pressure",
    "collapse_certificate_recursion_demand",
    "unresolved_rival_count",
    "quotient_resolved_rival_count",
)

FORBIDDEN_TERMS = (
    "optimal",
    "best_action",
    "dp_value",
    "oracle",
    "hidden_policy",
    "shortest_path",
    "q_value",
)


class DummyCore:
    def __init__(self) -> None:
        self.primitives: Dict[str, Any] = {}
        self.combinators: Dict[str, Any] = {}


class TraceBus:
    def __init__(self) -> None:
        self._votes: List[Dict[str, Any]] = []

    def publish(self, *, scope_key: str, action: Any, weight: float, channel: str | None = None, source: str | None = None) -> None:
        self._votes.append({
            "scope_key": scope_key,
            "action": action,
            "weight": float(weight),
            "scope": channel,
            "source": source,
        })

    def size(self, scope_key: str | None = None) -> int:
        if scope_key is None:
            return len(self._votes)
        return sum(1 for v in self._votes if v.get("scope_key") == scope_key)

    def drain(self, scope_key: str | None = None) -> List[Dict[str, Any]]:
        if scope_key is None:
            out = list(self._votes)
            self._votes.clear()
            return out
        out = [v for v in self._votes if v.get("scope_key") == scope_key]
        self._votes = [v for v in self._votes if v.get("scope_key") != scope_key]
        return out

    def signals(self) -> Dict[str, float]:
        return {}


@dataclass
class TraceHeaderState:
    co_weight: float = 1.0
    evidence_gate: float = 0.60
    fracture_tolerance: float = 0.45
    retention_depth: float = 0.60
    collapse_permission: float = 0.45
    identity_support_threshold: float = 0.50
    support_evidence: float = 0.40
    collapse_admissibility: float = 0.45
    revision_permissibility: float = 0.65
    support_carry_forward: float = 0.55
    rival_breadth: float = 0.65
    nonlocal_authority: float = 0.75
    path_sensitivity: float = 0.75
    local_authority: float = 0.35


@dataclass
class TraceHeader:
    state: TraceHeaderState


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _strip_public_effects(candidates: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for cand in candidates:
        row = dict(cand)
        row.pop("public_effects", None)
        row.pop("burden_effects", None)
        row.pop("effect_facts", None)
        out.append(row)
    return out


def _obs_from_candidates(candidates: List[Dict[str, Any]], family: str) -> Dict[str, Any]:
    actions = [c.get("candidate_id") for c in candidates if c.get("candidate_id") is not None and bool(c.get("legal", True))]
    return {
        "family": family,
        "t": 5,
        "action_space": actions,
        "problem_contract": {
            "task_anchor": {"kind": "relation_trace_diagnostic", "provided_externally": True},
            "actions": {"count": len(actions), "native_type": "adapter_candidates"},
            "observability_profile": {"state": "public_trace", "constraints": "public_trace"},
        },
        "candidates": candidates,
    }


def _run_candidate_commitment(candidates: List[Dict[str, Any]], family: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    obs = _obs_from_candidates(candidates, family)
    bus = TraceBus()
    prims: Dict[str, Any] = {"signal_bus": bus}
    header = TraceHeader(TraceHeaderState())
    CandidateEvidenceSurface().step(obs, prims, header, None)
    rows = [dict(r) for r in prims.get("__candidate_publication_rows__", [])]
    out = CommitmentSurface(collapse_enabled=False).step(obs, prims, header, None)
    return rows, dict(out or {})


def _relation_telemetry(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {}
    tel = rows[0].get("relation_surface_telemetry", {})
    return dict(tel) if isinstance(tel, dict) else {}


def _rows_by_action(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(r.get("action")): r for r in rows if r.get("action") is not None}


COUNT_FIELD_KEYS = {"quotient_share_count", "unresolved_rival_count", "quotient_resolved_rival_count"}


def _field_delta(on_rows: List[Dict[str, Any]], off_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    on = _rows_by_action(on_rows)
    off = _rows_by_action(off_rows)
    total = 0.0
    max_delta = 0.0
    scalar_total = 0.0
    scalar_max = 0.0
    topology_total = 0.0
    topology_max = 0.0
    by_action: Dict[str, Dict[str, float]] = {}
    for action, on_row in on.items():
        if action not in off:
            continue
        off_row = off[action]
        by_action[action] = {}
        for key in FIELD_KEYS:
            try:
                delta = abs(float(on_row.get(key, 0.0)) - float(off_row.get(key, 0.0)))
            except Exception:
                delta = 0.0 if on_row.get(key) == off_row.get(key) else 1.0
            by_action[action][key] = float(delta)
            total += delta
            max_delta = max(max_delta, delta)
            if key in COUNT_FIELD_KEYS:
                topology_total += delta
                topology_max = max(topology_max, delta)
            else:
                scalar_total += delta
                scalar_max = max(scalar_max, delta)
    return {
        "field_delta_l1": float(total),
        "field_delta_max": float(max_delta),
        "scalar_field_delta_l1": float(scalar_total),
        "scalar_field_delta_max": float(scalar_max),
        "topology_count_delta_l1": float(topology_total),
        "topology_count_delta_max": float(topology_max),
        "by_action": by_action,
    }


def _case_candidates() -> Dict[str, List[Dict[str, Any]]]:
    core = DummyCore()
    bandit = COAdapterBandit(core, n_arms=3)._derive_from_visible_history({"n_arms": 3, "t": 0}, 0)["candidates"]
    maint = COAdapterMaintenanceReplacement(DummyCore())._derive({
        "observed_health": 2,
        "max_health": 4,
        "health_observed": True,
        "degradation_prob_public": 0.20,
        "wait_recovery_prob_public": 0.00,
        "repair_cost_public": 0.80,
        "replace_cost_public": 2.0,
        "failure_penalty_public": 8.0,
        "observe_health_mode": "partial",
    })["candidates"]
    maze = COAdapterMaze(DummyCore())._derive({
        "pos": (1, 1),
        "goal": (1, 3),
        "grid": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "height": 3,
        "width": 4,
    })["candidates"]
    latent = COAdapterLatentMechanism(DummyCore())._derive({
        "pos": (0, 0),
        "goal": (2, 2),
        "door": (1, 1),
        "switches": [(0, 1)],
        "decoys": [(1, 0)],
        "legal_actions": ["UP", "DOWN", "LEFT", "RIGHT", "INTERACT"],
        "door_open": False,
        "hiddenness": 0.60,
        "rewrite_harshness": 0.40,
        "local_deceptiveness": 0.30,
    })["candidates"]
    renewal = COAdapterRenewal(DummyCore())._derive_from_visible_history({"A": 3, "obs": 0})["candidates"]
    return {
        "bandit_initial": list(bandit),
        "maintenance_partial_midhealth": list(maint),
        "maze_visible_local": list(maze),
        "latent_mechanism_visible": list(latent),
        "renewal_initial": list(renewal),
    }


def _trace_case(name: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    on_rows, on_commit = _run_candidate_commitment(candidates, name)
    off_rows, off_commit = _run_candidate_commitment(_strip_public_effects(candidates), name)
    telemetry = _relation_telemetry(on_rows)
    rels = dict(telemetry.get("relations_by_type", {}) or {})
    structural_relation_count = sum(int(v) for k, v in rels.items() if k not in {"rivalry", "decision_slot_competition"})
    weak_competition = int(rels.get("decision_slot_competition", 0) or 0)
    internal_operation_rows = int(telemetry.get("branch_internal_operation_rows", 0) or 0)
    internal_unresolved = float(telemetry.get("branch_internal_unresolved_pressure_total", 0.0) or 0.0)
    delta = _field_delta(on_rows, off_rows)
    return {
        "family": name,
        "candidate_rows": len(on_rows),
        "relations_total": int(telemetry.get("relations_total", 0) or 0),
        "relations_by_type": rels,
        "structural_relations": int(structural_relation_count),
        "weak_decision_competition_relations": int(weak_competition),
        "non_rival_relations": int(structural_relation_count),
        "branch_internal_operation_rows": int(internal_operation_rows),
        "branch_internal_unresolved_pressure_total": float(internal_unresolved),
        "branch_internal_hiddenness_pressure_total": float(telemetry.get("branch_internal_hiddenness_pressure_total", 0.0) or 0.0),
        "branch_internal_resolver_support_total": float(telemetry.get("branch_internal_resolver_support_total", 0.0) or 0.0),
        "rows_with_public_effects": int(telemetry.get("rows_with_public_effects", 0) or 0),
        "rows_with_relations": int(telemetry.get("rows_with_relations", 0) or 0),
        "identity_source_counts": dict(telemetry.get("identity_source_counts", {}) or {}),
        "field_delta_l1": float(delta["field_delta_l1"]),
        "field_delta_max": float(delta["field_delta_max"]),
        "field_delta_by_action": delta["by_action"],
        "commitment_on_action": on_commit.get("action"),
        "commitment_off_action": off_commit.get("action"),
        "commitment_on_mode": on_commit.get("canonical_commitment_mode"),
        "commitment_off_mode": off_commit.get("canonical_commitment_mode"),
        "commitment_action_changed": bool(on_commit.get("action") != off_commit.get("action")),
        "commitment_mode_changed": bool(on_commit.get("canonical_commitment_mode") != off_commit.get("canonical_commitment_mode")),
    }


def trace_all_cases() -> List[Dict[str, Any]]:
    return [_trace_case(name, candidates) for name, candidates in _case_candidates().items()]


def test_relation_path_changes_rcf_field_outputs_on_real_adapter_rows() -> None:
    cases = trace_all_cases()
    _assert(cases, "expected diagnostic cases")
    structural_cases = [
        c for c in cases
        if c.get("structural_relations", c.get("non_rival_relations", 0)) > 0
        or c.get("branch_internal_operation_rows", 0) > 0
    ]
    positive = [c for c in structural_cases if c["field_delta_l1"] > 0.01]
    _assert(len(positive) == len(structural_cases), f"every sampled family with structural relations or branch-internal operations should show RCF/certificate field deltas: {cases}")
    weak_only = [
        c for c in cases
        if c.get("weak_decision_competition_relations", 0) > 0
        and c.get("structural_relations", 0) == 0
        and c.get("branch_internal_operation_rows", 0) == 0
    ]
    _assert(all(c["field_delta_l1"] <= 0.01 for c in weak_only), f"weak decision-slot competition alone should not deform RCF field: {weak_only}")


def test_non_rival_relations_exist_where_public_burden_effects_should_support_them() -> None:
    cases = {c["family"]: c for c in trace_all_cases()}
    for name in ("maintenance_partial_midhealth", "maze_visible_local", "latent_mechanism_visible"):
        _assert(cases[name]["non_rival_relations"] > 0, f"{name} should derive non-rival burden/evidence/equivalence relations: {cases[name]}")
    for name in ("bandit_initial", "renewal_initial"):
        _assert(cases[name]["branch_internal_operation_rows"] > 0, f"{name} should carry branch-internal uncertainty/evidence operations even without cross-branch relations: {cases[name]}")


def test_public_effects_do_not_contain_solver_leakage_terms() -> None:
    for name, candidates in _case_candidates().items():
        for cand in candidates:
            for eff in cand.get("public_effects", []) or []:
                text = " ".join(str(v).lower() for v in eff.values())
                _assert(str(eff.get("leakage_status", "")).lower() == "public", f"{name}: non-public leakage status: {eff}")
                for forbidden in FORBIDDEN_TERMS:
                    _assert(forbidden not in text, f"{name}: forbidden solver-like term {forbidden} in public effect {eff}")


def test_commitment_is_not_claimed_as_validated_by_field_deltas_alone() -> None:
    cases = trace_all_cases()
    changed = [c for c in cases if c["commitment_action_changed"] or c["commitment_mode_changed"]]
    unchanged_with_field_delta = [c for c in cases if c["field_delta_l1"] > 0.01 and not c["commitment_action_changed"]]
    # This test intentionally records the current boundary: relation topology is
    # proven to affect RCF field outputs, but commitment/action changes are not
    # required for the diagnostic and should not be claimed merely from coverage.
    _assert(unchanged_with_field_delta, "expected at least one case where field changed but action did not, preserving the caveat")
    _assert(len(changed) <= len(cases), "sanity check")


if __name__ == "__main__":
    test_relation_path_changes_rcf_field_outputs_on_real_adapter_rows()
    test_non_rival_relations_exist_where_public_burden_effects_should_support_them()
    test_public_effects_do_not_contain_solver_leakage_terms()
    test_commitment_is_not_claimed_as_validated_by_field_deltas_alone()
