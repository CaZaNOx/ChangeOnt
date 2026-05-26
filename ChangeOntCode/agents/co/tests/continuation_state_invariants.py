"""Invariant/diagnostic module for continuation state invariants.

Run with: python -m agents.co.tests.continuation_state_invariants
"""
from __future__ import annotations

from typing import Any, Dict, List

from agents.co.runtime.surfaces.continuation_state import ContinuationStateTracker
from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface


class DummyBus:
    def __init__(self) -> None:
        self.votes: List[Dict[str, Any]] = []
    def publish(self, **kw: Any) -> None:
        self.votes.append(dict(kw))


class DummyHeaderState:
    evidence_gate = 0.55
    fracture_tolerance = 0.30
    retention_depth = 0.65
    collapse_permission = 0.45
    identity_support_threshold = 0.55
    support_evidence = 0.45
    rival_breadth = 0.70
    nonlocal_authority = 0.85
    path_sensitivity = 0.88
    local_authority = 0.20
    support_carry_forward = 0.45
    revision_permissibility = 0.75
    collapse_admissibility = 0.45


class DummyHeader:
    def __init__(self) -> None:
        self.state = DummyHeaderState()


def _abstract_obs(a_burden: float, b_burden: float = 0.08) -> Dict[str, Any]:
    return {
        "action_space": ["A", "B", "SAMPLE"],
        "problem_contract": {"actions": {"count": 3, "native_type": "abstract"}, "decision_scope": "anchor", "task_anchor": {"kind": "abstract_continuation", "provided_externally": True}},
        "candidates": [
            {"candidate_id": "A", "legal": True, "visible_delta": 0.82, "line_support": 0.82, "uncertainty_hint": 0.12, "novelty_hint": 0.05, "coverage_adequacy": 0.80, "tested_hint": 0.80, "reversibility_hint": 0.36, "contradiction_hint": a_burden},
            {"candidate_id": "B", "legal": True, "visible_delta": 0.48, "line_support": 0.50, "uncertainty_hint": 0.18, "novelty_hint": 0.10, "coverage_adequacy": 0.72, "tested_hint": 0.66, "reversibility_hint": 0.86, "contradiction_hint": b_burden},
            {"candidate_id": "SAMPLE", "legal": True, "visible_delta": 0.40, "line_support": 0.42, "uncertainty_hint": 0.74, "novelty_hint": 0.78, "coverage_adequacy": 0.20, "tested_hint": 0.20, "reversibility_hint": 0.96, "contradiction_hint": 0.10},
        ],
    }


def _step(surface: CandidateEvidenceSurface, obs: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    prims: Dict[str, Any] = {"signal_bus": DummyBus()}
    surface.step(obs, prims, DummyHeader(), None)
    rows = prims.get("__candidate_publication_rows__") or []
    return {str(r["action"]): r for r in rows}


def test_continuation_tracker_accumulates_burden_without_family_semantics() -> None:
    tracker = ContinuationStateTracker(alpha=0.5)
    first = tracker.update_candidate("A", {"support": 0.80, "burden": 0.10, "fracture": 0.08, "uncertainty": 0.10})
    second = tracker.update_candidate("A", {"support": 0.80, "burden": 0.72, "fracture": 0.60, "uncertainty": 0.10})
    assert second["burden_accumulation"] > first["burden_accumulation"]
    assert second["burden_trend"] > first["burden_trend"]
    assert second["continuation_instability"] > first["continuation_instability"]
    assert second["continuation_viability"] < first["continuation_viability"]


def test_candidate_surface_continuation_viability_decays_under_rising_burden() -> None:
    surface = CandidateEvidenceSurface(continuation_alpha=0.55)
    early = _step(surface, _abstract_obs(a_burden=0.12))
    mid = _step(surface, _abstract_obs(a_burden=0.48))
    late = _step(surface, _abstract_obs(a_burden=0.82))
    assert late["A"]["burden_accumulation"] > early["A"]["burden_accumulation"]
    assert late["A"]["continuation_instability"] > early["A"]["continuation_instability"]
    assert late["A"]["continuation_viability"] < early["A"]["continuation_viability"]
    assert late["B"]["continuation_viability"] >= mid["B"]["continuation_viability"] - 1e-9
    assert late["B"]["decision_state"] - late["A"]["decision_state"] > early["B"]["decision_state"] - early["A"]["decision_state"]


def test_continuation_state_source_has_no_family_or_action_policy_literals() -> None:
    import pathlib
    src = pathlib.Path(__file__).parents[1] / "runtime" / "surfaces" / "continuation_state.py"
    text = src.read_text()
    forbidden = ["maintenance", "bandit", "maze", "renewal", "RUN", "REPAIR", "REPLACE", "INSPECT", "WAIT"]
    for token in forbidden:
        assert token not in text, token


if __name__ == "__main__":
    test_continuation_tracker_accumulates_burden_without_family_semantics()
    test_candidate_surface_continuation_viability_decays_under_rising_burden()
    test_continuation_state_source_has_no_family_or_action_policy_literals()
