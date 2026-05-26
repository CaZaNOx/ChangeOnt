from __future__ import annotations

"""Diagnostic: public-effect relation coverage from real adapters.

This is not a reward benchmark.  It samples representative public observations
from active adapters, reads their candidate rows, and reports whether the
kernel-side RelationSurface can derive branch relations from adapter-published
public burden/effect facts.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.runtime.surfaces.relation_surface import derive_relation_surface

OUT = Path("outputs/adapter_public_effect_relation_coverage_v1.json")


class DummyCore:
    def __init__(self) -> None:
        self.primitives: Dict[str, Any] = {}
        self.combinators: Dict[str, Any] = {}


def _row_summary(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    effect_counts = [len(c.get("public_effects") or []) for c in candidates]
    ops: Dict[str, int] = {}
    bases: Dict[str, int] = {}
    leakage: Dict[str, int] = {}
    for cand in candidates:
        for eff in cand.get("public_effects") or []:
            ops[str(eff.get("operation", ""))] = ops.get(str(eff.get("operation", "")), 0) + 1
            bases[str(eff.get("public_basis", ""))] = bases.get(str(eff.get("public_basis", "")), 0) + 1
            leakage[str(eff.get("leakage_status", ""))] = leakage.get(str(eff.get("leakage_status", "")), 0) + 1
    return {
        "candidate_rows": len(candidates),
        "rows_with_public_effects": sum(1 for c in candidates if c.get("public_effects")),
        "min_effects_per_row": min(effect_counts) if effect_counts else 0,
        "max_effects_per_row": max(effect_counts) if effect_counts else 0,
        "operation_counts": dict(sorted(ops.items())),
        "public_basis_counts": dict(sorted(bases.items())),
        "leakage_status_counts": dict(sorted(leakage.items())),
    }


def _case(name: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = derive_relation_surface(candidates, {})
    return {
        "family": name,
        "candidate_summary": _row_summary(candidates),
        "relation_surface": result.telemetry,
    }


def main() -> None:
    rows: List[Dict[str, Any]] = []

    bandit = COAdapterBandit(DummyCore(), n_arms=3)
    rows.append(_case("bandit_initial", bandit._derive_from_visible_history({"n_arms": 3, "t": 0}, 0)["candidates"]))

    maint = COAdapterMaintenanceReplacement(DummyCore())
    maint_obs = {
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
    rows.append(_case("maintenance_partial_midhealth", maint._derive(maint_obs)["candidates"]))

    maze = COAdapterMaze(DummyCore())
    maze_obs = {
        "pos": (1, 1),
        "goal": (1, 3),
        "grid": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "height": 3,
        "width": 4,
    }
    rows.append(_case("maze_visible_local", maze._derive(maze_obs)["candidates"]))

    latent = COAdapterLatentMechanism(DummyCore())
    latent_obs = {
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
    rows.append(_case("latent_mechanism_visible", latent._derive(latent_obs)["candidates"]))

    renewal = COAdapterRenewal(DummyCore())
    rows.append(_case("renewal_initial", renewal._derive_from_visible_history({"A": 3, "obs": 0})["candidates"]))

    aggregate = {
        "cases": len(rows),
        "candidate_rows": sum(r["candidate_summary"]["candidate_rows"] for r in rows),
        "rows_with_public_effects": sum(r["candidate_summary"]["rows_with_public_effects"] for r in rows),
        "relations_total": sum(int(r["relation_surface"].get("relations_total", 0) or 0) for r in rows),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"aggregate": aggregate, "cases": rows}, indent=2, sort_keys=True))
    print(json.dumps({"output": str(OUT), **aggregate}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
