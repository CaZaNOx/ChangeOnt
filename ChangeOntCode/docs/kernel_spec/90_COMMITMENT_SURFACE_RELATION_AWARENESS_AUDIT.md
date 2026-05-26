# 90 — CommitmentSurface Relation-Awareness Audit

Status: historical diagnostic audit, superseded by the minimal CollapseCertificate implementation in `91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md`. Not reward evidence.

## Purpose

This file records the readout gap that existed after the first RelationSurface/RCF wiring pass. It is retained because it explains why CollapseCertificate was introduced. It is **not** the current implementation status.

## Historical audit result

The earlier runtime path was:

```text
adapter public_effects
→ kernel-side RelationSurface
→ explicit branch relations
→ RecursiveContinuationField field deformation
→ CommitmentSurface / action expression
```

At that stage, CommitmentSurface was relation-influenced mostly through scalar/proxy row fields. It did not yet consume first-class collapse-certificate fields. The diagnostic therefore found a real architecture gap: relation topology could reach RCF, but final readout could still flatten relation reasons too early.

Historical summary from that stage:

```text
relation_positive_cases = 5 / 5
field_delta_positive_cases = 5 / 5
commitment_changed_cases = 0 / 5
```

Interpretation at that time: relation topology reached RCF field computation, but sampled final commitments did not change.

## Current correction

The current runtime path is now:

```text
CandidateSurface
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

`CollapseCertificate` now preserves first-class collapse reasons before final readout, including:

```text
collapse_certificate_status
collapse_certificate_ready
collapse_certificate_score / earnedness
collapse_certificate_blocker_pressure
collapse_certificate_recursion_demand
collapse_blockers
unresolved_rival_count
quotient_resolved_rival_count
relations_by_type
weak_decision_competition_count
```

The current implementation and diagnostic status are recorded in:

```text
91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md
92_ARCHITECTURE_ACCEPTANCE_AUDITS.md
94_REAL_TRACE_STRUCTURAL_VALIDATION_AND_FORMULA_GROUNDING.md
95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
```

Current relation-path diagnostics report:

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "relations_total": 80,
  "non_rival_relations": 16,
  "field_delta_positive_cases": 5,
  "commitment_action_changed_cases": 0,
  "commitment_mode_changed_cases": 1
}
```

This is mechanism/trace evidence only. It is not reward evidence and not proof of final earned-collapse theory.

## Remaining risk

The readout gap is no longer simply "certificate absent." The remaining risks are:

```text
certificate reasons may be too coarse;
formula/gate weights are not fully grounded;
relation quality remains watchpoint-level;
certificate-caused behavior changes need controlled ablations;
weak decision-slot competition must remain telemetry, not strong rivalry.
```

## Failure modes to continue avoiding

### Metadata policy leakage

Do not let adapters publish `collapse_certificate_status = choose_this` or equivalent policy advice.

### Scalar flattening

Do not claim earned collapse if relation topology affects only a scalar score and the readout cannot explain which relation condition was resolved, blocked, quotiented, or preserved as grey.

### Rivalry noise

Do not let generic decision-slot competition dominate collapse certificates. Burden-specific relief, cancellation, equivalence, shared evidence, masking, buffering, exposure, and threshold relations must remain distinguishable.

## Evidence status

Current status:

```text
relation path to RCF: present
relation field deltas: present
first-class earned-collapse certificate: minimal v1 present
relation-aware final commitment: structurally present, still watchpoint-level
reward/performance evidence: not claimed
```
