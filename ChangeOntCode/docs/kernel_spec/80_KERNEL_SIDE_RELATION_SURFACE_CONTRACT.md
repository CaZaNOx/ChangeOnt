# 80. Kernel-Side RelationSurface Contract

Status: conceptual contract with first minimal runtime implementation recorded in `87_RELATION_SURFACE_PUBLIC_EFFECT_IMPLEMENTATION.md`.

This document binds the `_main` clarifications:

```text
S-DR-pressure-signature-continuation-branch-identity.md
S-CL-candidate-branch-continuation-commitment-separation.md
S-CL-public-facts-vs-policy-advice.md
```

to the runtime architecture. It specifies that continuation identity and branch relation derivation are kernel-side work.

---

## 1. Architectural placement

The intended pipeline is:

```text
Adapter
→ public problem facts / native actions / public effects
→ CandidateSurface
→ candidate expressions and local public signals
→ RelationSurface
→ continuation identities and branch relations
→ RecursiveContinuationField
→ branch-field deformation
→ CommitmentSurface
→ earned collapse into native action expression
```

RelationSurface is the layer that prevents RCF from inventing relations from scalar closeness while also preventing adapters from publishing policy advice as relation structure.

---

## 2. Adapter responsibility

Adapters may publish:

- legal actions and transitions;
- visible observations;
- public costs or resource constraints;
- public or parity-honest uncertainty structure;
- public burden/effect facts as defined in `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`;
- native action labels needed for environment interaction.

Adapters must not publish:

- optimal action labels;
- hidden-state verdicts;
- baseline-policy decisions;
- DP/UCB/A*/Q-value preferences;
- branch relations whose basis is strategic ranking rather than public effect structure.

---

## 3. CandidateSurface responsibility

CandidateSurface surfaces candidate expressions and public local signals. It may preserve public effects and raw candidate structure. It should not silently equate candidate/action with continuation branch.

CandidateSurface may produce provisional candidate IDs, but continuation identity authority belongs to RelationSurface/RCF once pressure-signature evidence exists.

---

## 4. RelationSurface responsibility

RelationSurface derives:

- `continuation_id` / `branch_id` from pressure-signature evidence;
- burden operation status from public burden/effect facts;
- relief relations;
- cancellation relations;
- quotient/equivalence relations;
- rivalry/exclusion relations;
- shared evidence relations;
- structural proximity relations;
- buffering/shielding relations;
- threshold/phase-shift relations;
- dependency relations where public effect grammar supports them.

RelationSurface must derive these from public facts and burden operations, not from action names alone, hidden reward, or benchmark performance. Named relations are derived cases of coupling among burden, admissibility, evidence, identity, and collapse conditions.

---

## 5. Continuation identity precedence

If a row has multiple identity fields, the intended order is:

```text
continuation_id
→ branch_id
→ candidate_id
→ action
```

`action` is a last-resort interface placeholder, not a continuation identity. A runtime that uses `action` first is provisional and not yet paper-clean.

---

## 6. Relation derivation examples

### Relief

```text
A carries/increases burden type X.
B reduces/relieves/prevents burden type X.
Scopes overlap.
Public basis is admissible.
→ relief(B, A)
```

### Cancellation

```text
A carries burden/effect condition X.
B resets/cancels condition X.
Scopes overlap.
→ cancellation(B, A)
```

### Hiddenness reduction

```text
A's collapse depends on unresolved hiddenness X.
B reveals/reduces uncertainty X.
→ hiddenness_reduction(B, A)
```

### Strong rivalry

```text
A and B consume the same public resource, legally exclude one another,
or one continuation invalidates/destabilizes the other's continuation condition.
→ rivalry(A, B)
```

Mere co-membership in one immediate action set is not strong rivalry. That is
`decision_slot_competition` telemetry unless a stronger public basis is present.

### Quotient / equivalence

```text
A and B have same-enough pressure signatures under active continuation tolerance.
Remaining differences do not change burden, admissibility, relation topology, or collapse consequences.
→ quotient(A, B)
```

### Buffering / shielding

```text
A absorbs or routes tension source X so X does not become operative burden for B under the active scale/anchor.
→ buffering_or_shielding(A, B)
```

This must not be inferred merely from low burden. The public basis must support actual buffering, not masking.

### Threshold / phase-shift

```text
A crosses or approaches a public threshold that changes B's burden regime, admissibility, or collapse-readiness.
→ phase_shift_or_critical_proximity(A, B)
```

---

## 7. Telemetry requirement

RelationSurface must log, at minimum:

```text
candidate_rows
branches_derived
relations_total
relations_by_type
rows_with_explicit_public_effects
rows_with_relations
relations_rejected_for_leakage
relations_rejected_for_insufficient_basis
identity_source_counts: continuation_id / branch_id / candidate_id / action
```

Telemetry must make relation starvation visible.

---

## 8. Paper-risk boundary

A result cannot be used as evidence for a relation-aware RCF if:

- branch identity is action-derived by default;
- real rows have no relation coverage;
- relations are inferred only from scalar closeness;
- RelationSurface is bypassed;
- relation effects are unlogged;
- performance improvement comes from family-specific action logic.

---

## 9. Current implementation status

A first runtime RelationSurface exists. The contract remains stronger than the current implementation because relation minimality, formula grounding, multi-step identity, and broader trace quality are still open.

---

## 10. First minimal implementation note — 2026-05-06

A first runtime RelationSurface now exists at:

```text
ChangeOntCode/agents/co/runtime/surfaces/relation_surface.py
```

It derives relations from public burden/effect facts and is integrated before RCF in `candidate_surface.py`. See `87_RELATION_SURFACE_PUBLIC_EFFECT_IMPLEMENTATION.md` for scope, tests, and limitations.

---

## 11. Architecture-acceptance correction: weak decision-slot competition is not strong rivalry

Following `92_ARCHITECTURE_ACCEPTANCE_AUDITS.md`, RelationSurface must separate procedural competition for one immediate readout slot from strong continuation rivalry.

```text
decision_slot_competition:
  public fact that only one candidate expression can be selected now;
  not by itself an earned-collapse blocker.

rivalry:
  public fact that one continuation blocks, consumes, invalidates, or destabilizes another continuation condition;
  may become an earned-collapse blocker if unresolved.
```

Adapters may publish a decision-slot fact, but the kernel must not treat that fact as a strong unresolved rival. Strong rivalry requires a stronger public basis than simple co-membership in an action set.

---

## 12. Architecture-acceptance correction: burden-regime continuation signatures

When RelationSurface derives continuation identity from public pressure signatures, it may include coarse burden-regime bands. It must not key identity by raw magnitudes.

```text
same action + materially different burden regime → different pressure signature
same action + small within-band variation → same pressure signature
```

This keeps branch identity pressure-sensitive without exploding into one branch per numeric observation.
