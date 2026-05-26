"""Invariants for CandidateSurface publication and fail-closed intake behavior."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface


class DummyBus:
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


@dataclass
class DummyHeaderState:
    evidence_gate: float = 0.7
    fracture_tolerance: float = 0.5
    retention_depth: float = 0.6
    collapse_permission: float = 0.5
    identity_support_threshold: float = 0.5
    support_evidence: float = 0.4


@dataclass
class DummyHeader:
    state: DummyHeaderState


def _base_obs() -> Dict[str, Any]:
    return {
        "action_space": [0, 1],
        "problem_contract": {
            "actions": {"count": 2, "native_type": "discrete"},
            "task_anchor": {"kind": "goal_reach", "provided_externally": True},
            "observability_profile": {"state": "direct", "outcome": "direct", "constraints": "direct"},
            "timescale_profile": {"horizon_fixity": "fixed", "drift": "slow"},
            "reversibility_profile": {"action_reversibility": "mixed", "commitment_cost": "medium"},
        },
        "candidates": [
            {
                "candidate_id": 0,
                "legal": True,
                "support_depth": 0.8,
                "paired_depth": 0.7,
                "line_support": 0.75,
                "continuity_support": 0.6,
                "uncertainty_hint": 0.3,
                "novelty_hint": 0.2,
                "contradiction_hint": 0.1,
                "coverage_adequacy": 0.7,
                "tested_hint": 0.6,
                "goal_relation": 0.1,
            },
            {
                "candidate_id": 1,
                "legal": True,
                "support_depth": 0.4,
                "paired_depth": 0.4,
                "line_support": 0.35,
                "continuity_support": 0.2,
                "uncertainty_hint": 0.7,
                "novelty_hint": 0.4,
                "contradiction_hint": 0.3,
                "coverage_adequacy": 0.5,
                "tested_hint": 0.5,
                "goal_relation": 0.9,
            },
        ],
    }


def _run(obs: Dict[str, Any]) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    bus = DummyBus()
    prims: Dict[str, Any] = {"signal_bus": bus}
    header = DummyHeader(DummyHeaderState())
    surf = CandidateEvidenceSurface()
    out = surf.step(obs, prims, header, None)
    return prims.get("__candidate_publication_rows__", []), out | {"votes": list(bus._votes)}


def test_candidate_surface_is_local_and_does_not_emit_policy_scopes() -> None:
    obs1 = _base_obs()
    rows1, out1 = _run(obs1)
    row1 = next(r for r in rows1 if r["action"] == 0)

    obs2 = _base_obs()
    # Change only the *other* candidate radically.
    obs2["candidates"][1].update({
        "support_depth": 1.0,
        "paired_depth": 1.0,
        "line_support": 1.0,
        "continuity_support": 1.0,
        "uncertainty_hint": 0.0,
        "novelty_hint": 0.0,
        "contradiction_hint": 0.0,
        "coverage_adequacy": 1.0,
        "tested_hint": 1.0,
        "goal_relation": 1.0,
    })
    rows2, out2 = _run(obs2)
    row2 = next(r for r in rows2 if r["action"] == 0)

    for key in ("local_support", "support_mass", "uncertainty", "novelty", "coverage"):
        assert abs(float(row1[key]) - float(row2[key])) < 1e-9, key

    scopes = {v["scope"] for v in out1["votes"]}
    assert scopes == {"base", "persistence", "salience", "fracture"}


def test_candidate_surface_publication_ignores_goal_relation_shifts() -> None:
    obs1 = _base_obs()
    rows1, _ = _run(obs1)
    row1 = next(r for r in rows1 if r["action"] == 0)

    obs2 = _base_obs()
    obs2["candidates"][0]["goal_relation"] = 1.0
    rows2, _ = _run(obs2)
    row2 = next(r for r in rows2 if r["action"] == 0)

    for key in ("local_support", "support_mass", "uncertainty", "novelty", "coverage"):
        assert abs(float(row1[key]) - float(row2[key])) < 1e-9, key


def test_candidate_surface_publication_ignores_support_depth_and_continuity_shifts() -> None:
    hdr = DummyHeader(DummyHeaderState())
    obs1 = {"candidates": [{"candidate_id": 0, "legal": True, "coverage_adequacy": 0.6, "tested_hint": 0.6, "uncertainty_hint": 0.2, "support_depth": 0.0, "continuity_support": 0.0}], "action_space": [0]}
    obs2 = {"candidates": [{"candidate_id": 0, "legal": True, "coverage_adequacy": 0.6, "tested_hint": 0.6, "uncertainty_hint": 0.2, "support_depth": 1.0, "continuity_support": 1.0}], "action_space": [0]}
    prims1 = {"signal_bus": DummyBus()}
    prims2 = {"signal_bus": DummyBus()}
    CandidateEvidenceSurface().step(obs1, prims1, hdr, None)
    CandidateEvidenceSurface().step(obs2, prims2, hdr, None)
    rows1 = list(prims1.get("__candidate_publication_rows__") or [])
    rows2 = list(prims2.get("__candidate_publication_rows__") or [])
    assert rows1 == rows2


def test_candidate_surface_transforms_burden_hint_into_fracture_state() -> None:
    surf = CandidateEvidenceSurface()
    hdr = DummyHeader(DummyHeaderState())
    obs_low = {
        "candidates": [{
            "candidate_id": 0, "legal": True, "visible_delta": 0.7, "line_support": 0.7,
            "coverage_adequacy": 0.8, "tested_hint": 0.6, "uncertainty_hint": 0.2,
            "contradiction_hint": 0.0, "reversibility_hint": 0.8,
        }],
        "action_space": [0],
    }
    obs_high = {
        "candidates": [{
            "candidate_id": 0, "legal": True, "visible_delta": 0.7, "line_support": 0.7,
            "coverage_adequacy": 0.8, "tested_hint": 0.6, "uncertainty_hint": 0.2,
            "contradiction_hint": 0.8, "reversibility_hint": 0.8,
        }],
        "action_space": [0],
    }
    prims1: Dict[str, Any] = {"signal_bus": DummyBus()}
    prims2: Dict[str, Any] = {"signal_bus": DummyBus()}
    surf.step(obs_low, prims1, hdr, None)
    surf.step(obs_high, prims2, hdr, None)
    low = prims1["__candidate_publication_rows__"][0]
    high = prims2["__candidate_publication_rows__"][0]
    assert float(high["fracture_state"]) > float(low["fracture_state"])
    assert float(high["decision_state"]) < float(low["decision_state"])




def _header_with(**kw: float) -> DummyHeader:
    state = DummyHeaderState()
    for k, v in kw.items():
        setattr(state, k, float(v))
    return DummyHeader(state)


def _run_with_header(obs: Dict[str, Any], header: DummyHeader) -> List[Dict[str, Any]]:
    bus = DummyBus()
    prims: Dict[str, Any] = {"signal_bus": bus}
    surf = CandidateEvidenceSurface()
    surf.step(obs, prims, header, None)
    return prims.get("__candidate_publication_rows__", [])


def _burden_tradeoff_obs() -> Dict[str, Any]:
    return {
        "action_space": ["A", "B", "SAMPLE"],
        "problem_contract": {
            "actions": {"count": 3, "native_type": "abstract"},
            "decision_scope": "anchor",
            "task_anchor": {"kind": "abstract_continuation", "provided_externally": True},
        },
        "candidates": [
            {
                "candidate_id": "A",
                "legal": True,
                "visible_delta": 0.82,
                "line_support": 0.82,
                "uncertainty_hint": 0.12,
                "novelty_hint": 0.05,
                "coverage_adequacy": 0.80,
                "tested_hint": 0.80,
                "reversibility_hint": 0.35,
                "contradiction_hint": 0.72,
            },
            {
                "candidate_id": "B",
                "legal": True,
                "visible_delta": 0.46,
                "line_support": 0.48,
                "uncertainty_hint": 0.20,
                "novelty_hint": 0.10,
                "coverage_adequacy": 0.72,
                "tested_hint": 0.65,
                "reversibility_hint": 0.82,
                "contradiction_hint": 0.08,
            },
            {
                "candidate_id": "SAMPLE",
                "legal": True,
                "visible_delta": 0.40,
                "line_support": 0.42,
                "uncertainty_hint": 0.72,
                "novelty_hint": 0.80,
                "coverage_adequacy": 0.20,
                "tested_hint": 0.20,
                "reversibility_hint": 0.95,
                "contradiction_hint": 0.12,
            },
        ],
    }


def test_candidate_surface_derives_preventive_support_from_relative_burden() -> None:
    rows = _run_with_header(
        _burden_tradeoff_obs(),
        _header_with(
            local_authority=0.25,
            nonlocal_authority=0.85,
            path_sensitivity=0.85,
            rival_breadth=0.55,
            revision_permissibility=0.70,
            support_carry_forward=0.45,
            evidence_gate=0.55,
            fracture_tolerance=0.35,
        ),
    )
    by = {r["action"]: r for r in rows}
    assert by["B"]["preventive_support"] > by["A"]["preventive_support"]
    assert by["A"]["fracture_state"] > by["B"]["fracture_state"]
    assert by["B"]["stability_under_change"] > by["A"]["stability_under_change"]


def test_candidate_surface_shape_controls_change_publication_without_action_names() -> None:
    obs = _burden_tradeoff_obs()
    local_rows = _run_with_header(
        obs,
        _header_with(
            local_authority=0.90,
            nonlocal_authority=0.10,
            path_sensitivity=0.10,
            rival_breadth=0.10,
            revision_permissibility=0.20,
            support_carry_forward=0.80,
            evidence_gate=0.85,
            fracture_tolerance=0.75,
        ),
    )
    burden_rows = _run_with_header(
        obs,
        _header_with(
            local_authority=0.20,
            nonlocal_authority=0.90,
            path_sensitivity=0.90,
            rival_breadth=0.65,
            revision_permissibility=0.75,
            support_carry_forward=0.45,
            evidence_gate=0.55,
            fracture_tolerance=0.30,
        ),
    )
    local = {r["action"]: r for r in local_rows}
    burden = {r["action"]: r for r in burden_rows}
    # Under burden-sensitive controls, the low-burden continuation gains relative
    # decision support against the locally attractive but burden-heavy candidate.
    local_gap = float(local["A"]["decision_state"]) - float(local["B"]["decision_state"])
    burden_gap = float(burden["A"]["decision_state"]) - float(burden["B"]["decision_state"])
    assert burden_gap < local_gap


def test_candidate_surface_hiddenness_increases_sampling_demand() -> None:
    obs = _burden_tradeoff_obs()
    local_rows = _run_with_header(
        obs,
        _header_with(local_authority=0.85, nonlocal_authority=0.10, rival_breadth=0.10, revision_permissibility=0.20, evidence_gate=0.85),
    )
    hidden_rows = _run_with_header(
        obs,
        _header_with(local_authority=0.20, nonlocal_authority=0.90, rival_breadth=0.85, revision_permissibility=0.80, evidence_gate=0.35),
    )
    local = {r["action"]: r for r in local_rows}
    hidden = {r["action"]: r for r in hidden_rows}
    assert hidden["SAMPLE"]["sampling_demand"] > local["SAMPLE"]["sampling_demand"]




def test_candidate_surface_derives_relations_from_public_effects_before_rcf() -> None:
    obs = _base_obs()
    obs["candidates"][0]["public_effects"] = [
        {
            "effect_id": "carry_debt",
            "kind": "burden",
            "operation": "carry",
            "burden_type": "degradation",
            "scope": "machine",
            "magnitude": 0.9,
            "public_basis": "declared_transition_rule",
            "leakage_status": "public",
        }
    ]
    obs["candidates"][1]["public_effects"] = [
        {
            "effect_id": "reduce_debt",
            "kind": "burden",
            "operation": "reduce",
            "burden_type": "degradation",
            "scope": "machine",
            "magnitude": 0.9,
            "public_basis": "declared_transition_rule",
            "leakage_status": "public",
        }
    ]
    rows, _ = _run(obs)
    by = {r["action"]: r for r in rows}
    assert by[1]["field_relation_count"] > 0
    assert by[1]["field_relief_support"] > 0.0
    assert by[1]["relation_surface_telemetry"]["relations_by_type"]["relief"] >= 1
    assert by[1]["relation_surface_identity_source"] == "public_effects"


def test_candidate_surface_source_has_no_family_or_action_policy_literals() -> None:
    import pathlib
    src = pathlib.Path(__file__).parents[1] / "runtime" / "surfaces" / "candidate_surface.py"
    text = src.read_text()
    forbidden = ["maintenance", "bandit", "maze", "renewal", "RUN", "REPAIR", "REPLACE", "INSPECT", "WAIT"]
    for token in forbidden:
        assert token not in text, token

if __name__ == "__main__":
    test_candidate_surface_is_local_and_does_not_emit_policy_scopes()
    test_candidate_surface_publication_ignores_goal_relation_shifts()
    test_candidate_surface_publication_ignores_support_depth_and_continuity_shifts()
    test_candidate_surface_transforms_burden_hint_into_fracture_state()
    test_candidate_surface_derives_preventive_support_from_relative_burden()
    test_candidate_surface_shape_controls_change_publication_without_action_names()
    test_candidate_surface_hiddenness_increases_sampling_demand()
    test_candidate_surface_derives_relations_from_public_effects_before_rcf()
    test_candidate_surface_source_has_no_family_or_action_policy_literals()
