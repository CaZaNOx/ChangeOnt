"""Probe relation-field concentration / function-like collapse telemetry.

Run with: python -m experiments.studies.relation_field_function_like_probe_v1
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from agents.co.runtime.surfaces.relation_surface import derive_relation_surface
from agents.co.runtime.surfaces.dynamic_shape_field import DynamicShapeField

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "relation_field_function_like_probe_v1.json"

CONTROLS = {
    "local_authority": 0.50,
    "path_sensitivity": 0.50,
    "contradiction_sensitivity": 0.50,
    "collapse_admissibility": 0.50,
    "dynamic_shape_coarsening": 0.20,
    "dynamic_shape_urgency": 0.15,
}


def effect(operation: str, burden_type: str = "target", magnitude: float = 1.0) -> Dict[str, Any]:
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


def row(name: str, effects: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "action": name,
        "candidate_id": name,
        "support_mass": 0.5,
        "local_support": 0.5,
        "decision_state": 0.5,
        "continuation_viability": 0.5,
        "stability_under_change": 0.5,
        "public_effects": effects,
    }


def run_case(name: str, rows: List[Dict[str, Any]], controls: Dict[str, Any]) -> Dict[str, Any]:
    result = derive_relation_surface(rows, controls)
    field = DynamicShapeField(alpha=0.60)
    update = field.update(rows=result.rows, relations=result.relations)
    return {
        "case": name,
        "telemetry": result.telemetry,
        "rows": [
            {
                "action": r.get("action"),
                "domain": r.get("relation_field_domain"),
                "concentration": r.get("relation_field_concentration"),
                "ambiguity": r.get("relation_field_ambiguity"),
                "threshold": r.get("relation_field_function_like_threshold"),
                "function_like": r.get("relation_field_function_like"),
                "dominant_operation_class": r.get("relation_field_dominant_operation_class"),
            }
            for r in result.rows
        ],
        "shape_update_evidence": update.get("public_evidence", {}),
        "shape_state_after": field.state_dict(),
    }


def main() -> None:
    cases = [
        run_case("highly_concentrated_function_like", [row("dominant", [effect("carry", magnitude=0.999)]), row("tiny", [effect("carry", magnitude=0.001)])], CONTROLS),
        run_case("flat_ambiguous_relation", [row("a", [effect("carry", magnitude=0.50)]), row("b", [effect("carry", magnitude=0.50)])], CONTROLS),
        run_case("shape_coarse_allows_borderline_collapse", [row("dominant", [effect("carry", magnitude=0.78)]), row("minor", [effect("carry", magnitude=0.22)])], {**CONTROLS, "dynamic_shape_coarsening": 0.90, "collapse_admissibility": 0.80, "dynamic_shape_urgency": 0.0}),
        run_case("shape_urgent_keeps_borderline_open", [row("dominant", [effect("carry", magnitude=0.78)]), row("minor", [effect("carry", magnitude=0.22)])], {**CONTROLS, "dynamic_shape_coarsening": 0.0, "collapse_admissibility": 0.20, "dynamic_shape_urgency": 0.80}),
    ]
    summary = {
        "study": "relation_field_function_like_probe_v1",
        "cases": len(cases),
        "function_like_cases": sum(1 for c in cases if any(r.get("function_like") for r in c["rows"])),
        "ambiguous_cases": sum(1 for c in cases if c["telemetry"].get("relation_field_ambiguous_count", 0) > 0),
        "all_cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
