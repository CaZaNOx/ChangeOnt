# Certificate-Aware Stable Continuation Update — 2026-05-16

## Status

Implemented as a structural readout-law correction, not as reward tuning.

The change follows the second-stage continuation-gating probe. The previous behavior blocked dominance-style earned collapse when a certificate was non-ready, but `stable_continuation` could still choose a certificate-blocked hiddenness branch while a comparable unblocked alternative existed.

## Code change

Updated:

```text
ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
```

New behavior:

```text
After dominance and reopen/sample fail:
1. choose the highest continuation-score branch as before;
2. if that branch is certificate-blocked, find the best unblocked continuation;
3. if the unblocked continuation is comparable under generic continuation/support margins, select it;
4. if the blocked branch is overwhelmingly stronger, allow continuation-under-burden without calling it dominance.
```

New telemetry:

```text
certificate_aware_stable_continuation_applied
certificate_aware_stable_continuation_alternative
continuation_gate_margin
support_advantage_limit
selected_continuation_gap_before_certificate_gating
selected_support_gap_before_certificate_gating
```

## Why this is structurally justified

The correction preserves the distinction:

```text
dominance / earned collapse ≠ stable continuation under unresolved burden
```

But it prevents `stable_continuation` from degrading into:

```text
highest continuation score after dominance was blocked
```

when an unblocked comparable continuation exists.

## Probe results after correction

`structural_continuation_gating_probe_v1` now reports:

```json
{
  "scenarios": 18,
  "certificate_aware_stable_continuation_switches": 11,
  "selected_blocked_stable_with_comparable_unblocked_alternative": 0,
  "selected_blocked_stable_with_unblocked_alternative": 1
}
```

The one remaining selected-blocked case is the explicit overwhelming-support control, where the unblocked alternative is not comparable.

`structural_microcase_probe_v1` now reports:

```json
{
  "cases": 7,
  "passed": 7,
  "passed_with_watchpoints": 0,
  "failed": 0,
  "selected_blocked_stable_continuation_watchpoints": 0
}
```

## Claim boundary

This does not prove CO works, does not prove RCF novelty, and does not prove empirical usefulness. It only fixes a structural contradiction between certificate-aware readout doctrine and the previous permissive stable-continuation behavior.

## Remaining work

The new margins are behavior-affecting coefficients. They must be added to the formula/coefficient ledger and stress-tested in real adapter traces before any empirical claim is made.
