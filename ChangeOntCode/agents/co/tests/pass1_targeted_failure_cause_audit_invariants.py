from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUMMARY = ROOT / "outputs" / "pass1_targeted_failure_cause_audit_v1" / "summary.json"
REPORT = ROOT.parent / "PASS1_TARGETED_FAILURE_CAUSE_AUDIT_REPORT_2026-05-25.md"


def test_targeted_failure_cause_audit_outputs_exist_and_are_diagnostic() -> None:
    assert SUMMARY.exists(), "Run experiments.studies.pass1_targeted_failure_cause_audit_v1 first"
    assert REPORT.exists()
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload.get("study") == "pass1_targeted_failure_cause_audit_v1"
    assert "not a tuning run" in payload.get("non_claims", [])
    assert "bandit" in payload and "renewal" in payload and "maintenance" in payload
    assert payload["settings"]["bandit_horizon"] >= 40
    assert payload["settings"]["renewal_horizon"] >= 40
    assert payload["bandit"]["co_regret_mean"] >= 0.0
    assert payload["renewal"]["phase_mean_reward"] >= payload["renewal"]["co_mean_reward"] - 1.0
    assert "middle" in payload["maintenance"]["by_regime"]


def test_report_keeps_no_problem_specific_patch_boundary() -> None:
    text = REPORT.read_text(encoding="utf-8")
    assert "No new kernel mechanism or problem-specific adjustment was made" in text
    assert "not a repair-specific rule" in text
    assert "concept-admission gate" in text
