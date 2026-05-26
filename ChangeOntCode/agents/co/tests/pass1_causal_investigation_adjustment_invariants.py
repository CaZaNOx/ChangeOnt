from __future__ import annotations

import json
from pathlib import Path

from experiments.studies.pass1_causal_investigation_adjustment_v1 import build_summary, main

ROOT = Path(__file__).resolve().parents[3]


def test_causal_investigation_adjustment_reports_safe_generic_fix() -> None:
    summary = build_summary()
    adj = summary["adjustment_applied"]
    assert adj["kind"] == "public_contract_vocabulary_normalization"
    assert summary["diagnosis"]["performance_tuning_justified"] is False
    assert summary["diagnosis"]["new_kernel_mechanism_justified"] is False
    assert summary["diagnosis"]["safe_generic_fix_found"] is True
    joined = "\n".join(adj["guardrails"])
    forbidden = ["family names used", "action-name bonuses", "hidden state"]
    assert "no family names" in joined
    assert "no action-name" in joined
    assert "no hidden state" in joined


def test_causal_investigation_adjustment_output_is_written() -> None:
    summary = main()
    out = ROOT / "outputs" / "pass1_causal_investigation_adjustment_v1.json"
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["study"] == "pass1_causal_investigation_adjustment_v1"
    assert payload["affected_shape_report_count"] >= 0


if __name__ == "__main__":
    test_causal_investigation_adjustment_reports_safe_generic_fix()
    test_causal_investigation_adjustment_output_is_written()
    print("pass1_causal_investigation_adjustment_invariants: PASS")
