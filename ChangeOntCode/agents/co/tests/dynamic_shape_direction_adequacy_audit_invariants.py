from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs" / "dynamic_shape_direction_adequacy_audit_v1.json"
REPORT = ROOT.parent / "DYNAMIC_SHAPE_DIRECTION_ADEQUACY_AUDIT_REPORT_2026-05-25.md"


def test_dynamic_shape_direction_audit_outputs_exist() -> None:
    assert OUT.exists(), "run experiments.studies.dynamic_shape_direction_adequacy_audit_v1 first"
    assert REPORT.exists()


def test_dynamic_shape_direction_audit_has_counts_and_boundary() -> None:
    data = json.loads(OUT.read_text(encoding="utf-8"))
    counts = data.get("counts", {})
    assert counts
    assert "not use native family/action rules" in data.get("claim_boundary", "")
    assert data.get("verdict", {}).get("dynamic_shape_direction_not_fully_resolved") is True


def test_report_does_not_claim_optimal_action() -> None:
    text = REPORT.read_text(encoding="utf-8")
    assert "does not assert which action is optimal" in text
    assert "not a missing new concept" in text
