from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT / "outputs" / "sequence_composition_microcase_probe_v1.json"
REPORT_PATH = ROOT.parent / "SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md"


def _load() -> dict:
    assert JSON_PATH.exists(), f"missing {JSON_PATH}; run experiments.studies.sequence_composition_microcase_probe_v1"
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_probe_is_claim_bounded() -> None:
    data = _load()
    assert REPORT_PATH.exists()
    text = REPORT_PATH.read_text(encoding="utf-8").lower()
    assert "not a benchmark" in data.get("claim_boundary", "").lower()
    assert "not co proof" in data.get("claim_boundary", "").lower()
    assert "family-specific" in data.get("claim_boundary", "").lower()
    assert "hidden state" in text


def test_positive_and_negative_controls_pass() -> None:
    data = _load()
    assert data.get("all_passed") is True, data
    rows = {r["id"]: r for r in data.get("case_results", [])}
    assert rows["SC1_EXPOSE_TO_RELIEVE"]["observed_active"] is True
    assert rows["SC2_RELIEVE_TO_STABILIZE"]["observed_active"] is True
    for cid in ("SC3_DISABLED_ABLATION", "SC4_NONPUBLIC_REJECTED", "SC5_INCOMPATIBLE_DOMAIN_REJECTED"):
        assert rows[cid]["observed_active"] is False, rows[cid]


if __name__ == "__main__":
    test_probe_is_claim_bounded()
    test_positive_and_negative_controls_pass()
    print("sequence_composition_microcase_probe_invariants: PASS")
