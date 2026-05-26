from __future__ import annotations

"""Invariants for the current-kernel watchpoint/hardening audit artifact.

These checks ensure the audit exists, remains claim-bounded, and records that the
prior dynamic-shape/readout and recursion-provenance watchpoints were hardened
without converting the diagnostic into evidence/proof.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "current_kernel_watchpoint_audit_v1.json"
REPORT_PATH = ROOT.parent / "CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing audit output {JSON_PATH}"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_audit_report_and_json_exist() -> None:
    assert JSON_PATH.exists()
    assert REPORT_PATH.exists()
    report = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not benchmark evidence" in report
    assert "not co proof" in report


def test_hardened_watchpoints_are_recorded() -> None:
    data = _load()
    findings = {f["id"]: f for f in data.get("audit_findings", [])}
    assert findings.get("HF1_DYNAMIC_SHAPE_NOW_READOUT_VISIBLE", {}).get("severity") == "resolved-watchpoint"
    assert findings.get("HF2_RECURSION_PROVENANCE_SPLIT", {}).get("severity") == "resolved-watchpoint"
    assert int(data.get("dynamic_controls_commitment_steps", 0)) > 0
    assert int(data.get("weak_only_high_recursion_count", -1)) == 0
    assert "structural" in findings["HF2_RECURSION_PROVENANCE_SPLIT"]["finding"].lower()


def test_remaining_watchpoints_are_narrower_and_not_robot_ready() -> None:
    data = _load()
    recommendation = str(data.get("recommendation", "")).lower()
    assert "do not add robot/simulation yet" in recommendation
    assert "quotient" in recommendation
    assert "maintenance" in recommendation
    findings = {f["id"]: f for f in data.get("audit_findings", [])}
    assert findings.get("WF3_QUOTIENT_CONSERVATIVE_BUT_UNAUDITED_FOR_MISSES", {}).get("severity") == "medium"
    assert findings.get("WF4_MAINTENANCE_ACTION_INSENSITIVITY_REMAINS", {}).get("severity") == "medium"


if __name__ == "__main__":
    test_audit_report_and_json_exist()
    test_hardened_watchpoints_are_recorded()
    test_remaining_watchpoints_are_narrower_and_not_robot_ready()
    print("current_kernel_watchpoint_audit_invariants: PASS")
