from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "context_conditioned_expectation_audit_v1.json"
REPORT_PATH = ROOT.parent / "CONTEXT_CONDITIONED_EXPECTATION_AUDIT_REPORT_2026-05-25.md"


def _load() -> dict:
    assert JSON_PATH.exists(), "run experiments.studies.context_conditioned_expectation_audit_v1 first"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_context_conditioned_audit_exists_and_is_claim_bounded() -> None:
    data = _load()
    assert data["study"] == "context_conditioned_expectation_audit_v1"
    assert data["verdict"]["aggregate_action_counts_were_insufficient"] is True
    assert data["verdict"]["context_conditioning_added"] is True
    assert data["verdict"]["kernel_change_made"] is False
    assert "not a benchmark" in data["claim_boundary"].lower()
    assert REPORT_PATH.exists()
    assert "aggregate ablation counts are too naive" in REPORT_PATH.read_text(encoding="utf-8").lower()


def test_mechanism_counts_have_expected_shape() -> None:
    data = _load()
    assert int(data["full_current_steps"]) > 0
    for mech in ("dynamic_shape", "sequence", "quotient", "recursion"):
        assert mech in data["mechanism_counts"]
        counts = data["mechanism_counts"][mech]
        total = int(counts.get("expected_none", 0)) + int(counts.get("expected_weak", 0)) + int(counts.get("expected_strong", 0))
        assert total == int(data["full_current_steps"])
    assert "carrier_plus_resolver" in data["context_bucket_counts"] or "sequence_present" in data["context_bucket_counts"]


def test_findings_preserve_no_tuning_boundary() -> None:
    data = _load()
    assert len(data.get("findings", [])) >= 4
    next_text = "\n".join(f.get("next_action", "") for f in data["findings"]).lower()
    assert "readout" in data["verdict"]["next_recommended_step"].lower()
    assert "tune" not in next_text
    assert "family-specific" in data["claim_boundary"].lower() or "family-specific" in REPORT_PATH.read_text(encoding="utf-8").lower()


if __name__ == "__main__":
    test_context_conditioned_audit_exists_and_is_claim_bounded()
    test_mechanism_counts_have_expected_shape()
    test_findings_preserve_no_tuning_boundary()
    print("context_conditioned_expectation_audit_invariants: PASS")
