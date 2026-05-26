# Real Adapter Certificate-Gating Review — 2026-05-16

## Scope

This review is a structural diagnostic, not a reward benchmark. It asks whether the certificate-aware readout laws introduced after the microcases behave coherently on real adapter candidate rows.

Reviewed path:

```text
adapter public_effects
→ CandidateSurface
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

The review uses:

- the five standard structural-trace adapter samples;
- a public-observation sweep over maintenance/replacement states;
- a public-observation sweep over latent-mechanism states.

No reward-performance claim is made here.

## Initial finding before correction

The certificate-aware stable-continuation rule did not fire in the five standard real-adapter samples. That was not itself a failure:

- maintenance and maze selected unblocked branches;
- latent mechanism had blocked candidates but no comparable unblocked continuation in the standard sample;
- bandit and renewal used `reopen_or_sample` with selected branches that also carry their own public resolver operation by sampling/reducing uncertainty.

The broader sweep exposed a different issue: `reopen_or_sample` could select a certificate-blocked branch merely because the branch carried burden/recursion pressure, even when a comparable unblocked resolver branch was available. This was most visible in maintenance rows where `RUN` carried degradation/hiddenness while `REPAIR` or `INSPECT` had public resolver/exposure effects.

This was a real readout-law gap. Sampling/reopening should select a branch that can expose, reduce, cancel, buffer, or otherwise resolve the unresolved burden. It should not select a blocked carrier-only branch just because that branch is burdened.

## Correction made

`CommitmentSurface` now includes certificate-aware reopen/sample gating:

```text
If reopen_or_sample would select a certificate-blocked branch,
and that branch has no resolver operation,
and a comparable unblocked resolver alternative exists,
select the resolver alternative instead.
```

The selected blocked branch is still allowed when:

- it has its own resolver operation, such as sampling an uncertain arm to reduce that arm-local uncertainty; or
- no unblocked resolver alternative exists.

New telemetry includes:

```text
certificate_aware_reopen_or_sample_applied
certificate_aware_reopen_or_sample_original
certificate_aware_reopen_or_sample_alternative
sampling_gate_margin
sampling_support_advantage_limit
selected_sampling_gap_before_certificate_gating
selected_sampling_support_gap_before_certificate_gating
```

## Diagnostic results after correction

Output file:

```text
ChangeOntCode/outputs/real_adapter_certificate_gating_review_v1.json
```

Aggregate:

```json
{
  "cases": 311,
  "certificate_aware_stable_continuation_applied_cases": 0,
  "certificate_aware_reopen_or_sample_applied_cases": 66,
  "stable_selected_blocked_with_unblocked_alternative_without_switch": 0,
  "reopen_or_sample_selected_blocked_despite_unblocked_resolver_watchpoints": 0,
  "watchpoints_by_type": {}
}
```

Standard five-sample adapter route:

```json
{
  "cases": 5,
  "certificate_aware_stable_continuation_applied_cases": 0,
  "certificate_aware_reopen_or_sample_applied_cases": 0,
  "stable_selected_blocked_with_unblocked_alternative_without_switch": 0,
  "reopen_or_sample_selected_blocked_despite_unblocked_resolver_watchpoints": 0,
  "watchpoints_by_type": {}
}
```

Interpretation:

- The stable-continuation correction remains mostly microcase-protected in the current standard real samples; it does not materially fire there.
- The real-adapter sweep did exercise a real readout defect in `reopen_or_sample` and the new resolver-aware correction applied in 66 cases.
- The remaining 30 blocked reopen/sample selections occur where no unblocked resolver alternative exists in the local candidate set. They are retained as notes, not watchpoints.

## Current status

This improves structural fidelity but does not prove performance or novelty. The new sampling gate introduces behavior-affecting margins and therefore expands the formula-ledger burden.

Open formula-ledger entries:

```text
resolver_support threshold
sampling_gate_margin
sampling_support_advantage_limit
criteria for “comparable” resolver alternative
conditions for allowing blocked sampling when no resolver alternative exists
```

Next appropriate step:

```text
Run small real-family manual traces and then controlled empirical smoke runs with frozen constants, making sure any behavioral changes are interpreted structurally before reward performance is discussed.
```
