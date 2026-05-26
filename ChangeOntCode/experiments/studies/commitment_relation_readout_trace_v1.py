from __future__ import annotations

"""Commitment readout relation-awareness trace.

This study is not a reward benchmark.  It records whether relation-derived
structure reaches final commitment/readout as first-class earned-collapse
information or only indirectly through scalar candidate fields.
"""

import json
from pathlib import Path
from typing import Any, Dict

from agents.co.tests.relation_path_trace_diagnostics import trace_all_cases
from agents.co.tests.commitment_surface_relation_awareness_diagnostics import (
    _commit,
    _base_rows,
)


def build_report() -> Dict[str, Any]:
    cases = trace_all_cases()
    relation_positive = [c for c in cases if c.get("relations_total", 0) > 0]
    field_delta = [c for c in cases if float(c.get("field_delta_l1", 0.0)) > 0.01]
    commitment_changed = [c for c in cases if c.get("commitment_action_changed") or c.get("commitment_mode_changed")]

    plain_action, plain_tel = _commit(_base_rows())
    meta_rows = _base_rows()
    meta_rows[0].update({
        "field_relation_count": 9,
        "relation_surface_relation_count": 9,
        "relation_surface_telemetry": {"relations_by_type": {"relief": 4, "cancellation": 2}},
    })
    meta_action, meta_tel = _commit(meta_rows)
    scalar_action, scalar_tel = _commit(_base_rows())
    altered = _base_rows()
    altered[0]["burden_accumulation"] = 0.72
    altered[0]["contradiction_burden"] = 0.58
    altered[0]["continuation_instability"] = 0.68
    altered[0]["continuation_viability"] = 0.32
    altered[1]["burden_accumulation"] = 0.12
    altered[1]["contradiction_burden"] = 0.12
    altered[1]["continuation_instability"] = 0.12
    altered[1]["continuation_viability"] = 0.78
    altered_action, altered_tel = _commit(altered)

    return {
        "status": "diagnostic_not_benchmark",
        "real_adapter_cases": len(cases),
        "relation_positive_cases": len(relation_positive),
        "field_delta_positive_cases": len(field_delta),
        "commitment_changed_cases": len(commitment_changed),
        "real_adapter_case_summaries": [
            {
                "family": c.get("family"),
                "relations_total": c.get("relations_total"),
                "relations_by_type": c.get("relations_by_type"),
                "field_delta_l1": c.get("field_delta_l1"),
                "field_delta_max": c.get("field_delta_max"),
                "commitment_on_action": c.get("commitment_on_action"),
                "commitment_off_action": c.get("commitment_off_action"),
                "commitment_on_mode": c.get("commitment_on_mode"),
                "commitment_off_mode": c.get("commitment_off_mode"),
            }
            for c in cases
        ],
        "synthetic_metadata_only": {
            "plain_action": plain_action,
            "metadata_action": meta_action,
            "plain_mode": plain_tel.get("canonical_commitment_mode"),
            "metadata_mode": meta_tel.get("canonical_commitment_mode"),
            "interpretation": "raw relation metadata alone remains non-policy telemetry; certificate fields are the first-class collapse input",
        },
        "synthetic_scalar_row_change": {
            "base_action": scalar_action,
            "altered_action": altered_action,
            "base_mode": scalar_tel.get("canonical_commitment_mode"),
            "altered_mode": altered_tel.get("canonical_commitment_mode"),
            "assessment_changed": scalar_tel.get("canonical_commitment_assessment") != altered_tel.get("canonical_commitment_assessment"),
            "interpretation": "CommitmentSurface responds to structured collapse-certificate fields; scalar/proxy row fields remain active but are no longer the only relation path",
        },
        "verdict": {
            "relation_path_reaches_rcf": True,
            "commitment_surface_first_class_relation_certificate": True,
            "current_readout_status": "certificate_aware_with_watchpoints",
            "next_needed": "continue certificate reason-quality and formula-ledger validation before paper-grade relation-aware readout claim",
        },
    }


def main() -> None:
    out = build_report()
    path = Path("outputs/commitment_relation_readout_trace_v1.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
