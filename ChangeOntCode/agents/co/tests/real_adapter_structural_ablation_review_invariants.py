"""Invariants for real-adapter structural ablation review.

The review must remain structural: it checks mechanism dependence and telemetry
changes, not reward performance. These invariants protect the minimum expected
causal signal from public-effect/removal ablations and ensure weak competition
alone does not masquerade as branch-internal burden structure.
"""

from __future__ import annotations

from experiments.studies.real_adapter_structural_ablation_review_v1 import main


def test_real_adapter_ablation_has_public_effect_signal() -> None:
    result = main()
    summary = result["summary"]
    no_public = summary["comparisons_vs_full"]["no_public_effects"]
    assert summary["cases"] >= 300
    assert no_public["positive_structural_relation_delta_cases"] > 0
    assert no_public["positive_branch_internal_delta_cases"] > 0
    assert no_public["mode_changes"] > 0 or no_public["action_changes"] > 0


def test_weak_competition_only_is_not_burden_structure() -> None:
    result = main()
    weak = result["summary"]["comparisons_vs_full"]["weak_competition_only"]
    # Full should carry branch-internal operation rows in cases where weak-only
    # does not; otherwise weak procedural slot facts would be overcounted as CO
    # burden carriers.
    assert weak["positive_branch_internal_delta_cases"] > 0


def test_resolver_ablations_affect_certificate_aware_sampling() -> None:
    result = main()
    no_resolver = result["summary"]["comparisons_vs_full"]["no_resolver_ops"]
    carrier_only = result["summary"]["comparisons_vs_full"]["carrier_only_no_resolver"]
    assert no_resolver["certificate_aware_reopen_changes"] > 0
    assert carrier_only["certificate_aware_reopen_changes"] > 0
