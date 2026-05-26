# 47. Recursive Continuation Field

Status: active first-pass kernel-runtime integration doctrine; relation/certificate-aware path recorded after 2026-05-06 fixes.

This file binds together existing doctrine that previously appeared under several names: effective CO field, continuation surface, branch-space, adaptation debt, closure/quotient, thin collapse, and `ContinuationState`. It does not introduce a new ontology primitive. It specifies how those already-admitted concepts should function together as a runtime field rather than as isolated candidate scores.

## 1. Layer placement

`RecursiveContinuationField` belongs to kernel-runtime architecture.

It is:

- not a root ontological primitive;
- not a deep element;
- not a six-question placement axis;
- not adapter logic;
- not a benchmark-specific policy;
- not a replacement for `ContinuationState`.

It sits after candidate publication, continuation identity, branch-internal burden operation typing, and RelationSurface relation derivation; it sits before CollapseCertificate and CommitmentSurface:

```text
Boundary / Adapter
→ CandidateSurface
→ Continuation Identity
→ Burden Operations
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
→ action expression
→ feedback update
```

`ContinuationState` is the per-continuation memory object. `RecursiveContinuationField` is the interaction space in which multiple continuation states deform one another before earned collapse is certified.

## 2. Ontological source

The relevant `_main` chain is:

```text
meta-change / recursive self-modulation
→ continuation admissibility
→ local comparability field
→ remaining transformation burden
→ identity-through-change
→ operative difference
→ regime signature
→ minimal adequate retention
→ thin collapse law
→ closure / quotient
```

The operational reading is:

- a candidate is not merely an action;
- a candidate is a possible continuation under change;
- a continuation has support, burden, debt, fracture, uncertainty, and possible equivalence to other continuations;
- collapse is lawful only when retaining richer grey structure is no longer needed for the regime.

## 3. Definitions

### 3.1 Continuation field

A continuation field is the bounded runtime field of candidate continuations currently live under the problem envelope. It records not only each continuation's local support, but also how continuations interact through burden, debt, rivalry, relief, equivalence, cancellation, and recursion-depth demand.

### 3.2 Branch

A branch is a live continuation hypothesis in the field. A branch may be expressed by one or more native actions over time, but it is not identical to a one-step action.

Example: in a maze, a branch can be a detour-continuation. In maintenance, a branch can be an operating-continuation or burden-relief-continuation. In bandit, a branch can be exploit-currently-supported or reopen/explore-continuation.

### 3.3 Continuation debt

Continuation debt is unresolved burden introduced when a branch deviates from a higher-level attractor, preserves local support by postponing necessary deformation, or consumes options that must later be repaired.

Debt is not a punishment for moving away from a goal. A detour may be lawful. Debt means only that the detour must later justify itself by relieving a higher burden, discovering a viable passage, preserving future options, or otherwise improving continuation viability.

### 3.4 Grey preservation

Grey preservation is the refusal to collapse a live ambiguity into a hard decision when the field still contains structurally relevant unresolved alternatives. It is the runtime inheritance of minimal adequate retention and thin collapse law.

Grey preservation is required when close rivals, high hiddenness, high consequence span, high revision cost, high path dependence, rising debt, or unstable equivalence relations remain active.

### 3.5 Recursion-depth budget

Recursion-depth budget is the bounded amount of further branch expansion / continuation simulation / neighbor inspection the runtime may allocate before committing. It is a runtime budget, not a metaphysical depth claim.

Depth should increase where the active shape and field conditions say premature collapse is dangerous. Depth should shrink in flat, low-risk, locally reliable regimes.

### 3.6 Branch interaction

Branch interaction is any generic effect one branch has on another branch's viability.

Allowed interaction types include:

- rivalry: two branches compete for collapse;
- relief: one branch reduces debt/burden produced by another;
- cancellation: a branch reverses or compensates a prior debt;
- quotient / merge: branches become same-enough under the active identity tolerance;
- fracture spread: instability of one branch increases recursion demand of neighbors;
- attractor debt: deviation from a public attractor increases unresolved burden until justified;
- sampling support: hiddenness or unresolved rivalry makes information-gathering branches more viable.

