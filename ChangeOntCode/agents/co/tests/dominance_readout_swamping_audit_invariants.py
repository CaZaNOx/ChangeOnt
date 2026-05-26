from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "dominance_readout_swamping_audit_v1.json"
REPORT_PATH = ROOT.parent / "DOMINANCE_READOUT_SWAMPING_AUDIT_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing {JSON_PATH}; run experiments.studies.dominance_readout_swamping_audit_v1"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_report_is_claim_bounded() -> None:
    data = _load()
    assert REPORT_PATH.exists()
    txt = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not a benchmark" in txt
    assert "not tuning evidence" in txt
    assert "not co proof" in txt
    assert "not maintenance-specific" in data.get("claim_boundary", "").lower()


def test_audit_records_gate_failures_and_mass_decomposition() -> None:
    data = _load()
    assert "gate_failure_counts" in data
    assert "avg_support_stability_field_share" in data
    assert "avg_dominance_penalty_ratio" in data
    assert isinstance(data.get("sample_cases", []), list)
    if data.get("sample_cases"):
        sample = data["sample_cases"][0]
        assert "support_stability_field_share_of_positive_mass" in sample
        assert "dominance_penalty_to_positive_mass_ratio" in sample


def test_recommendation_forbids_family_tuning() -> None:
    data = _load()
    rec = data.get("recommendation", "").lower()
    assert "do not tune" in rec or "do not treat" in rec
    assert "family" in rec
    assert "generic" in rec


def test_microcase_summary_is_embedded() -> None:
    data = _load()
    summary = data.get("microcase_summary", {})
    assert int(summary.get("cases", 0)) >= 4
    assert "watchpoints" in summary
    assert int(summary.get("watchpoints", 0)) == 0


if __name__ == "__main__":
    test_report_is_claim_bounded()
    test_audit_records_gate_failures_and_mass_decomposition()
    test_recommendation_forbids_family_tuning()
    test_microcase_summary_is_embedded()
    print("dominance_readout_swamping_audit_invariants: PASS")
