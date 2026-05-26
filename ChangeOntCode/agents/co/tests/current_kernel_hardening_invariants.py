"""Invariants for targeted current-kernel hardening.

Run with: python -m agents.co.tests.current_kernel_hardening_invariants
"""
from __future__ import annotations

from types import SimpleNamespace

from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface
from agents.co.runtime.surfaces.continuation_field import BranchRelation
from agents.co.runtime.surfaces.recursion_scheduler import derive_recursion_schedule
from experiments.studies.current_kernel_diagnostic_map_v1 import _step_summary


class Header:
    def __init__(self) -> None:
        self.state = SimpleNamespace(
            collapse_admissibility=0.40,
            revision_permissibility=0.30,
            support_carry_forward=0.20,
            rival_breadth=0.10,
            nonlocal_authority=0.25,
            path_sensitivity=0.35,
            local_authority=0.15,
            evidence_gate=0.50,
            fracture_tolerance=0.60,
        )


def test_dynamic_shape_effective_controls_are_commitment_visible() -> None:
    cs = CommitmentSurface(seed=0)
    controls = cs._direct_control_snapshot(
        Header(),
        observation={},
        primitives={
            "__dynamic_shape_effective_controls__": {
                "local_authority": 0.77,
                "path_sensitivity": 0.88,
                "revision_permissibility": 0.66,
                "dynamic_shape_urgency": 0.55,
                "dynamic_shape_projection_horizon": 0.44,
                "dynamic_shape_gauge_confidence": 0.91,
            }
        },
    )
    assert controls["dynamic_shape_controls_applied"] == 1.0, controls
    assert abs(controls["local_authority"] - 0.77) < 1e-9, controls
    assert abs(controls["path_sensitivity"] - 0.88) < 1e-9, controls
    assert abs(controls["static_local_authority"] - 0.15) < 1e-9, controls
    assert abs(controls["dynamic_shape_gauge_confidence"] - 0.91) < 1e-9, controls


def test_recursion_provenance_split_blocks_weak_sampling_as_structural_recursion() -> None:
    rows = [
        {
            "candidate_id": "branch_a",
            "support_mass": 0.40,
            "decision_state": 0.40,
            "field_debt": 0.08,
            "field_grey_pressure": 0.05,
            "field_recursion_budget": 0.72,
            "sampling_demand": 0.86,
            "uncertainty": 0.84,
            "branch_internal_hiddenness_pressure": 0.0,
            "branch_internal_threshold_pressure": 0.0,
        },
        {
            "candidate_id": "branch_b",
            "support_mass": 0.42,
            "decision_state": 0.42,
            "field_debt": 0.08,
            "field_grey_pressure": 0.05,
            "field_recursion_budget": 0.72,
            "sampling_demand": 0.86,
            "uncertainty": 0.84,
            "branch_internal_hiddenness_pressure": 0.0,
            "branch_internal_threshold_pressure": 0.0,
        },
    ]
    schedules = derive_recursion_schedule(
        rows,
        relations=[BranchRelation("branch_a", "branch_b", "decision_slot_competition", 1.0)],
        controls={"low_evidence_sampling": 0.90, "path_sensitivity": 0.75, "revision_permissibility": 0.75},
    )
    s = schedules["branch_a"]
    assert s.weak_procedural_channel > 0.0, s
    assert s.sampling_uncertainty_channel >= 0.50, s
    assert s.inherited_field_channel >= 0.70, s
    assert s.demand <= 0.24, s
    assert s.budget == 0, s
    assert "weak_competition_logged_only" in s.reasons or "sampling_uncertainty_channel_logged_only" in s.reasons, s


def test_diagnostic_step_summary_carries_deep_trace_fields() -> None:
    rows = [
        {
            "action": "branch_a",
            "candidate_id": "branch_a",
            "support_mass": 0.50,
            "field_recursion_budget": 0.22,
            "field_recursion_budget_before_scheduler": 0.70,
            "recursion_scheduler_demand": 0.22,
            "recursion_scheduler_structural_channel": 0.22,
            "recursion_scheduler_sampling_uncertainty_channel": 0.81,
            "recursion_scheduler_weak_procedural_channel": 0.25,
            "dynamic_shape_effective_controls": {"local_authority": 0.61, "dynamic_shape_urgency": 0.42},
            "dynamic_shape_controls_active": True,
            "dynamic_shape_update": {"applied": True, "state_after": {"update_count": 1}},
        }
    ]
    sel = {
        "canonical_commitment_mode": "dominance",
        "canonical_commitment_reason": "test",
        "direct_controls_used": {"dynamic_shape_controls_applied": 1.0, "local_authority": 0.61},
        "canonical_commitment_assessment": {"branch_a": {"dominance_score": 0.40}},
        "co_evidence_valid_for_step": True,
    }
    step = _step_summary(family="generic", mode="generic", seed=0, variant="full_current", t=0, action="branch_a", reward=0.0, sel=sel, rows=rows)
    assert step["dynamic_shape_controls_applied_in_commitment"] is True, step
    assert step["row_trace_sample"], step
    trace = step["row_trace_sample"][0]
    assert trace["recursion_scheduler_sampling_uncertainty_channel"] == 0.81, trace
    assert trace["dynamic_shape_effective_controls"]["local_authority"] == 0.61, trace
    assert "canonical_commitment_assessment_summary" in step, step


def main() -> None:
    test_dynamic_shape_effective_controls_are_commitment_visible()
    test_recursion_provenance_split_blocks_weak_sampling_as_structural_recursion()
    test_diagnostic_step_summary_carries_deep_trace_fields()
    print("current_kernel_hardening_invariants passed")


if __name__ == "__main__":
    main()
