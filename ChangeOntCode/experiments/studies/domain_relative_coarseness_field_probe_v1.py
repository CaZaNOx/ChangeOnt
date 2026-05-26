"""Probe bounded domain-relative coarseness field behavior.

Run with: python -m experiments.studies.domain_relative_coarseness_field_probe_v1
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from agents.co.runtime.surfaces.dynamic_shape_field import DynamicShapeField
from agents.co.runtime.surfaces.relation_surface import derive_relation_surface

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "domain_relative_coarseness_field_probe_v1.json"

CONTROLS = {
    "local_authority": 0.50,
    "path_sensitivity": 0.50,
    "contradiction_sensitivity": 0.50,
    "collapse_admissibility": 0.50,
    "dynamic_shape_coarsening": 0.20,
    "dynamic_shape_urgency": 0.15,
}


def effect(operation: str, burden_type: str, magnitude: float) -> Dict[str, Any]:
    return {
        "effect_id": f"{operation}_{burden_type}_{magnitude}",
        "kind": "burden",
        "operation": operation,
        "burden_type": burden_type,
        "scope": "public_domain",
        "magnitude": magnitude,
        "public_basis": "visible_observation",
        "leakage_status": "public",
    }


def row(name: str, effects: List[Dict[str, Any]], *, uncertainty: float = 0.0, debt: float = 0.0) -> Dict[str, Any]:
    return {
        "action": name,
        "candidate_id": name,
        "support_mass": 0.5,
        "local_support": 0.5,
        "decision_state": 0.5,
        "continuation_viability": 0.5,
        "stability_under_change": 0.5,
        "uncertainty": uncertainty,
        "field_debt": debt,
        "public_effects": effects,
    }


def run_case(name: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = derive_relation_surface(rows, CONTROLS)
    field = DynamicShapeField(alpha=0.75)
    update = field.update(rows=result.rows, relations=result.relations)
    state = field.state_dict()
    return {
        "case": name,
        "relation_surface_telemetry": result.telemetry,
        "update_evidence": update.get("public_evidence", {}),
        "coarseness_radius": state.get("coarseness_radius"),
        "coarseness_by_domain": state.get("coarseness_by_domain", {}),
        "rows": [
            {
                "action": r.get("action"),
                "domain": r.get("relation_field_domain"),
                "concentration": r.get("relation_field_concentration"),
                "ambiguity": r.get("relation_field_ambiguity"),
                "function_like": r.get("relation_field_function_like"),
                "domain_coarseness": field.domain_coarseness_for(r.get("relation_field_domain", "")),
            }
            for r in result.rows
        ],
    }


def main() -> None:
    cases = [
        run_case(
            "ambiguous_hiddenness_vs_concentrated_degradation",
            [
                row("hidden_a", [effect("carry", "hiddenness", 0.50)], uncertainty=0.80, debt=0.30),
                row("hidden_b", [effect("carry", "hiddenness", 0.50)], uncertainty=0.75, debt=0.35),
                row("degrade_resolve", [effect("relieve", "degradation", 0.92)], debt=0.05),
                row("degrade_minor", [effect("carry", "degradation", 0.08)], debt=0.05),
            ],
        ),
        run_case(
            "single_public_domain_fallback",
            [
                row("target_dom", [effect("carry", "target", 0.98)]),
                row("target_minor", [effect("carry", "target", 0.02)]),
            ],
        ),
    ]
    summary = {
        "study": "domain_relative_coarseness_field_probe_v1",
        "cases": len(cases),
        "domain_divergence_observed": any(len(c.get("coarseness_by_domain", {})) > 1 and len(set(round(v, 6) for v in c["coarseness_by_domain"].values())) > 1 for c in cases),
        "all_cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
