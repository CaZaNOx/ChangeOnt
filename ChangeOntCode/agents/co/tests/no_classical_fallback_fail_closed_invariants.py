"""Invariants for fail-closed canonical CO path.

These tests protect the architecture boundary that evidence-bearing CO runs may
not rescue empty/non-evidential conditions with first-legal, uniform, greedy, or
classical fallback behavior.

Run:
    python -m agents.co.tests.no_classical_fallback_fail_closed_invariants
"""
from __future__ import annotations

from agents.co.boundary.observation_mapper import translate_observation
from agents.co.runtime.support.signal_bus import KernelSignalBus
from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_boundary_does_not_emit_uniform_candidate_scores() -> None:
    scores, mask, meta = translate_observation(
        {"action_space": ["a", "b", "c"]},
        None,
        {},
        {},
        {},
    )
    _assert(scores == {}, f"boundary must fail closed without candidate facts, got {scores}")
    _assert(mask == set(), "empty boundary case should not invent a mask")
    _assert(meta.get("translator_mode") == "thin_boundary_empty_fail_closed", meta)
    _assert(meta.get("co_evidence_valid_for_step") is False, meta)


def test_candidate_surface_does_not_publish_uniform_votes() -> None:
    bus = KernelSignalBus()
    prims = {"signal_bus": bus}
    out = CandidateEvidenceSurface().step({"action_space": ["a", "b"]}, prims, None, None)
    _assert(out.get("candidate_surface_published") == 0, out)
    _assert(out.get("co_evidence_valid_for_step") is False, out)
    _assert(out.get("candidate_surface_contract_violation") == "no_candidate_votes_published", out)
    _assert(bus.size(scope_key="default") == 0, "candidate surface must not publish uniform votes")


def test_commitment_surface_does_not_choose_from_bare_action_space() -> None:
    out = CommitmentSurface().step({"action_space": ["a", "b"]}, {}, None, None)
    _assert("action" not in out, f"bare action_space must not produce action: {out}")


def test_commitment_surface_private_rule_rejects_empty_evidence() -> None:
    cs = CommitmentSurface()
    try:
        cs._canonical_commitment_choice({}, {"action_space": ["a"]}, {}, None, set(), ["a"])
    except RuntimeError as exc:
        _assert("fail-closed" in str(exc), str(exc))
    else:
        raise AssertionError("empty evidence should raise fail-closed RuntimeError")


def test_commitment_surface_ignores_legal_action_space_without_evidence() -> None:
    cs = CommitmentSurface()
    # Evidence exists only for action 'a'.  Action 'b' is legal but has no CO
    # candidate/score evidence and must not be eligible as a fallback option.
    prims = {
        "__candidate_publication_rows__": [
            {"action": "a", "decision_state": 0.5, "base_state": 0.5, "commitment_stability": 0.5}
        ]
    }
    out = cs.step({"action_space": ["a", "b"]}, prims, None, None)
    _assert(out.get("action") == "a", f"legal no-evidence action must not be selected: {out}")
    assessment = out.get("canonical_commitment_assessment", {})
    _assert("b" not in assessment, f"no-evidence legal action entered commitment assessment: {assessment}")


def test_adapter_rejects_invalid_kernel_action_without_rescue() -> None:
    from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement

    class BadPipelineCore:
        def __init__(self) -> None:
            self.primitives = {}

        def step(self, packet, feedback):
            return {"action": "INVALID_ACTION"}

    adapter = COAdapterMaintenanceReplacement(BadPipelineCore())
    try:
        adapter.select({"t": 0, "observe_health_mode": "partial"})
    except RuntimeError as exc:
        _assert("forbids adapter-side" in str(exc), str(exc))
    else:
        raise AssertionError("adapter must fail closed on invalid kernel action instead of rescuing with RUN")



def test_require_kernel_action_rejects_invalid_native_domain() -> None:
    from agents.co.boundary.problem_packet import require_kernel_action

    try:
        require_kernel_action({"action": "z"}, legal_actions=["a", "b"], family="unit_test")
    except RuntimeError as exc:
        _assert("invalid unit_test action" in str(exc), str(exc))
        _assert("forbids adapter-side fallback" in str(exc), str(exc))
    else:
        raise AssertionError("invalid native action must fail closed")


def test_every_active_adapter_passes_public_native_action_domain_to_guard() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "adapters"
    adapter_files = [
        root / "bandit_adapter.py",
        root / "renewal_adapter.py",
        root / "maze_adapter.py",
        root / "latent_mechanism_adapter.py",
        root / "maintenance_replacement_adapter.py",
    ]
    for path in adapter_files:
        src = path.read_text(encoding="utf-8")
        _assert(
            "require_kernel_action(out, legal_actions=" in src,
            f"{path.name} must validate kernel action against public native domain",
        )

def main() -> None:
    test_boundary_does_not_emit_uniform_candidate_scores()
    test_candidate_surface_does_not_publish_uniform_votes()
    test_commitment_surface_does_not_choose_from_bare_action_space()
    test_commitment_surface_private_rule_rejects_empty_evidence()
    test_commitment_surface_ignores_legal_action_space_without_evidence()
    test_adapter_rejects_invalid_kernel_action_without_rescue()
    test_require_kernel_action_rejects_invalid_native_domain()
    test_every_active_adapter_passes_public_native_action_domain_to_guard()


if __name__ == "__main__":
    main()
