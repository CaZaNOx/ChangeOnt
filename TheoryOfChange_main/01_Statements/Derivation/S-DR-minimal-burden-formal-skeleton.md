---
id: stmt.minimal-burden-formal-skeleton
type: DR
aliases:
- S-DR-minimal-burden-formal-skeleton
- MinimalBurdenAlgebra
- BurdenFormalSkeleton
title: Minimal burden formal skeleton
concepts:
- '[[02_Concepts/C-change-trace-invariants]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
- '[[01_Statements/Definition/S-DF-delta-field-tension.md]]'
- '[[01_Statements/Derivation/S-DR-burden-as-anchored-operative-tension.md]]'
- '[[01_Statements/Clarification/S-CL-burden-operation-table-and-stress-tests.md]]'
- '[[01_Statements/Derivation/S-DR-burden-relations-to-quotient-collapse-and-recursion.md]]'
parents:
- '[[01_Statements/Derivation/S-DR-burden-as-anchored-operative-tension.md]]'
- '[[01_Statements/Clarification/S-CL-burden-operation-table-and-stress-tests.md]]'
successors:
- '[[../ChangeOntCode/docs/kernel_spec/86_MINIMAL_BURDEN_FORMAL_SKELETON.md]]'
flags:
- formal-scaffold-not-final-algebra
- no-runtime-implementation-claim
tags:
- layer/foundations
- domain/formal
- type/DR
- concept/burden
- concept/algebra
- concept/kernel-bridge
- status/canonical-scaffold
status: canonical-scaffold
---
# Minimal burden formal skeleton

## Claim
The burden-operation doctrine can be sharpened into a minimal formal skeleton without yet pretending to possess a completed algebra.

The purpose of this skeleton is to prevent burden from collapsing into a single scalar score while also preventing burden language from remaining only metaphorical.

The skeleton defines:

```text
burden tokens;
burden type identity;
a partial order of burden within comparable regimes;
operation signatures;
minimal preservation laws;
known non-laws;
quotient and collapse dependencies.
```

It does not yet define a final semiring, quantale, residuated lattice, metric, or complete operation algebra. Those may become appropriate only after the skeleton survives examples and counterexamples.

---

## 1. Background derivation
`../02_Outer_Formation/014_S-DF-remaining-transformation-burden.md` defines burden as what still has to change for a present unfolding to reach a supportable continuation.

`S-DR-burden-as-anchored-operative-tension.md` refines this as anchored operative tension: a retained structure is de-centered in a changing relational field, and that de-centering becomes burden only when it is operative for continuation.

Therefore a burden is not merely:

```text
cost;
negative reward;
uncertainty;
distance;
difficulty;
amount of change.
```

A burden is a structured residual requirement relative to a continuation condition.

---

## 2. Minimal objects
Let the following be conceptual roles, not yet final mathematical objects.

### Continuation anchor
`A` := the condition, task-anchor, closure, viability condition, or admissibility criterion relative to which continuation matters.

Examples:

```text
reach the goal;
maintain machine function;
preserve identity-through-change;
reduce hiddenness enough to commit;
keep a path admissible;
retain a subject-relevant salience structure.
```

### Branch
`p, q, r` := retained continuation-pressure signatures, not one-step action labels.

### Tension
`τ` := field asymmetry or relational de-centering around a retained structure.

### Burden token
A burden token may be written schematically as:

```text
b = ⟨carrier, anchor, pressured_condition, type, scope, visibility,
     direction, coupling, barrier, basin, threshold, magnitude,
     history, public_basis⟩
```

Not every implementation must use these field names. The point is that burden identity cannot be reduced to `magnitude`.

### Zero / resolved burden
`0_A` := no operative residual transformation pressure relative to anchor `A` at the current scale and tolerance.

This is not universal nothingness. It is local resolvedness relative to an anchor.

---

## 3. Burden type identity
Two burden tokens `b1` and `b2` count as same-type under regime `ρ` only if:

```text
1. they pressure the same continuation/admissibility/closure condition or a declared equivalent class of such conditions;
2. the same class of transformations can relieve, cancel, expose, transfer, transform, absorb, or buffer them;
3. their scopes are overlapping or comparable under the active regime;
4. treating them as same-type does not erase an operative difference for relation, quotient, recursion, or collapse.
```

This yields a relative equivalence relation:

```text
b1 ≡_ρ b2
```

where `ρ` includes local scale, anchor, tolerance, and comparison regime.

Source is not identity. Quantity is not identity. Same source may produce several burdens; different sources may produce same-type burden.

---

## 4. Burden order
Burden comparison is not global total ordering.

Within a comparable burden type and local regime, define:

```text
b1 ⪯_ρ b2
```

as:

```text
b1 carries no more unresolved transformation pressure than b2
relative to the same anchor, condition, and operation class.
```

This is at most a preorder or partial order, not a universal scalar ranking.

Across unrelated burden types, comparison must not be forced unless a collapse certificate or regime rule specifies a lawful projection.

This prevents the common failure:

```text
degradation burden = 0.4
hiddenness burden = 0.4
therefore same burden
```

That inference is invalid unless the local regime defines a comparable projection.

---

## 5. Operation signatures
The initial burden operations are partial maps. They are not guaranteed to apply in every context.

### carry
```text
carry(p, b) → b'
```

The branch `p` keeps burden `b` active. Usually `b' ≡_ρ b`; magnitude, threshold, or history may change.

### amplify
```text
amplify(p, b, δ) → b'
```

Same-type burden increases in urgency, magnitude, gradient, threshold criticality, or collapse consequence.

