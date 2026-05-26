from __future__ import annotations

"""Multi-step continuation-identity probe v1.

This structural probe verifies the first-pass continuity-memory patch: different
native action expressions that operate on the same public burden domain can share
continuation memory without collapsing RelationSurface branch IDs into one row.
It is not performance evidence and not a final multi-step planning mechanism.
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List

from agents.co.tests import multi_step_continuation_identity_invariants as inv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "multi_step_continuation_identity_probe_v1.json"
REPORT = ROOT.parent / "MULTI_STEP_CONTINUATION_IDENTITY_PROBE_REPORT_2026-05-21.md"

TESTS: List[tuple[str, Callable[[], None]]] = [
    ("public_burden_domain_persists_across_action_expressions", inv.test_public_burden_domain_persists_across_action_expressions),
    ("distinct_public_burden_domains_do_not_merge", inv.test_distinct_public_burden_domains_do_not_merge),
    ("batch_tracker_updates_shared_memory_once_per_step", inv.test_batch_tracker_updates_shared_memory_once_per_step),
    ("candidate_surface_memory_crosses_actions_without_branch_collapse", inv.test_candidate_surface_memory_can_cross_actions_without_collapsing_branch_ids),
    ("action_fallback_last_resort", inv.test_action_fallback_remains_last_resort_only),
]


def _run_one(name: str, fn: Callable[[], None]) -> Dict[str, Any]:
    try:
        fn()
        return {"case": name, "passed": True, "error": ""}
    except Exception as exc:  # pragma: no cover - diagnostic payload
        return {"case": name, "passed": False, "error": repr(exc)}


def _make_report(result: Dict[str, Any]) -> str:
    return f"""# Multi-Step Continuation Identity Probe — 2026-05-21

## Scope

This report validates the first-pass continuation-memory update.  It tests that
candidate publication can retain a continuation-memory key across different
native action expressions when they operate on the same public burden domain,
while RelationSurface branch IDs remain distinct where the current action
expressions/effects are distinct.

This is structural validation only.  It is not reward evidence, not a planning
claim, not a robot/simulation result, and not final proof of the branch≠action
doctrine.

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
        "study": "multi_step_continuation_identity_probe_v1",
        "cases": len(cases),
        "passed": sum(1 for c in cases if c["passed"]),
        "failed": sum(1 for c in cases if not c["passed"]),
        "all_passed": all(c["passed"] for c in cases),
        "claim_boundary": "first-pass structural continuation-memory validation only; not final multi-step branch identity",
    }
    result = {"study": "multi_step_continuation_identity_probe_v1", "summary": summary, "cases": cases}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT.write_text(_make_report(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main()["summary"], indent=2, sort_keys=True))
