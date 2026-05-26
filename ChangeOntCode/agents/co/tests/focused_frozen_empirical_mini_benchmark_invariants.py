from __future__ import annotations

"""Invariants for the focused frozen empirical mini-benchmark.

These checks protect the benchmark-shaped study from becoming a performance claim:
outputs must exist, constants must be declared frozen, baselines must be explicit,
and CO structural telemetry must be present.  The tests do not assert CO wins.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs" / "focused_frozen_empirical_mini_benchmark_v1"


def _read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_focused_mini_benchmark_outputs_exist() -> None:
    for rel in ["suite_manifest.json", "runs.jsonl", "structural_telemetry.jsonl", "summary.json"]:
        path = OUT / rel
        assert path.exists(), f"missing benchmark output: {path}"
        assert path.stat().st_size > 0, f"empty benchmark output: {path}"


def test_focused_mini_benchmark_is_frozen_and_bounded() -> None:
    manifest = json.loads((OUT / "suite_manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
    boundary = str(summary.get("claim_boundary", "")).lower()
    assert manifest.get("constants_frozen_before_run") is True
    assert manifest.get("no_tuning_after_results") is True
    assert "not broad benchmark evidence" in boundary
    assert "not co proof" in boundary
    assert "not novelty evidence" in boundary


def test_focused_mini_benchmark_has_co_and_public_baselines_per_family() -> None:
    runs = _read_jsonl(OUT / "runs.jsonl")
    families = {str(r["family"]) for r in runs}
    assert families == {"maintenance_replacement"}
    for family in families:
        fam = [r for r in runs if str(r["family"]) == family]
        assert any(r.get("baseline_type") == "co" for r in fam), f"missing CO run for {family}"
        assert any(r.get("baseline_type") != "co" for r in fam), f"missing public baseline run for {family}"
        assert all(r.get("parity_label") for r in fam), f"missing parity labels for {family}"


def test_focused_mini_benchmark_preserves_structural_telemetry() -> None:
    rows = _read_jsonl(OUT / "structural_telemetry.jsonl")
    assert rows, "missing structural telemetry"
    families = {str(r.get("family")) for r in rows}
    assert families == {"maintenance_replacement"}
    assert any("canonical_commitment_mode" in r for r in rows), "missing commitment mode telemetry"
    assert any(bool(r.get("certificate_aware_reopen_or_sample_applied")) for r in rows), "expected at least one resolver-aware reopen/sample telemetry event in focused suite"
