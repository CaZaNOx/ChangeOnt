# 95. Kernel Structure Carrier Alignment

Status: docs-first target contract for carrier-placement fixes  
Date: 2026-05-06  
Claim boundary: architecture validation; not reward evidence.

## Purpose

The previous relation-path work made cross-branch topology explicit:

```text
public_effects -> RelationSurface -> RCF -> CollapseCertificate -> CommitmentSurface
```

Manual structural trace inspection then exposed a broader carrier-placement risk:
not every CO-relevant structure is a relation between two branches.  Some
structure is internal to one branch, some is temporal, some is gauge/regime
conditioned, some is quotient/collapse state, and some is only procedural
telemetry.  If those structures are forced into the wrong runtime carrier, the
implementation can look relation-aware while still misrepresenting the concept.

This file defines the target state that code must implement.

## Carrier classes

Every CO-relevant runtime fact must be assigned to one of these carrier classes.

```text
branch-internal burden operation
cross-branch relation
temporal branch state
regime/gauge control
quotient/equivalence marker
collapse-certificate blocker or resolver
readout gate
telemetry-only procedural fact
```

A fact may appear in more than one carrier only when the roles are distinct and
logged separately.

## Public effects must produce branch-internal operations

A public effect should not matter only when it can be paired with another branch.

Examples:

```text
SAMPLE arm A reduces arm-A uncertainty
INSPECT exposes health hiddenness
RUN carries or masks degradation
WAIT buffers ordinary degradation pressure
MOVE carries path-revisit burden
```

These are valid kernel inputs even if no second branch produces a cross-branch
relation.  Therefore `RelationSurface` must preserve first-class
branch-internal operation summaries such as:

```text
branch_internal_unresolved_pressure
branch_internal_resolver_support
branch_internal_cancellation_support
branch_internal_exposure_support
branch_internal_buffering_support
branch_internal_masking_pressure
branch_internal_threshold_pressure
branch_internal_hiddenness_pressure
branch_internal_transform_pressure
branch_internal_operation_counts
branch_internal_burden_types
```

These fields are not policy advice.  They are the branch-local burden-operation
carrier produced from public facts. Procedural `decision_slot` / weak competition
facts are excluded from branch-internal burden-operation counts; they remain
relation telemetry only.

## Cross-branch relations remain distinct

Relations should only express coupling between branches:

```text
relief(B, A): B reduces a burden carried by A
cancellation(B, A): B resets/cancels A's burden condition
shared_evidence(B, A): B exposes evidence relevant to A
rivalry(A, B): A and B are continuation-level incompatible
equivalence(A, B): A and B are same enough under active continuation tolerance
```

Weak decision-slot competition is procedural telemetry.  It must not become
strong rivalry or a collapse blocker by itself.

## Hiddenness carrier rule

Hiddenness can appear in two ways:

1. branch-internal burden: this branch carries unresolved hiddenness;
2. cross-branch relation: another branch exposes/reduces hiddenness relevant to it.

If no exposure branch exists, high hiddenness may still affect collapse through a
certificate blocker or recursion-demand signal under the active gauge.  It must
not vanish merely because it did not form a cross-branch relation.

## Buffering versus masking

```text
buffering: tension is absorbed/routed and does not convert into operative burden.
masking: burden remains active while local support makes it appear harmless.
```

Both can have high local support.  The carrier must distinguish them.
Buffering may resolve or lower blocker pressure; masking should raise caution,
grey pressure, or recursion demand.

## Quotient/equivalence carrier rule

Equivalence may not be based on action labels, raw scalar similarity, or weak
competition.  It must be derived from matching continuation-relevant pressure
signatures under the active tolerance.  Quotient facts should remain explicit as
`quotient_id`, `quotient_share_count`, and certificate reason flags.

## Collapse-certificate carrier rule

The certificate must preserve structured reasons rather than only a score.
Branch-internal operations can affect the certificate directly:

```text
hiddenness pressure -> hiddenness blocker / recursion demand
masking pressure -> masking blocker / caution
buffering support -> resolver support
relief/cancellation support -> burden-resolution reason
threshold pressure -> phase/critical caution or blocker
```

## Readout carrier rule

CommitmentSurface may consume certificate fields and scalar summaries, but a
high scalar score must not override an active structural blocker without an
explicit documented rule.  No non-CO rescue selector or first-legal rescue is allowed.

## Acceptance tests

The architecture should be considered aligned only when tests show:

```text
branch-internal public effects survive without cross-branch relations;
hiddenness can block/raise recursion without an exposure branch;
buffering and masking produce different certificate states;
weak decision-slot competition is telemetry-only;
quotient does not derive from weak competition or raw score similarity;
readout changes, when they occur, are traceable to certificate reasons.
```
