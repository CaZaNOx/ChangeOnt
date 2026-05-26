"""Invariants for first-pass multi-step continuation memory.

Run with: python -m agents.co.tests.multi_step_continuation_identity_invariants
"""
from __future__ import annotations

from agents.co.runtime.surfaces.continuation_state import ContinuationStateTracker, derive_continuation_memory_id
from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.tests.relation_path_trace_diagnostics import TraceBus, TraceHeader, TraceHeaderState


def _effect(operation: str, burden_type: str, *, scope: str = "machine_health", coupling: str = "health_continuation", magnitude: float = 0.75) -> dict:
    return {
        "operation": operation,
        "kind": "burden",
        "burden_type": burden_type,
        "scope": scope,
        "magnitude": magnitude,
        "public_basis": "declared_transition_rule",
        "leakage_status": "public",
        "direction": operation,
        "coupling": coupling,
    }


def test_public_burden_domain_persists_across_action_expressions() -> None:
    run_key, run_source = derive_continuation_memory_id({"action": "RUN_EXPR", "public_effects": [_effect("carry", "degradation")]})
    repair_key, repair_source = derive_continuation_memory_id({"action": "REPAIR_EXPR", "public_effects": [_effect("reduce", "degradation")]})
    assert run_source == "public_effect_domain"
    assert repair_source == "public_effect_domain"
    assert run_key == repair_key, (run_key, repair_key)


def test_distinct_public_burden_domains_do_not_merge() -> None:
    degradation_key, _ = derive_continuation_memory_id({"action": "A", "public_effects": [_effect("carry", "degradation")]})
    hiddenness_key, _ = derive_continuation_memory_id({"action": "B", "public_effects": [_effect("reveal", "hiddenness", scope="health_observability")]})
    assert degradation_key != hiddenness_key


def test_batch_tracker_updates_shared_memory_once_per_step() -> None:
    tracker = ContinuationStateTracker()
    key, _ = derive_continuation_memory_id({"action": "A", "public_effects": [_effect("carry", "degradation")]})
    outs = tracker.update_candidate_batch([
        (key, {"support": 0.30, "burden": 0.70, "fracture": 0.60, "uncertainty": 0.20}),
        (key, {"support": 0.70, "burden": 0.20, "fracture": 0.10, "uncertainty": 0.10}),
    ])
    assert len(outs) == 2
    assert outs[0]["continuation_age"] == 1.0
    assert outs[1]["continuation_age"] == 1.0
    assert outs[0]["continuation_memory_shared_count"] == 2.0
    assert len(tracker.snapshots()) == 1


def test_candidate_surface_memory_can_cross_actions_without_collapsing_branch_ids() -> None:
    obs = {
        "family": "continuation_identity_probe",
        "t": 0,
        "action_space": ["CARRIER_EXPR", "RESOLVER_EXPR"],
        "candidates": [
            {
                "candidate_id": "CARRIER_EXPR",
                "legal": True,
                "visible_delta": 0.55,
                "line_support": 0.55,
                "coverage_adequacy": 0.60,
                "tested_hint": 0.25,
                "uncertainty_hint": 0.30,
                "reversibility_hint": 0.35,
                "contradiction_hint": 0.65,
                "public_effects": [_effect("carry", "degradation", magnitude=0.80)],
            },
            {
                "candidate_id": "RESOLVER_EXPR",
                "legal": True,
                "visible_delta": 0.48,
                "line_support": 0.50,
                "coverage_adequacy": 0.55,
                "tested_hint": 0.25,
                "uncertainty_hint": 0.35,
                "reversibility_hint": 0.75,
                "contradiction_hint": 0.20,
                "public_effects": [_effect("reduce", "degradation", magnitude=0.60)],
            },
        ],
    }
    prims = {"signal_bus": TraceBus()}
    CandidateEvidenceSurface(dynamic_shape_enabled=False).step(obs, prims, TraceHeader(TraceHeaderState()), None)
    rows = prims["__candidate_publication_rows__"]
    assert len(rows) == 2
    memory_ids = {str(r.get("continuation_memory_id")) for r in rows}
    branch_ids = {str(r.get("branch_id")) for r in rows}
    assert len(memory_ids) == 1, rows
    assert len(branch_ids) == 2, rows
    assert all(r.get("continuation_memory_source") == "public_effect_domain" for r in rows)
    snapshots = prims["__continuation_state_snapshots__"]
    assert len(snapshots) == 1, snapshots


def test_action_fallback_remains_last_resort_only() -> None:
    key, source = derive_continuation_memory_id({"action": "ONLY_INTERFACE_EXPR", "public_effects": []})
    assert str(key) == "ONLY_INTERFACE_EXPR"
    assert source == "action"


def main() -> None:
    test_public_burden_domain_persists_across_action_expressions()
    test_distinct_public_burden_domains_do_not_merge()
    test_batch_tracker_updates_shared_memory_once_per_step()
    test_candidate_surface_memory_can_cross_actions_without_collapsing_branch_ids()
    test_action_fallback_remains_last_resort_only()
    print("multi_step_continuation_identity_invariants passed")


if __name__ == "__main__":
    main()
