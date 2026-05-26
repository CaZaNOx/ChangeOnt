from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "preblocking_resolver_cross_family_microcase_probe_v1.json"
REPORT_PATH = ROOT.parent / "PREBLOCKING_RESOLVER_CROSS_FAMILY_MICROCASE_PROBE_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing {JSON_PATH}; run experiments.studies.preblocking_resolver_cross_family_microcase_probe_v1"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_report_is_claim_bounded_and_generic() -> None:
    data = _load()
    assert REPORT_PATH.exists()
    txt = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not maintenance tuning" in txt
    assert "not co proof" in txt
    assert "hidden state" in txt
    assert "family names" in txt or "family labels" in txt
    assert "not a benchmark" in data.get("claim_boundary", "").lower()


def test_negative_controls_are_protected() -> None:
    data = _load()
    rows = {r["id"]: r for r in data.get("case_results", [])}
    for case_id in ("PB4_LOW_URGENCY_NO_TRIGGER", "PB5_WEAK_RESOLVER_NO_TRIGGER", "PB6_LARGE_CARRIER_ADVANTAGE_NO_TRIGGER"):
        assert rows[case_id]["status"] == "passed", f"negative control failed: {case_id} -> {rows[case_id]}"
        assert rows[case_id]["shape_gauged_resolver_timing_applied"] is False


def test_positive_high_urgency_case_triggers() -> None:
    data = _load()
    rows = {r["id"]: r for r in data.get("case_results", [])}
    assert rows["PB1_HIGH_URGENCY_HIGH_CARRIER_TRIGGERS"]["status"] == "passed"
    assert rows["PB1_HIGH_URGENCY_HIGH_CARRIER_TRIGGERS"]["selected"] == "RESOLVE_CONTINUATION"


def test_borderline_case_triggers_after_generic_carrier_gate_calibration() -> None:
    data = _load()
    rows = {r["id"]: r for r in data.get("case_results", [])}
    pb2 = rows["PB2_HIGH_URGENCY_BORDERLINE_CARRIER_AUDIT"]
    assert pb2["status"] == "passed"
    assert pb2["selected"] == "RESOLVE_CONTINUATION"
    assert pb2["shape_gauged_resolver_timing_applied"] is True
    finding = {f["id"]: f for f in data.get("audit_findings", [])}.get("PB_AUDIT_CARRIER_GATE_BORDERLINE")
    assert finding is not None
    assert "generic" in finding.get("next_action", "").lower()
    assert "family-specific" in finding.get("next_action", "").lower()


if __name__ == "__main__":
    test_report_is_claim_bounded_and_generic()
    test_negative_controls_are_protected()
    test_positive_high_urgency_case_triggers()
    test_borderline_case_triggers_after_generic_carrier_gate_calibration()
    print("preblocking_resolver_cross_family_microcase_invariants: PASS")
