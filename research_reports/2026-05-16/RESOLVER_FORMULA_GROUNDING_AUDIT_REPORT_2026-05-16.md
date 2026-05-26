# Resolver Formula Grounding Audit — 2026-05-16

## Claim boundary

This report is a structural formula-grounding audit. It is **not** reward evidence, parameter tuning, RCF novelty proof, or proof that CO works empirically.

The audit asks whether resolver recognition is grounded in public burden/effect operations rather than action names or ordinary score bonuses.

## Why this audit was needed

`real_adapter_formula_sensitivity_probe_v1` showed that resolver recognition is behavior-causal. Nearly disabling resolver recognition changes 66 of 311 real-adapter actions after the transform/nonresolver correction. That makes resolver support a high-integrity coefficient path: if it is underdefined, it can become a hidden action preference.

The audit therefore checks the resolver path:

```text
adapter public_effects
→ RelationSurface operation summaries
→ RCF / CollapseCertificate carrier fields
→ CommitmentSurface resolver_support
→ certificate-aware reopen/sample selection
```

## Correction made

`CommitmentSurface` previously counted `branch_internal_transform_pressure` as resolver support. That was too permissive.

Current rule:

```text
reduce / relieve / prevent  → resolver support
reset / cancel              → resolver support
reveal / expose             → resolver support
buffer / absorb             → resolver support
transform / transfer        → transform pressure, not resolver support unless paired with an explicit resolver operation
```

Reason:

A transformation may redirect or reopen burden. It does not by itself show that burden is reduced, exposed, canceled, or buffered. Counting raw transform pressure as resolver support would let mechanism-rewrite facts become certificate clearance without explicit resolution.

## New diagnostic

Added:

```text
ChangeOntCode/experiments/studies/resolver_formula_grounding_audit_v1.py
ChangeOntCode/agents/co/tests/resolver_formula_grounding_audit_invariants.py
```

## Summary output

```json
{
  "cases": 311,
  "candidate_rows_reviewed": 1550,
  "resolver_rows_at_threshold": 629,
  "selected_resolver_rows_at_threshold": 208,
  "transform_pressure_rows": 36,
  "transform_only_rows_counted_as_resolver": 0,
  "selected_transform_only_rows_counted_as_resolver": 0,
  "watchpoints_by_type": {}
}
```

Public effect operations reviewed:

```json
{
  "carry": 1266,
  "decision_slot": 1550,
  "reduce": 279,
  "reset": 217,
  "reveal": 253,
  "transform": 36
}
```

Operation groups:

```json
{
  "carrier_or_masking": 862,
  "relief_or_reduce": 279,
  "cancellation_or_reset": 217,
  "exposure_or_reveal": 253,
  "transform_or_transfer_nonresolver": 36
}
```

## Action-name spoofing checks

The audit added controlled microcases where resolver operations are deliberately assigned to misleading action names.

Checks passed:

```json
{
  "run_named_resolver_recognized": true,
  "repair_named_carrier_not_resolver": true,
  "repair_named_resolver_recognized": true,
  "run_named_carrier_not_resolver": true,
  "transform_only_not_resolver": true,
  "transform_pressure_recorded": true
}
```

Interpretation:

Resolver support follows public operation grammar, not labels like `RUN`, `REPAIR`, `INTERACT`, or `REPLACE`.

## Current grounded status

Stronger than before:

- resolver recognition is behavior-causal;
- resolver recognition is not action-name keyed;
- transform-only pressure is recorded but does not become resolver support;
- weak decision-slot competition remains nonresolver;
- no resolver watchpoints appeared in the 311-case real-adapter sweep.

Still provisional:

- `resolver_support_threshold = 0.08` is not derived from first principles;
- resolver magnitudes remain adapter-public-effect magnitudes and need family-by-family grounding;
- certificate-aware reopen/sample margins still need isolated microcase sweeps;
- this is structural trace evidence, not reward-performance evidence.

## Next implication

The next formula-ledger item is no longer “is resolver recognition action-name bias?” That now has a passing structural check. The next unresolved item is the **magnitude/threshold grounding**:

```text
Why is resolver_support >= 0.08 enough to qualify as a resolver alternative?
How much resolver support should be required under low/high hiddenness, low/high collapse authority, and low/high revision authority?
```

That should be tested with targeted resolver-threshold microcases before empirical performance runs.