### expose
```text
expose(p, b_hidden) → b_visible
```

Hidden or masked burden becomes field-visible. Exposure is not relief.

### mask_or_postpone
```text
mask(p, b) → b_masked
```

Local apparent burden decreases or urgency is deferred while residual transformation pressure remains. This must not be counted as relief.

### absorb_or_buffer
```text
buffer(p, τ) → 0_A  or  b_reduced
```

Incoming tension is routed, averaged, or absorbed so it either does not become operative burden at the active scale or becomes lower burden. Buffering is not masking because residual burden is actually prevented or lowered.

### relieve
```text
relieve(q, b) → b'
```

A branch or transformation reduces same-type burden while preserving the relevant continuation condition.

Relief law:

```text
if relieve(q, b) = b' then b' ⪯_ρ b
```

provided same-type comparability holds.

### cancel
```text
cancel(q, b) → 0_A + B_new?
```

A transformation removes or resets the condition under which `b` remains active. Cancellation may create a new burden set `B_new` under a different anchor or condition.

### transfer
```text
transfer(p, q, b) → b_q
```

Burden changes carrier or scope without changing type.

### transform
```text
transform(b_x) → b_y
```

Burden changes type because the unresolved requirement changes form. Type need not be preserved.

### threshold_or_phase_shift
```text
phase_shift(b, ρ) → (b', ρ')
```

A closure, barrier, coupling, or phase boundary changes the local comparison regime itself.

---

## 6. Minimal preservation laws
These laws are provisional but conceptually necessary for the current kernel direction.

### L1. Source non-identity
Source does not determine burden identity.

### L2. Magnitude non-identity
Magnitude does not determine burden identity.

### L3. Exposure is not relief
Making burden visible does not by itself reduce the residual transformation requirement.

### L4. Masking is not buffering
Masking lowers apparent urgency while residual burden remains; buffering prevents or lowers operative burden.

### L5. Relief preserves continuation condition
Relief reduces burden while preserving enough of the relevant continuation condition to count as continuation of that branch/profile.

### L6. Cancellation need not preserve branch identity
Cancellation may remove the condition that sustained the burden and may reset or terminate the prior branch identity.

### L7. Transformation may change burden type
When the unresolved requirement changes form, same-type comparison may no longer apply.

### L8. Thresholds can change order
Crossing a threshold may change the comparison regime; monotonic assumptions must be revalidated after phase-shift.

---

## 7. Known non-laws
These must not be assumed.

### N1. Burdens are not globally additive
Two burdens cannot always be summed into one scalar without losing operative structure.

### N2. Burdens are not globally comparable
Hiddenness burden and degradation burden are not comparable unless a local projection is explicitly justified.

### N3. Operations need not commute
Example:

```text
expose then relieve ≠ relieve then expose
```

because hidden burden may not be available for relief before exposure.

### N4. Local reduction need not be global relief
An operation can reduce visible burden while increasing masked or future burden.

### N5. Stability is not relief
A stable branch may carry unresolved burden; comfort, local support, or low visible turbulence is not evidence of relief.

---

## 8. Relation derivation
Branch relations derive from burden operations rather than arbitrary labels.

```text
if p carries/amplifies b_x
and q relieves b_x
then relief(q, p)
```

```text
if q cancels the condition under which p carries b_x
then cancellation(q, p)
```

```text
if q exposes hidden b_x relevant to p's collapse
then exposure(q, p)
```

```text
if p and q pressure mutually incompatible admissibility conditions
then rivalry(p, q)
```

```text
if changes in p alter q's burden, admissibility, quotient status, recursion demand, or collapse status
then proximity(p, q)
```

```text
if p and q preserve equivalent burden profiles under active tolerance
then quotient_equivalence(p, q)
```

---

## 9. Quotient dependency
Two branches may quotient only if their burden differences are nonoperative relative to the active anchor and tolerance.

A first criterion:

```text
p ~_ρ q
```

only if differences between their burden profiles do not change:

```text
continuation admissibility;
relation topology;
recursion demand;
grey preservation;
collapse consequence;
public action expression under the active readout.
```

This is not yet an algorithm. It is the preservation target for later kernel approximation.

---

## 10. Collapse dependency
Collapse is not warranted by scalar burden reduction alone.

A collapse certificate must inspect:

```text
branch identity stability;
burden resolved / bounded / relieved / canceled;
non-equivalent rivals absent or nonoperative;
hiddenness within tolerance;
relation topology no longer requiring recursion;
grey differences no longer operative;
fallback not evidence-bearing.
```

The formal skeleton therefore implies that `collapse_readiness` may be a scalar summary only after these logical components have been separately available.

---

## 11. Counterexample obligations
Any proposed implementation of this skeleton must survive these counterexamples:

```text
low visible burden but masked residual burden;
high immediate reward but growing transformation burden;
exposure that worsens visible state but improves collapse legitimacy;
relief that preserves branch identity;
cancellation that resets branch identity;
same source producing multiple burden types;
different sources producing same-type burden;
dense equivalent paths requiring quotient;
dense non-equivalent paths requiring grey/recursion;
threshold crossing where small perturbation changes regime.
```

Failure on these cases means the implementation is probably still cost/scalar scoring.

---

## 12. Status
This file closes the first formal skeleton. It does not close the full algebra.

Still open:

```text
whether burden operations reduce to a smaller algebra;
whether a useful semiring/quantale/residuated form exists;
how quotient tolerance is computed locally;
how recursion demand is bounded;
how scalar projections are justified and calibrated;
how this compares to known algorithms.
```
