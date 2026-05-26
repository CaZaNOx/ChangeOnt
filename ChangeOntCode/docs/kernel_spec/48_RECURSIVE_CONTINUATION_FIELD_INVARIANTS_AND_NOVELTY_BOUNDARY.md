# 48. Recursive Continuation Field Invariants and Novelty Boundary

Status: active first-pass invariant and novelty-boundary contract.

This file converts `47_RECURSIVE_CONTINUATION_FIELD.md` from doctrine into a testable contract. It also states the novelty boundary honestly: the recursive continuation field is not novel because it branches, searches, propagates messages, merges states, or allocates computation. Those all have known algorithmic relatives. Its possible CO-native contribution is the way those operations are organized around **identity-through-change**, **remaining transformation burden**, **continuation debt**, **quotient-aware grey preservation**, and **earned collapse**.

This file began as a pre-implementation invariant boundary and remains the standard for the first-pass implementation. If implementation pressure contradicts this file in order to improve a benchmark, the implementation is suspect; if implementation reveals a legitimate conceptual correction, update this file explicitly rather than letting code drift silently.

---

## 1. What would be CO-native here?

A CO-native recursive continuation field is not a planner with renamed variables. It is a runtime field whose basic unit is:

```text
continuation identity under change
```

not:

```text
state, action, value, reward, policy, tree node, message, or option label
```

The field may reuse known algorithmic tools, but the organizing law must be:

```text
A branch remains live only to the degree that its identity-through-change remains supportable under accumulated burden, debt, fracture, uncertainty, and quotient instability.

Collapse is lawful only when the unresolved grey field no longer carries enough structurally relevant burden/rivalry/hiddenness/equivalence ambiguity to justify retention.
```

### 1.1 Candidate CO-native mechanic

The strongest candidate mechanic is:

```text
continuation-debt field with quotient-aware grey preservation
```

Meaning:

1. A branch can retain high local support while accumulating unresolved transformation burden.
2. That unresolved burden becomes continuation debt.
3. Debt is relational: it can raise relief-branch viability, spread recursion demand to nearby rivals, cancel through compensating transformations, merge away through quotient/equivalence, or lower collapse readiness.
4. Collapse is not `argmax(score)`. Collapse is the earned reduction of a live continuation field when retention no longer changes lawful continuation.

If this reduces to ordinary value backup, MCTS rollout, active-inference expected-free-energy minimization, message passing, or options selection without a distinct debt/quotient/collapse law, then it is not a new kernel mechanic. It may still be useful, but the novelty claim fails.

---

## 2. What is not novel and must not be oversold

The following are not, by themselves, novel:

- keeping multiple paths live;
- expanding some branches more than others;
- propagating influence across a graph;
- merging equivalent states;
- weighting future cost;
- delaying a decision under uncertainty;
- using a task anchor or public goal signal;
- allocating more compute to harder cases;
- choosing an action after scoring candidates.

Known relatives include tree search / MCTS, dynamic programming, belief propagation, graph message passing, active inference, options, successor representations, beam search, particle filtering, and adaptive/anytime computation.

Therefore, an implementation may borrow from those methods, but it cannot claim CO novelty merely because it uses them.

---

## 3. The invariants the field must satisfy

These invariants are abstract. They must be tested using anonymous branches such as `A`, `B`, `C`, `SAMPLE`, `RELIEF`, not maintenance-specific names such as `RUN` or `REPAIR`.

### INV-48.1 Support is not viability

Given two branches with equal local support, if branch `A` has a rising burden/debt trend and branch `B` does not, `A`'s continuation viability must decrease relative to `B` even before immediate local support collapses.

```text
same local support + rising burden/debt
→ lower continuation viability
→ lower collapse readiness
```

### INV-48.2 Debt creates relief pressure

If branch `A` accumulates debt and branch `B` is generically marked as relieving the type of burden carried by `A`, then `B` must gain field viability or recursion priority even if `B` has lower immediate local support.

```text
debt(A) rises + relief_relation(B, A) > 0
→ viability(B) rises or collapse_delay(A) rises
```

### INV-48.3 Grey preservation under close unresolved rivals

If two or more branches are close in viability and unresolved burden/hiddenness/consequence is high, collapse must be delayed or recursion depth increased locally.

```text
near tie + high unresolved relevance
→ grey preserved
→ local recursion depth / sampling demand increases
```

### INV-48.4 Cheap collapse in flat reliable regions

If local cue reliability is high, hiddenness is low, burden/debt is low, rivals are clearly dominated, and revision cost/consequence span are low, the field should collapse cheaply.

```text
flat low-risk field
→ low recursion depth
→ collapse allowed
```

### INV-48.5 Shape controls recursion, not action presets

Changing shape-derived controls may alter recursion depth, debt sensitivity, grey preservation, and collapse readiness. It must not directly assign action preferences.

```text
same anonymous branches + different controls
→ different field dynamics
not: direct action-name boost
```

### INV-48.6 Proximity modulates branch influence

Branch influence must depend on structural proximity, not merely action labels. Structural proximity may include shared burden, shared evidence, shared attractor relation, reachability, quotient similarity, or common bottleneck.

```text
same relation strength + higher structural proximity
→ stronger influence
hard boundary / nonshared burden
→ weaker influence
```

### INV-48.7 Quotient / merge prevents duplicate futures

If two branches become same-enough under public state, remaining burden, and active identity tolerance, the field should merge them or share state rather than treating them as independent decisive futures.

```text
equivalent remaining continuation
→ quotient / merge / shared viability
```

