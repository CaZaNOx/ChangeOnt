from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "maintenance_action_insensitivity_audit_v1.json"
REPORT_PATH = ROOT.parent / "MAINTENANCE_ACTION_INSENSITIVITY_AUDIT_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing {JSON_PATH}"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_report_and_json_exist_and_are_claim_bounded() -> None:
    data = _load()
    assert REPORT_PATH.exists()
    text = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not a maintenance benchmark" in text
    assert "not co proof" in text
    assert "not a tuning justification" in data.get("claim_boundary", "").lower()


def test_action_insensitivity_is_recorded_without_tuning_license() -> None:
    data = _load()
    findings = {f["id"]: f for f in data.get("audit_findings", [])}
    assert findings.get("MAI1_ABLATION_ACTION_INSENSITIVITY_CONFIRMED", {}).get("severity") == "medium"
    assert "do not tune maintenance" in data.get("recommendation", "").lower()
    assert int(data.get("insensitive_comparison_count", 0)) >= 1


def test_mode_summary_contains_dominance_and_resolver_counts() -> None:
    data = _load()
    rows = {r["mode"]: r for r in data.get("mode_summary", [])}
    assert "middle" in rows
    assert "renewal_like" in rows
    for row in rows.values():
        assert "avg_selected_dominance_gap" in row
        assert "selected_run_with_carrier_and_resolver_alt" in row


if __name__ == "__main__":
    test_report_and_json_exist_and_are_claim_bounded()
    test_action_insensitivity_is_recorded_without_tuning_license()
    test_mode_summary_contains_dominance_and_resolver_counts()
    print("maintenance_action_insensitivity_audit_invariants: PASS")
