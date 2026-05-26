# runtime/surfaces/

Canonical role: generic runtime publication, relation, field, certificate, and finalization surfaces for the active CO loop.

Active loop here:

```text
CandidateSurface
→ ContinuationState / continuation identity carriers
→ branch-internal burden operation carriers
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

Allowed:

- candidate publication from lawful public packet structure;
- continuation-state tracking and branch identity telemetry;
- branch-internal burden operation carriers;
- kernel-side relation derivation from public effects;
- recursive continuation field updates;
- earned-collapse certificate construction;
- final commitment/readout through `CommitmentSurface` only;
- telemetry that makes the above traceable.

Forbidden:

- family-local rescue logic;
- hidden-state policy leakage;
- non-CO rescue in the canonical CO path;
- environment/boundary imports;
- baseline-policy selection;
- treating action labels as default branch identity when richer identity carriers exist.