### INV-48.8 Cancellation lowers debt

If a branch performs a compensating transformation that cancels prior debt, debt must fall unless new burden is introduced.

```text
debt_vector + compensating transformation
→ lower continuation debt
```

### INV-48.9 Hiddenness increases sampling pressure

If hidden decisiveness is high and local cue reliability is low, sampling/reopening branches must gain field viability or recursion priority, provided they are admissible.

```text
high hidden_decisiveness + low local_cue_reliability
→ sampling viability / recursion increases
```

### INV-48.10 Anti-smuggling invariant

The canonical field implementation must not branch on family name, action-name-specific policy labels, hidden simulator state, oracle shortest paths, value-iteration / DP / UCB outputs, threshold/control-limit verdicts, or benchmark-regime labels as policy.

---

## 4. Diagnosis contract

The recursive continuation field must make failures localizable:

```text
public packet
→ shape_prior6 / direct controls
→ candidate facts / ContinuationState
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
→ action
```

The field must emit telemetry sufficient to ask:

1. Did public evidence contain burden/debt information?
2. Did direct controls alter field dynamics?
3. Did branches interact through debt, relief, proximity, quotient, or cancellation?
4. Did grey preservation activate where rivals were close and unresolved?
5. Did collapse happen because the field was stable, or because a local score dominated too early?
6. Did the chosen action express a continuation identity, or only a one-step action score?

If telemetry cannot answer these, the implementation is not yet a valid test of the doctrine.

---

## 5. Minimal executable abstraction before family tests

Before maintenance, maze, bandit, renewal, robot, or simulator benchmarks are used as evidence, the field must pass abstract synthetic tests:

1. rising-debt branch;
2. relief branch;
3. close grey rivals;
4. flat easy field;
5. quotient pair;
6. cancellation;
7. proximity;
8. shape modulation;
9. anti-smuggling scan.

Only after these pass should family-level performance be interpreted.

---

## 6. What would count as evidence of novelty?

Evidence of novelty is not higher reward alone.

A credible novelty case requires:

1. The same field law applies across unrelated task families.
2. Branch interaction is explained by continuation debt, relief, quotient, proximity, and grey preservation rather than family policy.
3. The field behaves differently from simple action scoring, value backup, or tree expansion in controlled synthetic cases.
4. Ablations show that removing debt/quotient/grey-preservation mechanics collapses behavior toward known baselines or local scoring.
5. The implementation can state when it is merely reusing a known subroutine versus when CO-specific field law is doing work.

If these are not shown, the honest claim is:

```text
CO provides a philosophical synthesis and architecture scaffold, not yet a new algorithmic kernel.
```

If these are shown, the plausible claim is:

```text
CO contributes a recursive continuation-field mechanic: a shape-conditioned collapse law over identity-through-change, continuation debt, branch interaction, quotient/merge, cancellation, and grey preservation.
```

---

## 7. Implementation boundary for `RecursiveContinuationField v1`

Allowed first-pass capabilities:

- consume anonymous branch rows from `ContinuationState` / `CandidateSurface`;
- compute structural proximity between branches from public fields;
- propagate debt to relief branches through generic relation weights;
- increase recursion/collapse-delay for close unresolved rivals;
- merge quotient-equivalent branches where explicit same-enough public structure exists;
- reduce debt through cancellation relation;
- emit field-adjusted viability and collapse-readiness telemetry.

Forbidden first-pass capabilities:

- roll out hidden futures without public basis;
- run family-specific planners;
- inspect native action names for policy;
- import DP/UCB/threshold verdicts;
- tune weights to maintenance, maze, or bandit outcomes;
- claim generality from one family.

---

## 8. Relationship to `47_RECURSIVE_CONTINUATION_FIELD.md`

`47_RECURSIVE_CONTINUATION_FIELD.md` defines the doctrine.

This file defines the invariant and novelty boundary. Implementation must satisfy this file before family-level results are used as evidence for or against the recursive continuation-field claim.


---

Implementation note: the minimal runtime contract for the first executable version is recorded in `49_RECURSIVE_CONTINUATION_FIELD_RUNTIME_CONTRACT.md`. That file is not a success claim; it is the v1 contract for abstract invariants and diagnostics.

## Invariant closure update — 2026-05-06

The abstract RCF invariant set must be extended before relation-publication results are interpreted. Required additional invariants:

1. Branch identity precedence: `continuation_id` / `branch_id` must outrank `action`.
2. Action-only branches must be marked provisional in telemetry.
3. Relief relations require shared public burden/effect type and overlapping scope.
4. Cancellation requires public reset, inverse, or compensating effect.
5. Quotient requires same-enough residual continuation profile under declared tolerance.
6. Rivalry requires shared commitment slot, exclusive resource, or local closure conflict.
7. Relation publication must reject hidden bestness, hidden state, and baseline verdicts.
8. Relation coverage telemetry must expose relations by type and public basis.

See:

- `76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md`
- `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`
- `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md`

## Relation-to-collapse diagnostic update — 2026-05-06

`85_RELATION_TO_COLLAPSE_DIAGNOSTIC_CONTRACT.md` refines the abstract invariant set above into pre-benchmark microdiagnostics. The added diagnostic rule is:

```text
hold scalar candidate fields fixed;
change relation topology;
require quotient, grey, recursion, or collapse behavior to change for traceable relation reasons.
```

A runtime that cannot pass those diagnostics should not be described as relation-aware RCF, even if it improves reward in a family benchmark.
