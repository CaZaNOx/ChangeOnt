from __future__ import annotations

"""Invariants for DynamicShapeField suspicious-case investigation."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs" / "dynamic_shape_suspicious_case_investigation_v1.json"
REPORT = ROOT.parent / "DYNAMIC_SHAPE_SUSPICIOUS_CASE_INVESTIGATION_REPORT_2026-05-25.md"


def test_dynamic_shape_suspicious_case_investigation_outputs_exist() -> None:
    assert OUT.exists(), "run experiments.studies.dynamic_shape_suspicious_case_investigation_v1 first"
    assert REPORT.exists()


def test_prior_suspicious_cases_are_explained_or_retained_as_residual() -> None:
    data = json.loads(OUT.read_text(encoding="utf-8"))
    prior = int(data.get("prior_suspicious_cases", 0))
    counts = data.get("investigation_counts", {})
    assert prior > 0
    assert sum(int(v) for v in counts.values()) == prior
    # The audit must distinguish at least score-effect or classifier-overreach
    # from true residual non-effects, rather than restating the old suspicious count.
    assert any(
        key in counts
        for key in (
            "readout_score_effect_not_counted_by_prior_audit",
            "hidden_action_effect_detected_by_top_rank",
            "prior_classifier_overreach_refined_to_weak",
            "prior_classifier_overreach_refined_to_none",
        )
    )


def test_report_preserves_claim_boundary() -> None:
    text = REPORT.read_text(encoding="utf-8")
    assert "not a kernel change" in text
    assert "not a tuning license" in text
    assert "does not prove DynamicShapeField is adequate" in text
