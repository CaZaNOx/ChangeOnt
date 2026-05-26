"""Invariant/diagnostic module for commitment surface readout invariants.

Run with: python -m agents.co.tests.commitment_surface_readout_invariants
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface


class DummyBus:
    def __init__(self, votes: List[Dict[str, Any]] | None = None) -> None:
        self._votes = list(votes or [])

    def drain(self, scope_key: str | None = None):
        if scope_key is None:
            out = list(self._votes)
            self._votes.clear()
            return out
        out = [v for v in self._votes if v.get("scope_key") == scope_key]
        self._votes = [v for v in self._votes if v.get("scope_key") != scope_key]
        return out

    def signals(self):
        return {}


@dataclass
class DummyHeaderState:
    co_weight: float = 1.0
    evidence_gate: float = 0.7
    fracture_tolerance: float = 0.5
    retention_depth: float = 0.6
    collapse_permission: float = 0.5
    identity_support_threshold: float = 0.5
    support_evidence: float = 0.4
    collapse_admissibility: float = 0.5
    revision_permissibility: float = 0.5
    support_carry_forward: float = 0.5
    rival_breadth: float = 0.5
    nonlocal_authority: float = 0.5
    path_sensitivity: float = 0.5
    local_authority: float = 0.5


@dataclass
class DummyHeader:
    state: DummyHeaderState


def _obs() -> Dict[str, Any]:
    return {
        "t": 5,
        "family": "bandit",
        "action_space": [0, 1],
        "problem_contract": {
            "actions": {"count": 2, "native_type": "discrete"},
            "task_anchor": {"kind": "reward_seek", "provided_externally": False},
            "observability_profile": {"state": "direct", "outcome": "direct", "constraints": "direct"},
        },
        "candidates": [
            {"candidate_id": 0, "legal": True, "goal_relation": 0.0, "context_relation": 0.0, "reward_relation": 0.0},
            {"candidate_id": 1, "legal": True, "goal_relation": 1.0, "context_relation": 1.0, "reward_relation": 1.0},
        ],
    }


def _votes(scope_key: str) -> List[Dict[str, Any]]:
    return [
        {"scope_key": scope_key, "action": 0, "weight": 0.80, "scope": "base", "source": "test"},
        {"scope_key": scope_key, "action": 0, "weight": 0.30, "scope": "persistence", "source": "test"},
        {"scope_key": scope_key, "action": 0, "weight": 0.10, "scope": "salience", "source": "test"},
        {"scope_key": scope_key, "action": 0, "weight": 0.05, "scope": "fracture", "source": "test"},
        {"scope_key": scope_key, "action": 1, "weight": 0.55, "scope": "base", "source": "test"},
        {"scope_key": scope_key, "action": 1, "weight": 0.10, "scope": "persistence", "source": "test"},
        {"scope_key": scope_key, "action": 1, "weight": 0.12, "scope": "salience", "source": "test"},
        {"scope_key": scope_key, "action": 1, "weight": 0.20, "scope": "fracture", "source": "test"},
    ]


def _rows() -> List[Dict[str, Any]]:
    return [
        {"action": 0, "base_state": 0.80, "persistence_state": 0.30, "salience_state": 0.10, "fracture_state": 0.05},
        {"action": 1, "base_state": 0.55, "persistence_state": 0.10, "salience_state": 0.12, "fracture_state": 0.20},
    ]


def _run(obs: Dict[str, Any], votes: List[Dict[str, Any]]) -> Dict[str, Any]:
    head = CommitmentSurface(collapse_enabled=False)
    prims: Dict[str, Any] = {"signal_bus": DummyBus(votes), "__candidate_publication_rows__": _rows()}
    header = DummyHeader(DummyHeaderState())
    return head.step(obs, prims, header, None)


def test_commitment_surface_ignores_raw_candidate_priority_fields_when_publication_rows_are_fixed() -> None:
    out1 = _run(_obs(), _votes("bandit:general"))

    obs2 = _obs()
    obs2["candidates"][0].update({"goal_relation": 1.0, "context_relation": 1.0, "reward_relation": 1.0, "continuity_support": 1.0, "recent_reward_mean": 1.0})
    obs2["candidates"][1].update({"goal_relation": 0.0, "context_relation": 0.0, "reward_relation": 0.0, "continuity_support": 0.0, "recent_reward_mean": 0.0})
    out2 = _run(obs2, _votes("bandit:general"))

    assert out1["action"] == out2["action"] == 0
    for key in ("commit_readiness", "evidence_margin", "evidence_support"):
        assert abs(float(out1[key]) - float(out2[key])) < 1e-9, key


def test_commitment_surface_ignores_order_and_switch_scopes() -> None:
    scope_key = "bandit:general"
    votes = _votes(scope_key) + [
        {"scope_key": scope_key, "action": 1, "weight": 100.0, "scope": "order", "source": "test"},
        {"scope_key": scope_key, "action": 1, "weight": 100.0, "scope": "switch", "source": "test"},
    ]
    out = _run(_obs(), votes)
    assert out["action"] == 0


def test_salience_channel_preserves_absolute_strength_and_does_not_override_base_support() -> None:
    scope_key = "maintenance_replacement:anchor"
    votes = [
        {"scope_key": scope_key, "action": "RUN", "weight": 0.60, "scope": "base", "source": "test"},
        {"scope_key": scope_key, "action": "RUN", "weight": 0.04, "scope": "salience", "source": "test"},
        {"scope_key": scope_key, "action": "RUN", "weight": 0.40, "scope": "persistence", "source": "test"},
        {"scope_key": scope_key, "action": "RUN", "weight": 0.04, "scope": "fracture", "source": "test"},
        {"scope_key": scope_key, "action": "INSPECT", "weight": 0.54, "scope": "base", "source": "test"},
        {"scope_key": scope_key, "action": "INSPECT", "weight": 0.20, "scope": "salience", "source": "test"},
        {"scope_key": scope_key, "action": "INSPECT", "weight": 0.35, "scope": "persistence", "source": "test"},
        {"scope_key": scope_key, "action": "INSPECT", "weight": 0.03, "scope": "fracture", "source": "test"},
    ]
    rows = [
        {"action": "RUN", "base_state": 0.60, "persistence_state": 0.40, "salience_state": 0.04, "fracture_state": 0.04},
        {"action": "INSPECT", "base_state": 0.54, "persistence_state": 0.35, "salience_state": 0.20, "fracture_state": 0.03},
    ]
    obs = {
        "t": 1,
        "family": "maintenance_replacement",
        "decision_scope": "anchor",
        "action_space": ["RUN", "INSPECT"],
        "candidates": [{"candidate_id": "RUN", "legal": True}, {"candidate_id": "INSPECT", "legal": True}],
    }
    head = CommitmentSurface(collapse_enabled=False)
    prims: Dict[str, Any] = {"signal_bus": DummyBus(votes), "__candidate_publication_rows__": rows}
    header = DummyHeader(DummyHeaderState())
    out = head.step(obs, prims, header, None)
    assert out["action"] == "RUN"
    assert out["candidate_final_scores"]["RUN"] > out["candidate_final_scores"]["INSPECT"]



def _abstract_obs(actions: List[Any]) -> Dict[str, Any]:
    return {
        "t": 3,
        "family": "abstract_test_family",
        "decision_scope": "abstract",
        "action_space": list(actions),
        "candidates": [{"candidate_id": a, "legal": True} for a in actions],
    }


def _row_votes(scope_key: str, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    votes: List[Dict[str, Any]] = []
    for row in rows:
        a = row["action"]
        votes.extend([
            {"scope_key": scope_key, "action": a, "weight": row.get("base_state", row.get("support_mass", 0.0)), "scope": "base", "source": "abstract"},
            {"scope_key": scope_key, "action": a, "weight": row.get("persistence_state", row.get("commitment_stability", 0.0)), "scope": "persistence", "source": "abstract"},
            {"scope_key": scope_key, "action": a, "weight": row.get("salience_state", row.get("sampling_demand", 0.0)), "scope": "salience", "source": "abstract"},
            {"scope_key": scope_key, "action": a, "weight": row.get("fracture_state", row.get("contradiction_burden", 0.0)), "scope": "fracture", "source": "abstract"},
        ])
    return votes


def _run_abstract(rows: List[Dict[str, Any]], state: DummyHeaderState) -> Dict[str, Any]:
    actions = [r["action"] for r in rows]
    obs = _abstract_obs(actions)
    votes = _row_votes("abstract_test_family:abstract", rows)
    prims: Dict[str, Any] = {"signal_bus": DummyBus(votes), "__candidate_publication_rows__": rows}
    return CommitmentSurface(collapse_enabled=False).step(obs, prims, DummyHeader(state), None)


def test_local_support_can_dominate_when_burden_is_low_and_local_authority_is_high() -> None:
    rows = [
        {"action": "A", "support_mass": 0.88, "local_support": 0.90, "decision_state": 0.86, "base_state": 0.86, "commitment_stability": 0.55, "persistence_state": 0.55, "contradiction_burden": 0.05, "fracture_state": 0.05, "sampling_demand": 0.04, "salience_state": 0.04, "uncertainty": 0.10},
        {"action": "B", "support_mass": 0.55, "local_support": 0.52, "decision_state": 0.55, "base_state": 0.55, "commitment_stability": 0.70, "persistence_state": 0.70, "contradiction_burden": 0.04, "fracture_state": 0.04, "sampling_demand": 0.20, "salience_state": 0.20, "uncertainty": 0.35},
    ]
    out = _run_abstract(rows, DummyHeaderState(local_authority=1.0, nonlocal_authority=0.0, path_sensitivity=0.0, revision_permissibility=0.0, collapse_admissibility=1.0, support_carry_forward=0.4, rival_breadth=0.1))
    assert out["action"] == "A"
    assert out["canonical_commitment_mode"] == "dominance"


def test_high_burden_can_defeat_local_support_under_nonlocal_path_sensitive_controls() -> None:
    rows = [
        {"action": "A", "support_mass": 0.86, "local_support": 0.90, "decision_state": 0.84, "base_state": 0.84, "commitment_stability": 0.20, "persistence_state": 0.20, "contradiction_burden": 0.88, "fracture_state": 0.88, "sampling_demand": 0.05, "salience_state": 0.05, "uncertainty": 0.12},
        {"action": "B", "support_mass": 0.58, "local_support": 0.55, "decision_state": 0.58, "base_state": 0.58, "commitment_stability": 0.82, "persistence_state": 0.82, "contradiction_burden": 0.04, "fracture_state": 0.04, "sampling_demand": 0.08, "salience_state": 0.08, "uncertainty": 0.25},
    ]
    out = _run_abstract(rows, DummyHeaderState(local_authority=0.1, nonlocal_authority=1.0, path_sensitivity=1.0, revision_permissibility=0.8, collapse_admissibility=0.1, support_carry_forward=0.8, rival_breadth=0.7, fracture_tolerance=0.1))
    assert out["action"] == "B"
    assert out["canonical_commitment_mode"] in {"stable_continuation", "dominance"}


def test_no_dominance_with_high_uncertainty_can_select_sampling_candidate() -> None:
    rows = [
        {"action": "A", "support_mass": 0.58, "local_support": 0.58, "decision_state": 0.56, "base_state": 0.56, "commitment_stability": 0.20, "persistence_state": 0.20, "contradiction_burden": 0.35, "fracture_state": 0.35, "sampling_demand": 0.10, "salience_state": 0.10, "uncertainty": 0.70},
        {"action": "B", "support_mass": 0.56, "local_support": 0.55, "decision_state": 0.55, "base_state": 0.55, "commitment_stability": 0.18, "persistence_state": 0.18, "contradiction_burden": 0.32, "fracture_state": 0.32, "sampling_demand": 0.12, "salience_state": 0.12, "uncertainty": 0.72},
        {"action": "S", "support_mass": 0.46, "local_support": 0.45, "decision_state": 0.46, "base_state": 0.46, "commitment_stability": 0.15, "persistence_state": 0.15, "contradiction_burden": 0.10, "fracture_state": 0.10, "sampling_demand": 0.92, "salience_state": 0.92, "uncertainty": 0.90},
    ]
    out = _run_abstract(rows, DummyHeaderState(local_authority=0.0, nonlocal_authority=1.0, path_sensitivity=0.7, revision_permissibility=1.0, collapse_admissibility=0.0, support_carry_forward=0.2, rival_breadth=1.0))
    assert out["action"] == "S"
    assert out["canonical_commitment_mode"] == "reopen_or_sample"


def test_same_candidate_packet_can_change_choice_under_different_direct_controls() -> None:
    rows = [
        {"action": "LOCAL", "support_mass": 0.92, "local_support": 0.95, "decision_state": 0.90, "base_state": 0.90, "commitment_stability": 0.20, "persistence_state": 0.20, "continuation_viability": 0.80, "support_persistence": 0.50, "continuation_instability": 0.20, "contradiction_burden": 0.22, "fracture_state": 0.22, "sampling_demand": 0.04, "salience_state": 0.04, "uncertainty": 0.10},
        {"action": "STABLE", "support_mass": 0.55, "local_support": 0.50, "decision_state": 0.55, "base_state": 0.55, "commitment_stability": 0.85, "persistence_state": 0.85, "continuation_viability": 0.70, "support_persistence": 0.85, "continuation_instability": 0.02, "contradiction_burden": 0.02, "fracture_state": 0.02, "sampling_demand": 0.10, "salience_state": 0.10, "uncertainty": 0.35},
    ]
    local_out = _run_abstract(rows, DummyHeaderState(local_authority=1.0, nonlocal_authority=0.0, path_sensitivity=0.0, revision_permissibility=0.0, collapse_admissibility=1.0, support_carry_forward=0.2, rival_breadth=0.0, fracture_tolerance=0.9))
    nonlocal_out = _run_abstract(rows, DummyHeaderState(local_authority=0.0, nonlocal_authority=1.0, path_sensitivity=1.0, revision_permissibility=0.8, collapse_admissibility=0.0, support_carry_forward=0.9, rival_breadth=0.8, fracture_tolerance=0.1))
    assert local_out["action"] == "LOCAL"
    assert nonlocal_out["action"] == "STABLE"

if __name__ == "__main__":
    test_commitment_surface_ignores_raw_candidate_priority_fields_when_publication_rows_are_fixed()
    test_commitment_surface_ignores_order_and_switch_scopes()
    test_salience_channel_preserves_absolute_strength_and_does_not_override_base_support()
    test_local_support_can_dominate_when_burden_is_low_and_local_authority_is_high()
    test_high_burden_can_defeat_local_support_under_nonlocal_path_sensitive_controls()
    test_no_dominance_with_high_uncertainty_can_select_sampling_candidate()
    test_same_candidate_packet_can_change_choice_under_different_direct_controls()
