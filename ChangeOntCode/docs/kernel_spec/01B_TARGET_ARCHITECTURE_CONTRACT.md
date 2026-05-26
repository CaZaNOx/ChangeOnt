# 01B. Target Architecture Contract

Status: canonical target contract for the current CO kernel execution loop.  
Last consolidated: 2026-05-06.  
Claim boundary: docs target state; implementation must be audited against this file.

## Purpose

This file defines what the active CO kernel is allowed to be and what the runtime must implement. It states the current positive target: public structure is transformed into continuation identity, burden operations, relation topology, field state, earned-collapse certificates, and final commitment.

The current target is:

```text
public problem facts
→ candidate expressions
→ continuation identity
→ burden interpretation
→ burden operation typing
→ relation topology
→ recursive continuation field
→ earned-collapse certificate
→ commitment/readout
→ environment update
```

## Layer contract

### Boundary / Adapter

The boundary exposes lawful public structure. It may publish:

```text
native observation summaries;
legal candidate expressions;
task / continuation anchor;
hidden/public distinction;
public_effects / public burden-effect facts;
public constraints and admissible/prohibited transformations.
```

It must not publish:

```text
optimal action labels;
DP/Q values;
hidden-state policy advice;
shortest-path answers from unavailable topology;
family-specific rescue logic;
post-hoc benchmark tuning.
```

### Kernel

The kernel performs problem-agnostic change-processing over public structure. Its active responsibilities are:

```text
construct continuation identities;
interpret branch-internal burden operations;
derive cross-branch relations;
update field state through RCF;
mark quotient/equivalence, grey pressure, and recursion demand;
produce structured earned-collapse certificates;
constrain commitment through the certificate.
```

### Readout

Readout expresses an earned collapse as a native action. It must not become a policy head that chooses by score-maximum selection, first-legal rescue, greedy reward, or baseline-policy rescue.

### Experiment

Experiments test whether code implements the docs. Reward/performance is not interpretable as CO evidence unless boundary leakage, non-CO rescue, relation/certificate trace, and formula-ledger checks pass.

## Canonical execution loop

```text
0. Problem state / observation
   Environment presents the current local situation: observations, legal actions,
   public signals, hidden/public distinction, and task/continuation anchor.

1. Boundary / Adapter
   Translate native problem information into lawful public structure. Publish
   candidate expressions and public_effects. Do not solve.

2. Candidate Surface
   Publish candidate rows as thin operational carriers. Candidate rows are not
   final branches and not final decisions.

3. Continuation Identity Construction
   Derive continuation_id / branch identity from retained pressure signatures:
   task anchor, burden profile, deformation direction, retained invariant,
   relation scope, and collapse condition. Action labels are last-resort aliases.

4. Burden Interpretation
   Interpret public facts through the continuation anchor. Change-field asymmetry
   becomes tension; operative tension becomes burden.

5. Burden Operation Typing
   Type what each branch does with burden: carry, amplify, expose, mask, buffer,
   relieve, cancel, transfer, transform, threshold/phase-shift.

6. Relation Surface
   Derive typed cross-branch relations from public burden/effect facts:
   relief, cancellation, shared evidence, dependency, strong rivalry,
   equivalence/quotient, and weak decision-slot competition as telemetry only.

7. Recursive Continuation Field
   Update branch field state using branch-internal operations, relations,
   retention, gauge/shape controls, debt, relief, grey pressure, quotient,
   recursion demand, and viability.

8. Collapse Certificate
   Check whether collapse into a branch is earned. Preserve structured reasons:
   unresolved rivals, quotient-resolved rivals, hiddenness, burden blockers,
   resolver support, recursion demand, grey still operative, fail-closed / non-evidential status.

9. Commitment Surface / Readout
   Express the certified branch collapse as a native action. High local scalar
   support may not override active structural blockers without a documented rule.

10. Environment update / next loop
   Execute the action, receive new observation, update public state, and repeat.
```

## Active primitives/elements by role

```text
Bend:
  local deformation of continuation possibility.

Gauge / HAQ tolerance:
  local comparison, quotient, hiddenness, and collapse sensitivity.

Temporal retention:
  what persists across loops and transformations.

ReID / identity-through-change:
  continuation identity across changing action expressions.

Remaining transformation burden:
  unresolved continuation-relevant pressure.

Change operators:
  carry, amplify, expose, mask, buffer, relieve, cancel, transfer, transform.

Closure / quotient:
  when remaining differences no longer matter for active continuation.

Thin collapse:
  legitimate compression of live structure into row, scalar, branch, certificate, or action.
```

Runtime surfaces instantiate these roles; they are not themselves deep ontology primitives.

## Forbidden runtime shortcuts

```text
candidate = action = branch;
branch relation from action names alone;
weak decision-slot competition as strong rivalry;
burden as reward/cost score;
quotient from raw scalar similarity;
collapse as score-maximum selection;
baseline-policy rescue or first-legal rescue;
adapter-side policy relation such as "repair is best now".
```

## Acceptance gate for code

A runtime path satisfies this target only if diagnostics show:

```text
public_effects are leakage-safe;
branch-internal operations survive without cross-branch relations;
relations are typed and not dominated by false strong rivalry;
RCF field deltas trace to burden operations and relations;
CollapseCertificate carries structured reasons;
CommitmentSurface respects certificate gates;
no non-CO rescue selector contributes to evidence-bearing runs;
readout-affecting scalars have formula-ledger entries.
```

## Open status

This contract specifies the current target architecture. It does not solve:

```text
complete burden operation composition laws;
exact quotient tolerance calibration;
recursion scheduler/budget;
six-question prior minimality/sufficiency;
full formula derivation;
full algorithm comparison;
consciousness/meaning theory.
```

Those are scoped as formal, empirical, or later theoretical work rather than hidden assumptions.
