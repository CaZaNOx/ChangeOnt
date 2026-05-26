from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "generic_readout_swamping_trace_audit_v1.json"
REPORT_PATH = ROOT.parent / "GENERIC_READOUT_SWAMPING_TRACE_AUDIT_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing {JSON_PATH}; run experiments.studies.generic_readout_swamping_trace_audit_v1"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_report_is_claim_bounded() -> None:
    data = _load()
    assert REPORT_PATH.exists()
    text = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not co proof" in text
    assert "not a benchmark" in text
    assert "family-specific" in data.get("claim_boundary", "").lower()


def test_swamping_trace_metrics_exist() -> None:
    data = _load()
    ov = data.get("overall", {})
    assert int(data.get("full_current_steps", 0)) > 0
    assert "avg_support_stability_field_share" in ov
    assert "avg_penalty_ratio" in ov
    assert "carrier_with_resolver_alt_steps" in ov
    assert isinstance(data.get("by_family_mode", {}), dict)


def test_findings_are_generic_not_family_patch() -> None:
    data = _load()
    findings = {f["id"]: f for f in data.get("audit_findings", [])}
    assert findings.get("GRS1_READOUT_SWAMPING_REMAINS_GENERIC_WATCHPOINT", {}).get("severity") == "medium"
    rec = data.get("recommendation", "").lower()
    assert "family-specific" in rec
    assert "generic" in rec
    assert "sequence-composition" in rec


if __name__ == "__main__":
    test_report_is_claim_bounded()
    test_swamping_trace_metrics_exist()
    test_findings_are_generic_not_family_patch()
    print("generic_readout_swamping_trace_audit_invariants: PASS")
