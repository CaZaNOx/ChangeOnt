# Structural Continuation-Gating Probe Report — 2026-05-16

## Status

Diagnostic added, executed, and used to implement the first certificate-aware `stable_continuation` correction.

This report is not benchmark evidence. It records a controlled structural probe following `STRUCTURAL_MICROCASE_PROBE_REPORT_2026-05-16.md`.

## Why this probe exists

The first structural microcase probe exposed one remaining watchpoint:

```text
A branch whose certificate blocks dominance could still be selected under
stable_continuation when local support was materially higher than an unblocked
alternative.
```

The code already blocked **dominance-style earned collapse** when a certificate was non-ready under active blocker/recursion pressure. The unresolved question was whether the non-dominance mode `stable_continuation` should also be certificate-aware when an unblocked alternative exists.

## Design decision taken

The repo now implements **certificate-aware stable continuation**:

```text
After dominance and reopen/sample fail, if the highest continuation candidate
is certificate-blocked, CommitmentSurface checks the best unblocked continuation.
If the unblocked continuation is comparable under generic continuation/support
margins, it is selected instead.
If the blocked continuation is overwhelmingly stronger, it may still continue
under unresolved burden, but not as earned dominance.
```

This is Option B from the earlier probe discussion, but it is not a hard veto. It preserves the possibility of continuation-through-burden when no comparable clean continuation exists.

## Added / updated diagnostic

```text
ChangeOntCode/experiments/studies/structural_continuation_gating_probe_v1.py
ChangeOntCode/agents/co/tests/structural_continuation_gating_probe_invariants.py
```

The diagnostic sweeps synthetic support gaps between:

```text
continue_hidden: carries hiddenness burden and has a non-ready/blocking certificate
neutral_probe: unblocked alternative
inspect_exposes: unblocked alternative that explicitly exposes hiddenness
```

It also includes controls:

```text
overwhelming_support_continues_under_burden_control
all_branches_blocked_no_unblocked_counterfactual
```

## Latest result summary after correction

```json
{
  "scenarios": 18,
  "certificate_aware_stable_continuation_switches": 11,
  "selected_blocked_stable_with_comparable_unblocked_alternative": 0,
  "selected_blocked_stable_with_unblocked_alternative": 1,
  "current_vs_best_unblocked_counterfactual_differs": 1
}
```

Interpretation:

- Comparable unblocked continuations now displace blocked hiddenness continuations.
- The remaining selected-blocked case is the explicit overwhelming-support control, where the unblocked alternative is outside the comparable band.
- The all-blocked control remains permissive because there is no unblocked continuation to choose.

## Implemented rule location

```text
ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
```

The new telemetry fields include:

```text
certificate_aware_stable_continuation_applied
certificate_aware_stable_continuation_alternative
continuation_gate_margin
support_advantage_limit
selected_continuation_gap_before_certificate_gating
selected_support_gap_before_certificate_gating
```

## Claim boundary

This correction does not prove reward performance or CO novelty. It only repairs a structural readout issue:

```text
stable_continuation is no longer simply the highest continuation score after
dominance is blocked when a comparable unblocked continuation exists.
```

The margins are still provisional and must enter the formula/coefficient ledger. Future empirical studies must not treat this as a tuned performance improvement.

## Remaining watchpoint

The rule still contains behavior-affecting coefficients. They are conceptually grounded by blocker pressure, revision, rivalry, nonlocal authority, collapse admissibility, and local authority, but the exact weights are provisional.

Required follow-up:

```text
1. record the new margins in the formula ledger;
2. inspect real adapter traces for action/mode changes;
3. verify that the rule does not make the system over-timid in maintenance/maze/renewal;
4. keep oracle/classical fallback prohibited.
```
