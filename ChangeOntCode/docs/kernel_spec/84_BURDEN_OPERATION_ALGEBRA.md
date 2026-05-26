# 84. Burden Operation Algebra

Status: conceptual/kernel contract; no runtime implementation claim.

This document binds:

```text
TheoryOfChange_main/01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md
TheoryOfChange_main/01_Statements/Definition/S-DF-delta-field-tension.md
TheoryOfChange_main/01_Statements/Derivation/S-DR-burden-as-anchored-operative-tension.md
TheoryOfChange_main/01_Statements/Clarification/S-CL-burden-operation-table-and-stress-tests.md
```

to the kernel-side RelationSurface and RCF design.

---

## 1. Contract definition

Burden is anchored operative tension:

```text
burden = residual transformation pressure carried by a continuation relative to a condition of admissible continuation
```

The refined field-asymmetry formulation is:

```text
burden = continuation-relevant de-centering of a retained structure in a changing relational field
```

Tension is more primitive than burden. Tension becomes burden only when it is operative for continuation admissibility, branch relation, quotient, grey preservation, recursion, or collapse.

---

## 2. Burden is not merely magnitude

A kernel burden record must not collapse burden into one scalar. Burden requires at least these semantic roles, even if implementation names differ:

```text
burden_id
burden_type
carrier_branch_or_candidate
continuation_anchor
pressured_condition
tension_source
scale
coupling
operation_status
scope
visibility_status
direction_or_relief_vector
gradient_or_pressure_strength
barrier_or_access_cost
basin_status
threshold_status
history_or_momentum_trace
magnitude_or_ordinal
public_basis
resolution_class
leakage_status
```

`magnitude_or_ordinal` is not the identity of the burden. The identity is defined by pressured condition, transformation/resolution class, coupling, and local comparison regime.

---

## 3. Burden type identity

Two burden records count as same-type only when:

```text
1. they pressure the same continuation/admissibility/closure condition;
2. the same class of transformations can relieve, cancel, expose, transfer, transform, absorb, or buffer them;
3. their scopes overlap or are comparable under the active local regime;
4. treating them as same-type does not erase operative relation/collapse differences.
```

Source alone is not identity. Quantity alone is not identity. Same-size perturbations can differ radically by closure position, coupling, barrier, basin, and threshold status.

---

## 4. Operations

The initial operation set is:

```text
carry
amplify
expose
mask_or_postpone
relieve
cancel
transfer
transform
absorb_or_buffer
threshold_or_phase_shift
```

### carry
The branch continues while keeping burden active.

### amplify
The branch increases same-type burden, urgency, gradient, or criticality.

### expose
The branch or observation makes hidden burden visible to the field.

### mask_or_postpone
The branch lowers apparent urgency or preserves local support while burden remains unresolved.

### relieve
The branch reduces same-type burden while preserving the relevant continuation condition.

### cancel
The branch removes or resets the condition under which the burden is active.

### transfer
The burden changes carrier or scope without changing type.

### transform
The burden changes type because the unresolved requirement changes form.

### absorb_or_buffer
The structure routes or averages incoming tension so it does not become operative burden at the active scale.

### threshold_or_phase_shift
The burden regime changes discontinuously because a closure, barrier, coupling, or phase boundary is crossed.

---

## 5. Buffering, masking, and stability

The kernel must distinguish buffering from masking.

```text
buffering:
ordinary tension is absorbed/routed and does not become operative burden.

masking:
operative burden remains but appears locally harmless, low-urgency, or well-supported.
```

This distinction is essential for stability. A stable continuation is not burden-free because no change occurs. It is stable because ordinary tensions are handled without becoming identity-breaking burden.

---

## 6. Direction, barrier, basin

A burden can point toward different operation classes:

```text
toward relief
away from overload
toward exposure
around a barrier
toward cancellation/reset
toward quotient/collapse
into grey preservation / recursion
```

A candidate may have a clear relief direction but a high barrier. Therefore burden relief and accessible relief are distinct.

Required conceptual distinctions:

```text
residual burden       ≠ available relief path
available relief path ≠ low barrier
low barrier           ≠ earned collapse
```

---

## 7. Relation derivation from burden operations

RelationSurface should derive relations from public burden/effect facts and burden operations.

```text
A carries/amplifies burden X.
B relieves burden X.
→ relief(B, A)
```

```text
A carries burden condition X.
B cancels/resets condition X.
→ cancellation(B, A)
```