## 4. Why this layer is needed

A kernel that only publishes candidate rows can still behave like a classical action scorer:

```text
action has current support
→ action wins
```

That misses a CO distinction:

```text
continuation has current support
but the continuation's debt/burden/fracture field may be worsening
→ collapse may be premature
```

The field layer exists to prevent the runtime from losing grey structure too early. It allows the kernel to track how a locally supported branch becomes less viable because of accumulated debt, path dependence, hiddenness, or rivalry, even before immediate local support collapses.

## 5. Relation to the six-question shape prior

The six questions do not decide branches. They modulate field dynamics.

- high `hidden_decisiveness` increases sampling support and recursion depth;
- high `reshapeability` increases admissible revision and branch birth;
- high `local_cue_reliability` allows earlier collapse from local support;
- high `revision_cost` delays premature collapse and increases debt sensitivity;
- high `consequence_span` amplifies nonlocal burden and branch-debt propagation;
- high `topology_constraint` increases path sensitivity, quotient discipline, and detour debt.

Correct route:

```text
shape_prior6
→ direct controls
→ recursion/debt/collapse modulation
→ field interaction
→ commitment
```

Incorrect route:

```text
shape_prior6
→ hidden posture/action preset
→ action
```

## 6. Boundary and anti-smuggling law

The continuation field may use only:

- public candidate admissibility;
- public task anchor / reward direction where available;
- public costs and visible consequences;
- visible or parity-honest uncertainty;
- candidate-local support / burden / fracture / uncertainty;
- direct controls derived from `shape_prior6`;
- kernel history generated from prior public observations.

It may not use:

- family labels as policy branches;
- action-name-specific policy hacks;
- hidden simulator state;
- shortest-path oracle scores in partial maps;
- threshold/control-limit verdicts;
- value-iteration / DP / UCB outputs as kernel-native truth;
- post-hoc shape values fitted to benchmark outcomes.

## 7. Core field laws

### Law 1: support is not viability

High local support is not sufficient for collapse when burden, debt, rivalry, hiddenness, or revision exposure are high.

### Law 2: debt must become field pressure

If one branch preserves local support by postponing necessary deformation, the unresolved burden becomes continuation debt. That debt must either be relieved, justified, merged away by quotient, or counted against later viability.

### Law 3: collapse must be earned

Collapse is justified when active rivals are sufficiently dominated, debt is low or falling, hiddenness is tolerable for the regime, and retaining grey structure would no longer change lawful continuation.

### Law 4: grey retention is bounded

The kernel may not keep all branches alive indefinitely. Retention must be justified by field pressure and bounded by recursion budget.

### Law 5: recursion depth is local

Depth is allocated to contested or burdened regions, not globally. A main branch with rising debt can receive deeper recursion while flat subbranches collapse cheaply.

### Law 6: branch equivalence is operational

Branches that become same-enough under active identity tolerance should merge by closure/quotient. Branches that differ only by locally cancelled debt should not be counted as separate decisive futures.

### Law 7: branch interaction is generic

A branch can raise or lower another branch's viability only through generic quantities such as burden relief, debt cancellation, uncertainty reduction, admissibility, quotient relation, or support persistence — never through family-specific policy labels.

## 8. Examples without policy leakage

### Maze

A public goal direction may act as an attractor. Moving away from it can create directional debt, but this is not forbidden: a detour is allowed when it may relieve a higher obstruction. The field should track whether the detour later reduces obstruction or merely compounds debt. It must not read undiscovered walls or oracle shortest paths.

### Maintenance

Continuing operation can retain local reward while accumulating recovery debt. Repair or inspection may gain field relevance by relieving burden or reducing hiddenness, not because the kernel knows a maintenance threshold.

