from __future__ import annotations

"""Invariant wrapper for the continuation-gating structural probe.

This test protects the certificate-aware stable-continuation correction.  It
requires comparable unblocked alternatives to displace blocked stable
continuations, while preserving a control where an overwhelmingly stronger
blocked branch may continue under unresolved burden.
"""

from experiments.studies.structural_continuation_gating_probe_v1 import main


def test_continuation_gating_probe_redirects_comparable_blocked_continuations() -> None:
    result = main()
    agg = result.get("aggregate", {})
    assert int(agg.get("scenarios", 0)) >= 10
    assert int(agg.get("selected_blocked_stable_with_comparable_unblocked_alternative", 0)) == 0, result
    assert int(agg.get("certificate_aware_stable_continuation_switches", 0)) >= 1, result
    assert "reward" not in str(result.get("claim_boundary", "")).lower() or "not" in str(result.get("claim_boundary", "")).lower()


def test_continuation_gating_probe_preserves_overwhelming_support_control() -> None:
    result = main()
    control = [s for s in result.get("scenarios", []) if s.get("scenario") == "overwhelming_support_continues_under_burden_control"]
    assert control, result
    record = control[0]
    assert record.get("selected_action") == "continue_hidden", record
    assert record.get("selected_is_certificate_blocked") is True, record
    assert record.get("selected_blocked_stable_with_comparable_unblocked_alternative") is False, record
