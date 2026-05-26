# 86. Minimal Burden Formal Skeleton

Status: formal/kernel scaffold; no runtime implementation claim.

This document binds:

```text
TheoryOfChange_main/01_Statements/Derivation/S-DR-minimal-burden-formal-skeleton.md
TheoryOfChange_main/01_Statements/Clarification/S-CL-burden-algebra-laws-counterexamples-and-non-laws.md
84_BURDEN_OPERATION_ALGEBRA.md
85_RELATION_TO_COLLAPSE_DIAGNOSTIC_CONTRACT.md
```

to the next architecture step.

---

## 1. Purpose
The prior burden files define burden as anchored operative tension and list burden operations. This file gives the minimal formal skeleton that a kernel implementation must respect before burden algebra is treated as more than terminology.

This is not a completed algebra. It is the minimum shape of one.

---

## 2. Formal roles
A burden record is not a scalar. It must preserve enough structure to distinguish burden identity, operation, relation derivation, quotient, and collapse.

Minimal burden record roles:

```text
carrier_branch
anchor
pressured_condition
burden_type
scope
visibility
coupling
direction
barrier
basin_status
threshold_status
history_trace
magnitude_or_ordinal
public_basis
resolution_class
```

A runtime may use different field names, but it must be able to recover these roles in telemetry or tests.

---

## 3. Identity and order

### Burden type identity
Two burden records are same-type only if:

```text
they pressure the same continuation/admissibility/closure condition;
they are altered by the same class of transformations;
their scopes are comparable under the active regime;
combining them does not erase operative relation/collapse differences.
```

### Burden order
Burden order is local and partial:

```text
b1 ⪯ b2
```

means `b1` carries no more unresolved transformation pressure than `b2` for the same anchor, pressured condition, and operation class.

No global burden scalar is canonical at this stage.

---

## 4. Operation signatures
The runtime implementation may approximate these, but the conceptual signatures are:

```text
carry(branch, burden) -> burden
amplify(branch, burden, delta) -> burden
expose(branch, hidden_burden) -> visible_burden
mask(branch, burden) -> masked_burden
buffer(branch, tension) -> no_burden_or_reduced_burden
relieve(branch, burden) -> reduced_same_type_burden
cancel(branch, burden) -> resolved_old_burden + possible_new_burdens
transfer(source_branch, target_branch, burden) -> burden_on_target
transform(burden_x) -> burden_y
phase_shift(burden, regime) -> burden_prime, regime_prime
```

---

## 5. Required laws

A future implementation must preserve these distinctions:

```text
exposure is not relief;
masking is not buffering;
stability is not relief;
source is not burden identity;
magnitude is not burden identity;
local reward improvement is not burden relief;
cancellation may create new burdens;
phase-shift may change comparison regime;
operation order may matter.
```

---

## 6. Relation derivation rules
RelationSurface should derive named relations from burden operations rather than receiving policy-shaped relation conclusions.

Examples:

```text
A carries/amplifies burden X
B relieves X
=> relief(B, A)
```

```text
B cancels the condition under which A carries X
=> cancellation(B, A)
```

```text
B exposes hidden burden X relevant to A's collapse
=> exposure(B, A)
```

```text
A and B have mutually incompatible admissibility conditions
=> rivalry(A, B)
```

```text
A and B preserve equivalent burden profiles under active tolerance
=> quotient_equivalence(A, B)
```

These rules are kernel-side. Adapters may publish public effect facts, not policy conclusions.

---

## 7. Quotient and collapse preservation targets

### Quotient target
Quotienting is allowed only when remaining burden differences no longer change:

```text
admissibility;
relation topology;
recursion demand;
grey preservation;
collapse consequence;
action expression under readout.
```

### Collapse target
Collapse is earned only if burden and relation structure no longer require preserved grey or recursion.

A scalar `collapse_readiness` may summarize this only after the logical components are available:

```text
branch_identity_stable
burden_resolved_or_bounded
rivals_quotient_canceled_or_nonoperative
hiddenness_within_tolerance
relation_topology_no_longer_demands_recursion
grey_difference_nonoperative
fallback_not_evidence_bearing
```

---

## 8. Counterexample obligations
Before broad family benchmark claims, implementations must pass toy cases for:

```text
low visible burden but masked residual burden;
high cost but true relief;
same source different burdens;
different sources same burden;
exposure worsening visible state;
relief versus cancellation;
dense equivalent path quotient;
dense non-equivalent grey preservation;
tiny threshold perturbation;
stable but burdened branch.
```

These cases are mechanism-validity tests, not reward benchmarks.

---

## 9. Open formal questions
The following remain open and must not be silently assumed by code:

```text
whether operations reduce to a smaller algebra;
whether burden records form a useful semiring/quantale/residuated structure;
how exact quotient tolerance is computed;
how recursion demand is bounded;
how scalars are calibrated without hidden scoring;
how the mechanism differs from known algorithms in formal terms.
```

---

## 10. Current implementation implication
The safe next step remains controlled diagnostics, not broad benchmarking. First-pass carriers exist, but further toy and ablation diagnostics must instantiate this skeleton and check that relation topology and burden operations change quotient/grey/recursion/collapse behavior independently of scalar candidate scores.
