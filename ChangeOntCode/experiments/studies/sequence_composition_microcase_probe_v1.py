from __future__ import annotations

"""First-pass sequence-composition microcase probe.

Claim-bounded structural probe: not a benchmark, not CO proof, and not a
family-specific sequence policy.  It validates that public phase transitions can
be composed across steps while negative controls remain protected.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.tests.relation_path_trace_diagnostics import TraceBus, TraceHeader, TraceHeaderState

OUT_JSON = ROOT / "outputs" / "sequence_composition_microcase_probe_v1.json"
REPORT_MD = ROOT.parent / "SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Sequence-composition microcase probe only. It is not a benchmark, not CO proof, "
    "and not a license for family-specific or native-action sequence templates."
)


def _json_safe(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def _effect(operation: str, burden_type: str, *, scope: str = "local", coupling: str = "shared", magnitude: float = 0.72, leakage_status: str = "public") -> Dict[str, Any]:
    return {
        "operation": operation,
        "kind": "burden",
        "burden_type": burden_type,
        "scope": scope,
        "magnitude": magnitude,
        "public_basis": "declared_transition_rule",
        "leakage_status": leakage_status,
        "direction": operation,
        "coupling": coupling,
    }


def _obs(expr: str, effects: List[Dict[str, Any]], *, contradiction: float = 0.30, uncertainty: float = 0.24) -> Dict[str, Any]:
    return {
        "family": "sequence_composition_microcase",
        "action_space": [expr],
        "candidates": [
            {
                "candidate_id": expr,
                "legal": True,
                "visible_delta": 0.56,
                "line_support": 0.56,
                "coverage_adequacy": 0.64,
                "tested_hint": 0.32,
                "uncertainty_hint": uncertainty,
                "reversibility_hint": 0.72,
                "contradiction_hint": contradiction,
                "public_effects": effects,
            }
        ],
    }


def _step(surface: CandidateEvidenceSurface, obs: Dict[str, Any], feedback: Dict[str, Any] | None = None) -> Dict[str, Any]:
    prims = {"signal_bus": TraceBus()}
    surface.step(obs, prims, TraceHeader(TraceHeaderState()), feedback)
    rows = list(prims.get("__candidate_publication_rows__", []))
    return dict(rows[0]) if rows else {}


def _run_pair(case_id: str, first_effects: List[Dict[str, Any]], second_effects: List[Dict[str, Any]], *, enabled: bool = True, expect_active: bool = True) -> Dict[str, Any]:
    surf = CandidateEvidenceSurface(dynamic_shape_enabled=False, sequence_composition_enabled=enabled)
    first = _step(surf, _obs(f"{case_id}_A", first_effects, contradiction=0.52), None)
    second = _step(surf, _obs(f"{case_id}_B", second_effects, contradiction=0.18), {"action": f"{case_id}_A"})
    active = bool(second.get("sequence_composition_active"))
    passed = active is bool(expect_active)
    return {
        "id": case_id,
        "passed": passed,
        "expected_active": bool(expect_active),
        "observed_active": active,
        "first_phase": first.get("continuation_phase"),
        "second_phase": second.get("continuation_phase"),
        "transition": second.get("sequence_phase_transition", ""),
        "support": float(second.get("sequence_composition_support", 0.0) or 0.0),
        "disabled": bool(second.get("sequence_composition_disabled", False)),
    }


def main() -> Dict[str, Any]:
    os.environ["CO_STRICT_ERRORS"] = "1"
    cases = [
        _run_pair("SC1_EXPOSE_TO_RELIEVE", [_effect("reveal", "hiddenness")], [_effect("reduce", "load")], expect_active=True),
        _run_pair("SC2_RELIEVE_TO_STABILIZE", [_effect("reduce", "load")], [_effect("prevent", "load", magnitude=0.20)], expect_active=True),
        _run_pair("SC3_DISABLED_ABLATION", [_effect("reveal", "hiddenness")], [_effect("reduce", "load")], enabled=False, expect_active=False),
        _run_pair("SC4_NONPUBLIC_REJECTED", [_effect("reveal", "hiddenness")], [_effect("reduce", "load", leakage_status="oracle")], expect_active=False),
        _run_pair("SC5_INCOMPATIBLE_DOMAIN_REJECTED", [_effect("reveal", "hiddenness", scope="one", coupling="one")], [_effect("reduce", "load", scope="two", coupling="two")], expect_active=False),
    ]
    passed = sum(1 for c in cases if c["passed"])
    out = {
        "study": "sequence_composition_microcase_probe_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "cases": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "all_passed": passed == len(cases),
        "case_results": cases,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(_json_safe(out), indent=2, sort_keys=True), encoding="utf-8")
    _write_report(out)
    return out


def _write_report(data: Mapping[str, Any]) -> None:
    lines = [
        "# Sequence Composition Microcase Probe v1 — 2026-05-22",
        "",
        "## Claim boundary",
        "",
        CLAIM_BOUNDARY,
        "",
        "## Summary",
        "",
        f"Cases: {data['cases']}; passed: {data['passed']}; failed: {data['failed']}.",
        "",
        "## Cases",
        "",
        "| id | passed | expected active | observed active | phases | transition | support |",
        "|---|---:|---:|---:|---|---|---:|",
    ]
    for c in data.get("case_results", []):
        lines.append(f"| {c['id']} | {int(c['passed'])} | {int(c['expected_active'])} | {int(c['observed_active'])} | {c.get('first_phase')} → {c.get('second_phase')} | {c.get('transition','')} | {float(c.get('support',0.0)):.3f} |")
    lines += [
        "",
        "## Interpretation",
        "",
        "The sequence composer recognizes generic public phase progression across selected feedback and current candidate rows. It does not inspect family names, native action meanings, hidden state, reward hindsight, DP values, or baseline values.",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
