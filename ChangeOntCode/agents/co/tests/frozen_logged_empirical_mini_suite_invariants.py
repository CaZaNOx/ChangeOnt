from __future__ import annotations

"""Invariants for the frozen logged empirical mini-suite.

These checks do not assert performance wins. They assert that the mini-suite is
frozen, explicit about baselines, and preserves auditable logs/CO structural
telemetry.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs" / "frozen_logged_empirical_mini_suite_v1"


def _read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_frozen_logged_empirical_mini_suite_outputs_exist() -> None:
    for rel in ["suite_manifest.json", "runs.jsonl", "structural_telemetry.jsonl", "summary.json"]:
        path = OUT / rel
        assert path.exists(), f"missing mini-suite output: {path}"
        assert path.stat().st_size > 0, f"empty mini-suite output: {path}"


def test_frozen_logged_empirical_mini_suite_has_explicit_baselines_and_co() -> None:
    runs = _read_jsonl(OUT / "runs.jsonl")
    families = {str(r["family"]) for r in runs}
    assert {"bandit", "renewal", "maze", "maintenance_replacement", "latent_mechanism"}.issubset(families)
    for family in families:
        fam_runs = [r for r in runs if str(r["family"]) == family]
        assert any(r.get("baseline_type") == "co" for r in fam_runs), f"missing CO run for {family}"
        assert any(r.get("baseline_type") != "co" for r in fam_runs), f"missing explicit baseline for {family}"


def test_frozen_logged_empirical_mini_suite_claim_boundary_is_non_evidential() -> None:
    summary = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
    boundary = str(summary.get("claim_boundary", "")).lower()
    assert "not benchmark evidence" in boundary
    assert "not tuning evidence" in boundary
    assert "not co proof" in boundary


def test_frozen_logged_empirical_mini_suite_preserves_co_telemetry() -> None:
    rows = _read_jsonl(OUT / "structural_telemetry.jsonl")
    assert rows, "missing CO structural telemetry rows"
    families = {str(r.get("family")) for r in rows}
    assert {"bandit", "renewal", "maze", "maintenance_replacement", "latent_mechanism"}.issubset(families)
    assert any("canonical_commitment_mode" in r for r in rows), "no canonical commitment telemetry preserved"
    assert any("signal_bus_votes" in r for r in rows), "no signal bus telemetry preserved"
