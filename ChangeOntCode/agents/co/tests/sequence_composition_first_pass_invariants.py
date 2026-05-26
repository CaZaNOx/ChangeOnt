"""Invariants for first-pass sequence-level continuation composition.

Run with: python -m agents.co.tests.sequence_composition_first_pass_invariants
"""
from __future__ import annotations

from pathlib import Path

from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.runtime.surfaces.sequence_composition import SequenceContinuationComposer, derive_phase_signature
from agents.co.tests.relation_path_trace_diagnostics import TraceBus, TraceHeader, TraceHeaderState


def _effect(operation: str, burden_type: str, *, scope: str = "local", coupling: str = "generic_coupling", magnitude: float = 0.75) -> dict:
    return {
        "operation": operation,
        "kind": "burden",
        "burden_type": burden_type,
        "scope": scope,
        "magnitude": magnitude,
        "public_basis": "declared_transition_rule",
        "leakage_status": "public",
        "direction": operation,
        "coupling": coupling,
    }


def _obs(candidate_id: str, effects: list[dict], *, visible: float = 0.55, support: float = 0.55, contradiction: float = 0.35) -> dict:
    return {
        "family": "sequence_composition_probe",
        "action_space": [candidate_id],
        "candidates": [
            {
                "candidate_id": candidate_id,
                "legal": True,
                "visible_delta": visible,
                "line_support": support,
                "coverage_adequacy": 0.62,
                "tested_hint": 0.30,
                "uncertainty_hint": 0.24,
                "reversibility_hint": 0.72,
                "contradiction_hint": contradiction,
                "public_effects": effects,
            }
        ],
    }


def _step(surface: CandidateEvidenceSurface, obs: dict, feedback: dict | None = None) -> list[dict]:
    prims = {"signal_bus": TraceBus()}
    surface.step(obs, prims, TraceHeader(TraceHeaderState()), feedback)
    return list(prims.get("__candidate_publication_rows__", []))


def test_public_phase_signatures_are_generic() -> None:
    row = {"action": "X", "public_effects": [_effect("reveal", "hiddenness")], "support_mass": 0.4, "burden_pressure": 0.5}
    sig = derive_phase_signature(row)
    assert sig.phase == "expose"
    assert "hidden" in sig.domain


def test_exposure_to_relief_sequence_becomes_active_without_action_semantics() -> None:
    surface = CandidateEvidenceSurface(dynamic_shape_enabled=False, sequence_composition_enabled=True)
    first = _step(surface, _obs("EXPR_A", [_effect("reveal", "hiddenness", scope="local", coupling="shared")], contradiction=0.50))
    assert first and first[0]["continuation_phase"] == "expose"
    second = _step(surface, _obs("EXPR_B", [_effect("reduce", "load", scope="local", coupling="shared")], contradiction=0.20), {"action": "EXPR_A"})
    assert second
    row = second[0]
    assert row.get("sequence_composition_active") is True, row
    assert row.get("sequence_phase_transition") in {"expose_to_relieve", "expose_to_stabilize"}, row
    assert float(row.get("sequence_composition_support", 0.0)) > 0.0
    assert row.get("sequence_continuation_id")


def test_sequence_composition_can_be_disabled_for_ablation() -> None:
    surface = CandidateEvidenceSurface(dynamic_shape_enabled=False, sequence_composition_enabled=False)
    _step(surface, _obs("EXPR_A", [_effect("reveal", "hiddenness", scope="local", coupling="shared")], contradiction=0.50))
    second = _step(surface, _obs("EXPR_B", [_effect("reduce", "load", scope="local", coupling="shared")], contradiction=0.20), {"action": "EXPR_A"})
    assert second
    row = second[0]
    assert row.get("sequence_composition_active") is False
    assert row.get("sequence_composition_disabled") is True


def test_hidden_or_nonpublic_effects_do_not_create_sequence() -> None:
    composer = SequenceContinuationComposer()
    prior = [{"action": "A", "public_effects": [_effect("reveal", "hiddenness", coupling="shared")], "support_mass": 0.4, "burden_pressure": 0.5}]
    rows, _ = composer.apply(prior, feedback=None, controls={})
    # Store prior row then feed a non-public current effect; it must not produce a sequence.
    rows, _ = composer.apply([{"action": "B", "public_effects": [{**_effect("reduce", "load", coupling="shared"), "leakage_status": "oracle"}], "support_mass": 0.6, "burden_pressure": 0.1}], feedback={"action": "A"}, controls={})
    assert rows[0].get("sequence_composition_active") is False


def test_no_problem_family_or_native_action_literals_in_implementation() -> None:
    src = Path(__file__).resolve().parents[1] / "runtime" / "surfaces" / "sequence_composition.py"
    text = src.read_text(encoding="utf-8").lower()
    forbidden = ["maintenance", "bandit", "renewal", "maze", "latent", "inspect", "repair", "replace", "wait"]
    hits = [x for x in forbidden if x in text]
    assert not hits, hits


def main() -> None:
    test_public_phase_signatures_are_generic()
    test_exposure_to_relief_sequence_becomes_active_without_action_semantics()
    test_sequence_composition_can_be_disabled_for_ablation()
    test_hidden_or_nonpublic_effects_do_not_create_sequence()
    test_no_problem_family_or_native_action_literals_in_implementation()
    print("sequence_composition_first_pass_invariants passed")


if __name__ == "__main__":
    main()
