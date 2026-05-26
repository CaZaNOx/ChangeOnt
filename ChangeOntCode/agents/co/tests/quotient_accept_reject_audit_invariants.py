from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "quotient_accept_reject_audit_v1.json"
REPORT_PATH = ROOT.parent / "QUOTIENT_ACCEPT_REJECT_AUDIT_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing {JSON_PATH}"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_report_and_json_exist_and_are_claim_bounded() -> None:
    data = _load()
    assert REPORT_PATH.exists()
    text = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not benchmark evidence" in text
    assert "not a co proof" in text
    assert "not a final quotient law" in data.get("claim_boundary", "").lower()


def test_quotient_provenance_is_visible() -> None:
    data = _load()
    findings = {f["id"]: f for f in data.get("audit_findings", [])}
    assert findings.get("QAR1_PROVENANCE_NOW_VISIBLE", {}).get("severity") == "resolved-watchpoint"
    assert int(data.get("accepted_profiles_total", 0)) > 0
    assert "task_summary" in data and data["task_summary"]


def test_no_duplicate_signature_bug_detected_in_capped_trace() -> None:
    data = _load()
    assert int(data.get("duplicate_signature_bug_count", -1)) == 0
    findings = {f["id"]: f for f in data.get("audit_findings", [])}
    assert findings.get("QAR2_NO_DUPLICATE_SIGNATURE_MISSED_QUOTIENT_FOUND", {}).get("severity") == "passed-check"


if __name__ == "__main__":
    test_report_and_json_exist_and_are_claim_bounded()
    test_quotient_provenance_is_visible()
    test_no_duplicate_signature_bug_detected_in_capped_trace()
    print("quotient_accept_reject_audit_invariants: PASS")
