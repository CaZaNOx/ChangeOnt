from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    out = ROOT / "outputs" / "pass1_kernel_closure_audit_v1.json"
    assert out.exists(), "run experiments.studies.pass1_kernel_closure_audit_v1 first"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["study"] == "pass1_kernel_closure_audit_v1"
    assert data["verdict"]["pass1_kernel_mechanism_set_present"] is True
    assert data["verdict"]["pass1_kernel_closure_candidate"] is True
    assert data["verdict"]["release_ready"] is False
    assert data["verdict"]["publication_ready"] is False
    assert data["diagnostic_map"]["runs_failed"] == 0
    assert data["mechanism_visibility"]["avg_dynamic_shape_applied_steps"] > 0.0
    assert data["mechanism_visibility"]["avg_sequence_active_steps"] > 0.0
    assert data["mechanism_visibility"]["avg_recursion_scheduler_demand"] >= 0.0
    assert "no_sequence" in data["ablation_sensitivity"]["by_ablation"]
    assert len(data["blocking_watchpoints"]) >= 5
    assert any(w["id"] == "P1A_MAINTENANCE_INSENSITIVITY_UNRESOLVED" for w in data["blocking_watchpoints"])
    print("pass1_kernel_closure_audit_invariants: PASS")


if __name__ == "__main__":
    main()
