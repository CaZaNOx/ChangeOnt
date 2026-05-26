from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs" / "maintenance_dynamic_shape_resolution_audit_v1.json"
REPORT = ROOT.parent / "MAINTENANCE_DYNAMIC_SHAPE_RESOLUTION_AUDIT_REPORT_2026-05-25.md"


def test_maintenance_dynamic_shape_resolution_audit_outputs_exist() -> None:
    assert OUT.exists(), "run experiments.studies.maintenance_dynamic_shape_resolution_audit_v1 first"
    assert REPORT.exists()


def test_maintenance_dynamic_shape_resolution_audit_has_claim_boundary_and_counts() -> None:
    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert "does not assert an optimal maintenance action" in data.get("claim_boundary", "")
    assert data.get("total_maintenance_full_steps", 0) > 0
    assert data.get("counts", {}).get("total_classified_steps", 0) == data.get("total_maintenance_full_steps", 0)
    assert data.get("verdict", {}).get("maintenance_specific_tuning_justified") is False


def test_report_does_not_license_tuning_or_claim_failure() -> None:
    text = REPORT.read_text(encoding="utf-8")
    assert "does not justify a maintenance-specific rule" in text
    assert "not caused by DynamicShapeField absence" in text
    assert "generic cross-family microcases" in text
