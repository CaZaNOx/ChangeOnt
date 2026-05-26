from __future__ import annotations

"""Relation-path trace validation study.

This is a forensic diagnostic, not a reward benchmark.  It compares identical
adapter observations with public_effects present vs stripped, then records
whether kernel-side RelationSurface-derived topology changes RCF field outputs
and whether that reaches commitment/readout.
"""

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

from agents.co.tests.relation_path_trace_diagnostics import trace_all_cases

OUT = Path("outputs/relation_path_trace_v1.json")


def main() -> None:
    cases: List[Dict[str, Any]] = trace_all_cases()
    rel_types: Counter = Counter()
    for case in cases:
        rel_types.update({str(k): int(v) for k, v in dict(case.get("relations_by_type", {}) or {}).items()})
    aggregate = {
        "cases": len(cases),
        "candidate_rows": sum(int(c.get("candidate_rows", 0) or 0) for c in cases),
        "relations_total": sum(int(c.get("relations_total", 0) or 0) for c in cases),
        "non_rival_relations": sum(int(c.get("non_rival_relations", 0) or 0) for c in cases),
        "field_delta_positive_cases": sum(1 for c in cases if float(c.get("field_delta_l1", 0.0) or 0.0) > 0.01),
        "commitment_action_changed_cases": sum(1 for c in cases if bool(c.get("commitment_action_changed"))),
        "commitment_mode_changed_cases": sum(1 for c in cases if bool(c.get("commitment_mode_changed"))),
        "relations_by_type": dict(sorted(rel_types.items())),
    }
    payload = {
        "diagnostic_scope": "relation_path_trace_v1",
        "claim_boundary": "coverage/field-effect diagnostic only; not reward evidence and not full collapse-certificate validation",
        "aggregate": aggregate,
        "cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"output": str(OUT), **aggregate}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
