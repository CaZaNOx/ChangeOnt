---
id: stmt.burden-algebra-laws-counterexamples-and-non-laws
type: CL
aliases:
- S-CL-burden-algebra-laws-counterexamples-and-non-laws
- BurdenAlgebraCounterexamples
- BurdenNonLaws
title: Burden algebra laws, counterexamples, and non-laws
concepts:
- '[[02_Concepts/C-change-trace-invariants]]'
dependencies:
- '[[01_Statements/Derivation/S-DR-minimal-burden-formal-skeleton.md]]'
parents:
- '[[01_Statements/Derivation/S-DR-minimal-burden-formal-skeleton.md]]'
successors:
- '[[../ChangeOntCode/docs/kernel_spec/86_MINIMAL_BURDEN_FORMAL_SKELETON.md]]'
flags:
- counterexample-gate
- no-runtime-implementation-claim
tags:
- layer/foundations
- domain/formal
- type/CL
- concept/burden
- concept/algebra
- status/canonical-scaffold
status: canonical-scaffold
---
# Burden algebra laws, counterexamples, and non-laws

## Purpose
This clarification prevents the burden algebra from becoming fake rigor. A burden formalism is useful only if it has explicit laws, explicit non-laws, and counterexamples that can break incorrect implementations.

---

## 1. Minimal laws

### Law 1: Burden is anchor-relative
No burden token is meaningful without a continuation anchor or admissibility condition.

A quantity may be measured without an anchor, but it is not a CO burden until it matters for continuation.

### Law 2: Burden is field-relative
A burden token is defined relative to local scale, coupling, barrier, basin, and comparison regime. The same perturbation can be irrelevant, buffered, amplifying, or regime-shifting depending on this field placement.

### Law 3: Burden type is operation-relative
Burden type is identified by the pressured continuation condition plus the class of transformations that can alter the burden-status. Source and size are insufficient.

### Law 4: Exposure is not relief
A hidden burden can become visible without being reduced. This may increase visible burden while improving field truthfulness.

### Law 5: Masking is not buffering
Masking hides or postpones operative burden. Buffering absorbs or routes tension so it does not become operative burden at the active scale.

### Law 6: Relief preserves relevant continuation
Relief lowers same-type burden while preserving enough of the continuation profile for identity-through-change.

### Law 7: Cancellation can terminate a burden condition
Cancellation removes or resets the condition under which burden remains active. It may create new burdens.

### Law 8: Phase shifts can break local ordering
A small change can alter the burden regime if it crosses a threshold, closure, coupling, or barrier boundary.

---

## 2. Non-laws
The following are forbidden assumptions.

```text
burden = cost
burden = uncertainty
burden = negative reward
burden = scalar distance
burden = source label
burden = discomfort
burden = low score
```

Also forbidden:

```text
all burdens can be added;
all burdens are comparable;
all local improvements are relief;
all stability is relief;
all exposure is improvement;
all recurrence is stability;
all path density demands recursion.
```

---

## 3. Counterexample set

### C1. Low visible burden, high masked burden
A branch has high immediate reward and low visible instability while accumulating hidden degradation. The algebra must classify this as masking/postponement, not relief.

### C2. High local cost, true burden relief
A repair/reset action has high immediate cost but lowers the burden that blocks future continuation. The algebra must not mistake high cost for high burden.

### C3. Same source, different burdens
A blocked door may create topological obstruction burden, hiddenness burden, and revision burden. The source is one, but the burden types differ.

### C4. Different sources, same burden
Wear, shock, and overuse can all create same-type degradation burden if the same repair/reset class addresses the same continuation pressure.

### C5. Exposure worsens visible state
Inspection can reveal that the current branch is worse than believed. Visible burden rises, but collapse legitimacy improves because hiddenness is reduced.

### C6. Relief versus cancellation
Repair relieves degradation while preserving machine-continuation. Replacement cancels the prior degradation condition but may create reset/resource burden.

### C7. Dense equivalent paths
Many locally distinct paths preserve the same residual burden profile. The correct operation is quotient, not recursion explosion.

### C8. Dense non-equivalent paths
Many paths differ in burden type, barrier, or collapse consequence. The correct operation is grey preservation or bounded recursion, not premature quotient.

### C9. Tiny threshold perturbation
A small change crosses a closure or barrier boundary and changes the burden regime. Size alone cannot predict burden effect.

### C10. Stable but burdened
A branch appears stable because perturbations are masked or buffered locally, but it may still carry unresolved future burden. Stability is not automatically relief.

---

## 4. Use in kernel diagnostics
Any future RelationSurface / RCF implementation should include toy cases corresponding to this counterexample set. Reward performance is not a substitute for passing them.

If implementation cannot distinguish these cases, the burden algebra has not been implemented; the runtime is likely using scalar scoring with CO names.
