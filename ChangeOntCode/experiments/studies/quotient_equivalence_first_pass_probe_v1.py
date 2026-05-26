from __future__ import annotations

"""Quotient/equivalence first-pass structural probe v1.

This probe executes the invariant cases for the first-pass quotient/equivalence
helper.  It is structural validation only: it does not measure reward, benchmark
performance, or novelty.
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List

from agents.co.tests import quotient_equivalence_first_pass_invariants as inv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "quotient_equivalence_first_pass_probe_v1.json"
REPORT = ROOT.parent / "QUOTIENT_EQUIVALENCE_FIRST_PASS_PROBE_REPORT_2026-05-21.md"

TESTS: List[tuple[str, Callable[[], None]]] = [
    ("different_expressions_same_public_residual_profile_may_quotient", inv.test_different_expressions_same_public_residual_profile_may_quotient),
    ("same_expression_different_burden_regime_does_not_quotient", inv.test_same_expression_different_burden_regime_does_not_quotient),
    ("weak_decision_slot_competition_is_not_quotient_basis", inv.test_weak_decision_slot_competition_is_not_quotient_basis),
    ("same_scalar_score_different_hiddenness_profile_does_not_quotient", inv.test_same_scalar_score_different_hiddenness_profile_does_not_quotient),
    ("hidden_or_solver_like_effects_do_not_derive_quotient", inv.test_hidden_or_solver_like_effects_do_not_derive_quotient),
    ("exclusion_or_rivalry_facts_do_not_quotient_by_themselves", inv.test_exclusion_or_rivalry_facts_do_not_quotient_by_themselves),
    ("quotient_helper_contains_no_problem_family_or_native_action_literals", inv.test_quotient_helper_contains_no_problem_family_or_native_action_literals),
]


def _run_one(name: str, fn: Callable[[], None]) -> Dict[str, Any]:
    try:
        fn()
        return {"case": name, "passed": True, "error": ""}
    except Exception as exc:  # pragma: no cover - diagnostic payload
        return {"case": name, "passed": False, "error": repr(exc)}


def _make_report(result: Dict[str, Any]) -> str:
    return f"""# Quotient / Equivalence First-Pass Probe — 2026-05-21

## Scope

This report validates the first-pass quotient/equivalence helper added for the
rough kernel-completion pass.  It tests conservative quotienting from public
residual profiles while rejecting false quotient cases involving same interface
expression, scalar-score closeness, weak procedural competition, hidden/solver
facts, and rivalry/exclusion facts.

This is structural validation only.  It is not empirical performance evidence,
not proof that quotient tolerance is final, and not a publication-safe novelty
claim.

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
        "study": "quotient_equivalence_first_pass_probe_v1",
        "cases": len(cases),
        "passed": sum(1 for c in cases if c["passed"]),
        "failed": sum(1 for c in cases if not c["passed"]),
        "all_passed": all(c["passed"] for c in cases),
        "claim_boundary": "first-pass structural quotient/equivalence validation only; not final tolerance calibration",
    }
    result = {"study": "quotient_equivalence_first_pass_probe_v1", "summary": summary, "cases": cases}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT.write_text(_make_report(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main()["summary"], indent=2, sort_keys=True))
