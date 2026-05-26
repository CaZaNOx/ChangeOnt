from __future__ import annotations

"""DynamicShapeField microcase probe v1.

This probe executes the pre-implementation expectations from docs 103/104
against the first-pass DynamicShapeField.  It is structural validation only: no
reward claim, no benchmark claim, and no CO proof.
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List

from agents.co.tests import dynamic_shape_field_invariants as inv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "dynamic_shape_microcase_probe_v1.json"
REPORT = ROOT.parent / "DYNAMIC_SHAPE_MICROCASE_PROBE_REPORT_2026-05-21.md"

TESTS: List[tuple[str, Callable[[], None]]] = [
    ("repeated_carrier_burden", inv.test_repeated_carrier_burden_increases_persistence_and_shortens_projection),
    ("successful_exposure", inv.test_successful_exposure_reduces_hiddenness_and_can_raise_confidence),
    ("failed_exposure", inv.test_failed_exposure_does_not_invent_knowledge),
    ("topology_discovery", inv.test_topology_discovery_updates_known_admissibility_not_topology),
    ("stable_low_coupling_coarsening", inv.test_stable_low_coupling_permits_coarsening),
    ("high_coupling_projection_consumption", inv.test_high_coupling_consumes_projection_and_narrows_coarseness),
    ("resolver_requires_public_relation", inv.test_resolver_relation_requires_explicit_public_relation),
    ("transform_transfer_nonresolver", inv.test_transform_transfer_not_resolution_by_itself),
    ("revision_success", inv.test_revision_success_lowers_revision_pressure_via_public_feedback),
    ("failed_revision", inv.test_failed_revision_raises_narrowing_pressure),
    ("reward_alone_no_update", inv.test_reward_alone_does_not_update_shape),
    ("shape_ablation_visible", inv.test_shape_update_ablation_visible_in_candidate_surface),
]


def _run_one(name: str, fn: Callable[[], None]) -> Dict[str, Any]:
    try:
        fn()
        return {"case": name, "passed": True, "error": ""}
    except Exception as exc:  # pragma: no cover - diagnostic payload
        return {"case": name, "passed": False, "error": repr(exc)}


def _make_report(result: Dict[str, Any]) -> str:
    return f"""# DynamicShapeField Microcase Probe — 2026-05-21

## Scope

This report validates the first-pass persistent `DynamicShapeField` against the
microcase expectations in docs `103_DYNAMIC_SHAPE_FIELD_CONTRACT.md` and
`104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md`.

It is structural validation only.  It is not reward evidence, not benchmark
evidence, not a novelty claim, and not proof of CO.

## Summary

```json
{json.dumps(result['summary'], indent=2, sort_keys=True)}
```

## Case outcomes

```json
{json.dumps(result['cases'], indent=2, sort_keys=True)}
```
"""


def main() -> Dict[str, Any]:
    cases = [_run_one(name, fn) for name, fn in TESTS]
    summary = {
        "study": "dynamic_shape_microcase_probe_v1",
        "cases": len(cases),
        "passed": sum(1 for c in cases if c["passed"]),
        "failed": sum(1 for c in cases if not c["passed"]),
        "all_passed": all(c["passed"] for c in cases),
        "claim_boundary": "structural microcases only; not empirical performance evidence",
    }
    result = {"study": "dynamic_shape_microcase_probe_v1", "summary": summary, "cases": cases}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT.write_text(_make_report(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main()["summary"], indent=2, sort_keys=True))
