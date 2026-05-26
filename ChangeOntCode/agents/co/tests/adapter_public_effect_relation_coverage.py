"""Invariant/diagnostic module for adapter public effect relation coverage.

Run with: python -m agents.co.tests.adapter_public_effect_relation_coverage
"""
from __future__ import annotations

"""Adapter public-effect coverage diagnostics.

These are not reward/performance tests.  They verify that real adapters publish
lawful public burden/effect facts and that the kernel-side RelationSurface can
derive nonzero relation topology from those facts without action-name policy or
hidden-solver hints.
"""

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.runtime.surfaces.relation_surface import derive_relation_surface


class DummyCore:
    def __init__(self) -> None:
        self.primitives = {}
        self.combinators = {}


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _check(name: str, candidates: list[dict], *, require_non_rival_relation: bool = False) -> dict:
    _assert(candidates, f"{name}: expected candidates")
    rows_with_effects = [c for c in candidates if c.get("public_effects")]
    _assert(len(rows_with_effects) == len(candidates), f"{name}: every candidate should publish public_effects")
    for cand in rows_with_effects:
        for eff in cand.get("public_effects", []):
            _assert(eff.get("leakage_status") == "public", f"{name}: effect must be public: {eff}")
            _assert(eff.get("public_basis") in {"visible_observation", "declared_transition_rule", "legal_constraint", "public_history", "parity_honest_uncertainty", "problem_contract"}, f"{name}: non-public basis: {eff}")
            text = " ".join(str(v).lower() for v in eff.values())
            for forbidden in ("optimal", "best_action", "dp_value", "oracle", "hidden_policy"):
                _assert(forbidden not in text, f"{name}: public effect leaks solver-like term {forbidden}: {eff}")
    result = derive_relation_surface(candidates, {})
    _assert(result.telemetry["rows_with_public_effects"] == len(candidates), f"{name}: RelationSurface did not accept all public effects")
    _assert(result.telemetry["relations_total"] > 0, f"{name}: expected nonzero derived relation topology")
    if require_non_rival_relation:
        rels = dict(result.telemetry.get("relations_by_type", {}))
        non_rival = sum(v for k, v in rels.items() if k not in {"rivalry", "decision_slot_competition"})
        _assert(non_rival > 0, f"{name}: expected at least one non-rival burden/evidence relation, got {rels}")
    return result.telemetry


def test_bandit_adapter_public_effects_drive_relation_surface() -> None:
    adapter = COAdapterBandit(DummyCore(), n_arms=3)
    derived = adapter._derive_from_visible_history({"n_arms": 3, "t": 0}, 0)
    telemetry = _check("bandit", list(derived["candidates"]))
    _assert(telemetry["relations_by_type"].get("decision_slot_competition", 0) > 0, "bandit should expose weak one-slot competition")


def test_maintenance_adapter_public_effects_drive_relation_surface() -> None:
    adapter = COAdapterMaintenanceReplacement(DummyCore())
    obs = {
        "observed_health": 2,
        "max_health": 4,
        "health_observed": True,
        "degradation_prob_public": 0.20,
        "wait_recovery_prob_public": 0.00,
        "repair_cost_public": 0.80,
        "replace_cost_public": 2.0,
        "failure_penalty_public": 8.0,
        "observe_health_mode": "partial",
    }
    telemetry = _check("maintenance", list(adapter._derive(obs)["candidates"]), require_non_rival_relation=True)
    rels = dict(telemetry.get("relations_by_type", {}))
    _assert(rels.get("relief", 0) > 0 or rels.get("cancellation", 0) > 0, f"maintenance should derive relief/cancellation, got {rels}")


def test_maze_adapter_public_effects_drive_relation_surface() -> None:
    adapter = COAdapterMaze(DummyCore())
    obs = {
        "pos": (1, 1),
        "goal": (1, 3),
        "grid": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "height": 3,
        "width": 4,
    }
    telemetry = _check("maze", list(adapter._derive(obs)["candidates"]), require_non_rival_relation=True)
    rels = dict(telemetry.get("relations_by_type", {}))
    _assert(rels.get("relief", 0) > 0 or rels.get("equivalence", 0) > 0, f"maze should derive visible-distance/equivalence relations, got {rels}")


def test_latent_adapter_public_effects_drive_relation_surface() -> None:
    adapter = COAdapterLatentMechanism(DummyCore())
    obs = {
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
    }
    telemetry = _check("latent", list(adapter._derive(obs)["candidates"]), require_non_rival_relation=True)
    rels = dict(telemetry.get("relations_by_type", {}))
    _assert(rels.get("relief", 0) > 0 or rels.get("shared_evidence", 0) > 0 or rels.get("equivalence", 0) > 0, f"latent should derive mechanism/route relations, got {rels}")


def test_renewal_adapter_public_effects_drive_relation_surface() -> None:
    adapter = COAdapterRenewal(DummyCore())
    derived = adapter._derive_from_visible_history({"A": 3, "obs": 0})
    telemetry = _check("renewal", list(derived["candidates"]))
    _assert(telemetry["relations_by_type"].get("decision_slot_competition", 0) > 0, "renewal should expose weak one-slot competition")


if __name__ == "__main__":
    test_bandit_adapter_public_effects_drive_relation_surface()
    test_maintenance_adapter_public_effects_drive_relation_surface()
    test_maze_adapter_public_effects_drive_relation_surface()
    test_latent_adapter_public_effects_drive_relation_surface()
    test_renewal_adapter_public_effects_drive_relation_surface()