```text
A's collapse depends on hidden burden X.
B exposes X.
→ exposure / hiddenness-reduction relation
```

```text
A masks burden X.
B exposes or relieves X.
→ anti-masking / diagnostic relation
```

```text
A buffers tension T that would otherwise become burden for B.
→ shielding / buffering proximity relation
```

```text
A and B pressure mutually incompatible admissibility conditions.
→ rivalry(A, B)
```

```text
A and B preserve same burden profile under active continuation tolerance.
→ quotient/equivalence(A, B)
```

```text
A crosses a threshold that changes B's burden regime.
→ critical-proximity / phase-shift relation(A, B)
```

---

## 8. Adapter boundary

Adapters may publish public burden/effect facts. They must not publish policy-shaped relation conclusions.

Allowed:

```text
this transition can increase degradation
this action can reduce hiddenness
this observation reveals variable X
this move is blocked by public topology
this action consumes public resource
this transition can buffer ordinary variation below threshold
this transformation can reset condition X
```

Forbidden:

```text
this branch is optimal
repair should be selected now
this is the shortest hidden route
hidden state says replace
DP value says choose this
```

---

## 9. Family stress tests

### Maintenance

```text
RUN      → carry/amplify degradation burden when degradation pressure is operative
INSPECT  → expose hiddenness/degradation burden
REPAIR   → relieve degradation burden while preserving machine-continuation
REPLACE  → cancel/reset prior degradation condition; may transform into resource/restart burden
WAIT     → carry, buffer, mask, or relieve phase/time burden depending on declared dynamics
FAILURE  → threshold/phase-shift after accumulated burden crosses admissibility boundary
```

### Maze

```text
open corridor             → low or buffered route burden
blocked route discovered  → expose hidden topology burden
continue blocked route    → carry/amplify obstruction burden
detour                    → transfer route burden into path-length/commitment burden
opened/bypassed route     → relieve/cancel obstruction burden
equivalent routes         → quotient
non-equivalent chokepoints → grey/recursion pressure
```

### Bandit

```text
exploit with unresolved alternatives → carry/mask uncertainty burden
sample arm/class                    → expose/relieve uncertainty burden
poor sample evidence                → transform hiddenness into exclusion/rivalry
sufficient equivalence              → quotient/collapse
high reward with unresolved unknowns → possible masking, not automatic relief
```

### Renewal

```text
stable phase          → carry bounded burden / buffer ordinary fluctuation
past degradation      → amplify cycle/degradation burden
phase wait/alignment  → relieve cycle-phase burden when alignment improves
reset/renew           → cancel/transform accumulated burden
hidden phase          → expose/preserve grey
threshold crossing    → phase-shift of burden regime
```

---

## 10. Required diagnostics before runtime evidence

Before claiming burden-aware kernel behavior, tests should show:

1. low-cost high-burden branches do not collapse merely because score is high;
2. high-cost relief/cancellation can be field-relevant even when immediate score is lower;
3. masking is not relief;
4. buffering is not masking;
5. exposure can increase short-term apparent burden while improving collapse legitimacy;
6. relief requires same-type burden overlap;
7. cancellation differs from relief;
8. same source can produce multiple burden types;
9. different sources can produce same burden type;
10. threshold/phase-shift differs from smooth amplification;
11. same scalar score and same scalar burden magnitude can produce different outcomes if direction/barrier/relation topology differs;
12. relation topology changes behavior when scalar candidate scores are held fixed.

---

## 11. Paper-risk boundary

A result is not evidence for burden-aware CO if:

- burden is only immediate reward/cost;
- burden type is only an action-name label;
- burden is a scalar with no direction/barrier/coupling structure;
- relief is inferred from low burden or high stability alone;
- buffering and masking are conflated;
- cancellation and relief are indistinguishable;
- threshold behavior is smoothed away without justification;
- masking/postponement counts as resolution;
- relation topology has no effect independent of scalar score;
- adapters publish optimality conclusions as burden facts.

---

## 12. Current status

This is a conceptual and kernel-contract closure. The current runtime contains first-pass branch-internal operation carriers and RelationSurface-derived operation summaries, but this file is stronger than the implementation. Full operation-composition laws, formula grounding, and broader counterexample diagnostics remain open before performance claims.


## Runtime carrier alignment

See `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md`. Public burden/effect facts must not disappear when they do not form a cross-branch relation. Branch-internal operations are first-class kernel carriers, while weak decision-slot competition remains procedural telemetry rather than strong rivalry or a collapse blocker.