### Bandit

Exploiting a currently supported continuation can be a stable continuation when uncertainty and drift are low. Under unresolved uncertainty or stale support, exploitation creates exploration debt and sampling branches gain viability.

### Renewal

A phase-aligned continuation may be locally weak but field-viable if it preserves cycle coherence. A locally rewarding action can become debt-heavy if it breaks phase viability.

### Latent mechanism

Trusting a visible cue is a continuation. If hidden decisive structure remains unresolved, sampling or reinterpretation branches gain viability through hiddenness pressure, not through a family-specific clue.

## 9. Abstract invariants for first implementation

`48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md` is now the binding invariant and novelty-boundary contract for this doctrine. A first implementation is acceptable only if abstract candidate tests demonstrate:

1. same local support + rising burden lowers continuation viability;
2. a lower-local-support branch that relieves active burden can gain viability;
3. high hiddenness and low cue reliability increase sampling / grey preservation;
4. high consequence span and revision cost increase recursion depth or collapse delay;
5. equivalent branches merge under quotient tolerance;
6. canceling a prior debt lowers branch debt;
7. close rivals increase local recursion depth;
8. flat low-risk branches collapse cheaply;
9. changing direct controls changes field behavior before changing action;
10. no family-name or action-name literal appears in the canonical field implementation.

The list above is a short summary. The full test contract, diagnostic contract, and novelty boundary are in `48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md`.

## 10. Minimal implementation direction

Do not immediately create many new surfaces.

A minimal `RecursiveContinuationField v1` should:

- consume existing `ContinuationState` rows;
- compute branch-level debt and neighbor/rival pressure;
- compute recursion-depth/collapse-delay hints;
- compute quotient/merge candidates where same-enough relations are available;
- emit generic field-adjusted viability for `CommitmentSurface`;
- expose audit telemetry explaining whether collapse, grey-retention, or branch expansion was justified.

This is an extension of the current runtime bridge, not a new solver.

## 11. Failure meaning

If this doctrine is ignored, the kernel will keep regressing toward action scoring:

```text
candidate action + local support
→ earned collapse / committed branch
```

A CO-aligned kernel must instead treat action as the current expression of a field-shaped continuation:

```text
bounded continuation field
→ branch interaction / debt / quotient / grey-retention
→ collapse when stability is earned
→ action expression
```

## 12. First-pass readiness bar

This doctrine has a first-pass runtime implementation, but the readiness bar remains the maintenance checklist for any behavior-affecting change:

- keep the layer runtime-only;
- preserve the derivation from existing CO concepts;
- keep abstract invariants passing;
- forbid family policy leakage;
- preserve the diagnostic split between boundary, shape, candidate, relation, field, certificate, commitment, and readout;
- do not turn benchmark performance into the reason for the mechanism.

Passing the readiness bar does not mean maintenance is solved, baselines are beaten, or new robot/simulator work should be promoted into the active phase.


---

Implementation note: the minimal runtime contract for the first executable version is recorded in `49_RECURSIVE_CONTINUATION_FIELD_RUNTIME_CONTRACT.md`. That file is not a success claim; it is the v1 contract for abstract invariants and diagnostics.

## Branch identity closure update — 2026-05-06

The `_main` bridge now contains a dedicated derivation:

`TheoryOfChange_main/01_Statements/Derivation/S-DR-continuation-branch-identity-from-bounded-continuation-profile.md`

This strengthens the branch definition above. A branch is the minimally retained identity of a live admissible continuation, not a one-step action label. Therefore, the canonical implementation must prefer continuation identity fields over native action fields when constructing field branches:

```text
continuation_id → branch_id → candidate_id → action
```

Using `action` first is a documented misalignment unless the row has no continuation identity available. Runs in which branch identity falls back to action labels must be treated as provisional RCF tests.

Relation publication is governed by:

- `76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md`
- `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`

The field should consume public relations; it should not invent strong cross-branch relations from scalar closeness alone.
