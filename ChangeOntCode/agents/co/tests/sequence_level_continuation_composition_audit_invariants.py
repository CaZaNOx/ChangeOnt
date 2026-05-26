from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "sequence_level_continuation_composition_audit_v1.json"
REPORT_PATH = ROOT.parent / "SEQUENCE_LEVEL_CONTINUATION_COMPOSITION_AUDIT_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing {JSON_PATH}; run experiments.studies.sequence_level_continuation_composition_audit_v1"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_report_is_claim_bounded() -> None:
    data = _load()
    assert REPORT_PATH.exists()
    text = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not co proof" in text
    assert "not a license" in data.get("claim_boundary", "").lower()
    assert "family-specific" in data.get("claim_boundary", "").lower()


def test_cross_action_memory_and_first_pass_sequence_composition_are_recorded() -> None:
    data = _load()
    assert int(data.get("row_trace_sample_rows", 0)) > 0
    assert int(data.get("cross_action_memory_groups", 0)) > 0
    assert int(data.get("sequence_field_rows", 0)) > 0
    assert int(data.get("sequence_active_rows", 0)) > 0
    findings = {f["id"]: f for f in data.get("audit_findings", [])}
    assert "SLC1_CROSS_ACTION_MEMORY_EXISTS" in findings
    assert "SLC2_SEQUENCE_COMPOSITION_FIRST_PASS_PRESENT" in findings


def test_recommendation_forbids_action_specific_sequence_patch() -> None:
    data = _load()
    rec = data.get("recommendation", "").lower()
    assert "generic" in rec
    assert "family-specific" in rec
    assert "family-specific" in rec


if __name__ == "__main__":
    test_report_is_claim_bounded()
    test_cross_action_memory_and_first_pass_sequence_composition_are_recorded()
    test_recommendation_forbids_action_specific_sequence_patch()
    print("sequence_level_continuation_composition_audit_invariants: PASS")
