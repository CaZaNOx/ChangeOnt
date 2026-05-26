# 85. Relation-to-Collapse Diagnostic Contract

Status: kernel diagnostic contract; first microdiagnostic implementation present.

This document binds:

```text
TheoryOfChange_main/01_Statements/Derivation/S-DR-burden-relations-to-quotient-collapse-and-recursion.md
TheoryOfChange_main/01_Statements/Clarification/S-CL-relation-to-collapse-microdiagnostics.md
80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md
81_STRUCTURAL_PROXIMITY_PATH_DENSITY_AND_RECURSION_CONTRACT.md
84_BURDEN_OPERATION_ALGEBRA.md
```

to the next pre-benchmark validation step.

---

## 1. Purpose

Before broad family benchmarks are interpreted as evidence for a CO-native RCF, the runtime must pass relation-to-collapse diagnostics showing that burden operations and relation topology affect quotient, grey preservation, recursion, and collapse in traceable ways.

This contract is not a performance benchmark. It is a mechanism-validity gate.

---

## 2. Required mechanism chain

A successful implementation must make the following chain visible in telemetry:

```text
public burden/effect fact
→ burden operation
→ derived branch relation
→ branch-field deformation
→ quotient / grey / recursion / collapse effect
→ action expression, if collapse is earned
```

If the chain skips directly from candidate scalar score to selected action, the diagnostic fails as a CO-native mechanism test.

---

## 3. Required microdiagnostics

### D85.1 Fixed-score relation topology

Scalar candidate fields are held fixed while relation topology changes.

Expected:

```text
field behavior changes for relation reasons.
```

Reject if:

```text
behavior is unchanged or relation changes are merely scalar bonuses without traceable burden operations.
```

### D85.2 Dense equivalent path quotient

Many branches have equivalent residual continuation profiles.

Expected:

```text
quotient/merge/shared state increases;
recursion does not grow merely from count.
```

### D85.3 Dense non-equivalent grey preservation

Many branches remain non-equivalent by burden type, barrier, collapse consequence, or relation topology.

Expected:

```text
grey preservation and/or bounded recursion increases.
```

### D85.4 Buffering versus masking

Low apparent burden is produced once by genuine absorption/buffering and once by masking/postponement.

Expected:

```text
buffering may permit cheap collapse;
masking retains debt/burden and delays collapse or requires exposure.
```

### D85.5 Relief versus cancellation

A burdened branch has one relief branch and one cancellation/reset branch.

Expected:

```text
relief and cancellation produce distinguishable field effects.
```

### D85.6 Exposure under hiddenness

An exposure branch reveals or reduces hidden burden relevant to another branch's collapse.

Expected:

```text
exposure gains viability/recursion priority under hidden-decisive regimes.
```

### D85.7 Sparse high-consequence branch

A single non-equivalent unresolved branch has high collapse consequence.

Expected:

```text
recursion/grey preservation may activate despite low path density.
```

### D85.8 Collapse certificate

A high-score branch with unresolved non-equivalent rivals is compared to a lower-score branch whose rivals are quotient/canceled/nonoperative.

Expected:

```text
collapse follows certificate status, not raw score alone.
```

---

## 4. Telemetry requirements

Each diagnostic must log:

```text
identity_source_counts
branches_derived
public_effect_rows
burden_operations_by_type
relations_by_type
relations_rejected_for_leakage
relations_rejected_for_insufficient_basis
quotient_count
grey_preservation_events
recursion_demand_events
collapse_certificate_status
collapse_blockers
action_expression_source
```

A diagnostic without this telemetry is not evidence. It may be useful debugging output, but it cannot support a paper claim.

---

## 5. Collapse certificate fields

A first implementation may approximate the collapse certificate, but it must separately report these logical components:

```text
branch_identity_stable
burden_resolved_or_bounded
rivals_quotient_canceled_or_nonoperative
hiddenness_within_tolerance
relation_topology_no_longer_demands_recursion
grey_difference_nonoperative
fallback_not_evidence_bearing
```

The implementation may summarize these into a scalar `collapse_readiness`, but that scalar is not a substitute for the certificate.

---

## 6. Failure interpretations

### Scalar scoring failure

If fixed-score relation topology changes do not alter field behavior, RCF is still scalar scoring.

### Path-count search failure

If dense equivalent paths increase recursion instead of quotienting, recursion is path-count search rather than continuation-field regulation.

### Premature quotient failure

If dense non-equivalent paths quotient because scalar values are close, the field is erasing operative difference.

### Stability-as-relief failure

If low visible burden or high stability counts as relief without a public burden operation, the field is inferring relation structure from scalar comfort.

### Argmax collapse failure

If collapse follows highest score despite unresolved non-equivalent burden relations, earned collapse is not implemented.

---

## 7. Relationship to family benchmarks

Family benchmarks may be run after these diagnostics, but reward deltas do not replace them. A family-level result is interpretable only if the runtime can show which burden operations, relations, quotient events, grey events, recursion events, and collapse certificates occurred.

This is the bridge from conceptual burden algebra to honest empirical testing.

---

## 8. First toy diagnostic implementation — 2026-05-06

The first non-benchmark diagnostic implementation lives at:

```text
ChangeOntCode/agents/co/tests/burden_relation_microdiagnostics.py
```

It checks the current explicit-relation RCF path against the following microdiagnostic cases:

```text
fixed scalar rows with changed relation topology;
masking versus buffering;
exposure/shared evidence versus relief;
relief versus cancellation;
dense equivalent paths quotienting instead of preserving extra grey;
dense non-equivalent paths preserving grey/recursion;
sparse high-consequence unresolved relation driving recursion;
collapse certificate distinction between quotient-equivalence and unresolved rivalry.
```

These tests are not family benchmarks and do not claim reward improvement. They only verify that the current field path can react differently when relation topology and burden-operation roles differ.

Current limitation: this diagnostic module still uses direct explicit relations or row-embedded relation hints. It does not yet implement the full kernel-side `RelationSurface`, public burden/effect fact derivation, or the complete telemetry list required above. Passing these tests is therefore a necessary mechanism sanity check, not sufficient evidence for a finished CO-native kernel.


---

## 9. RelationSurface public-effect implementation — 2026-05-06

The first public-effect RelationSurface diagnostics live at:

```text
ChangeOntCode/agents/co/tests/relation_surface_public_effect_invariants.py
```

These tests verify that public burden/effect facts can derive relations before RCF, and that non-public/solver-like facts are rejected.
