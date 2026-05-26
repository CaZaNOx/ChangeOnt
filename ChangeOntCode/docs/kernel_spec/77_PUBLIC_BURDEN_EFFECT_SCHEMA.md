# 77. Public Burden / Effect Schema

Status: active conceptual closure / first minimal schema implementation in RelationSurface.

This document specifies the public facts that may lawfully bridge translator output, candidate publication, relation publication, and RCF branch interaction.

It closes the conceptual gap identified in the traceability ledger: relation publication cannot be grounded if candidate rows contain only scalar support/burden scores and action labels.

---

## 1. Why this schema is needed

`Remaining transformation burden` is conceptually grounded in `_main`, but a runtime cannot publish lawful branch relations from the abstract concept alone. It needs typed public facts that say what kind of burden or effect is being carried, relieved, reset, preserved, or made uncertain.

Without such facts, the field has two bad options:

1. infer relations from scalar closeness or low burden, which risks fake relation activity;
2. refuse to infer relations, which leaves RCF relation-starved.

The schema gives a third option:

```text
public burden/effect facts
→ relation publication
→ RCF field interaction
```

---

## 2. Schema authority

Allowed facts must satisfy all of these:

1. public or parity-honest;
2. traceable to the problem contract or visible history;
3. not a near-final action ranking;
4. not derived from hidden optimal policy;
5. typed generically enough to apply across families;
6. auditable in logs.

---

## 3. Minimal fields

Candidate rows may carry a list-like field:

```text
public_effects: [EffectFact, ...]
```

Each `EffectFact` has:

```text
effect_id: stable local identifier
kind: burden | uncertainty | reset | admissibility | support | cost | topology | evidence | resource | buffering | threshold
burden_type: optional generic type label
scope: candidate | branch | candidate_set | temporal | local_region | task_anchor
operation: carry | increase | reduce | relieve | prevent | reset | cancel | reveal | hide | preserve | consume | require | exclude | merge | buffer | mask | transfer | transform | threshold
magnitude: bounded scalar or ordinal bin
direction: optional transformation direction or relief class
coupling: optional relation to the active continuation anchor
barrier: optional accessibility/cost bin for the transformation
threshold_status: none | below_threshold | accumulating | critical | phase_shifted
basin_status: stable | metastable | unstable | overclosed | underclosed | unknown
public_basis: visible_observation | declared_transition_rule | legal_constraint | public_cost | public_history | parity_honest_uncertainty | kernel_history
confidence: bounded scalar or ordinal bin
leakage_status: public | parity_honest | investigatory | forbidden
```

The exact code representation may differ, but these semantic roles must be present.

---

## 4. Burden types

Burden types must be generic and problem-contract grounded. Examples:

```text
degradation
hiddenness
uncertainty
topological_obstruction
cycle_phase
resource_consumption
revision_cost
path_commitment
coverage_gap
contradiction
identity_instability
```

A family may instantiate a generic type, but it may not create a private policy type like:

```text
repair_needed_now
best_arm
shortest_route
replace_threshold_crossed
```

---

## 5. Effect operations

### carry / increase

The candidate continues or increases a burden type.

Example:

```text
RUN carries/increases degradation burden under public maintenance dynamics.
```

This is allowed only if degradation dynamics are public or parity-honestly observable.

### reduce / relieve / prevent

The candidate reduces, relieves, or prevents a burden type.

Example:

```text
REPAIR reduces degradation burden under public maintenance dynamics.
```

This does not say REPAIR is optimal. It only says what public kind of effect the candidate has.

### reset / cancel

The candidate resets or structurally neutralizes a carried burden or state class.

Example:

```text
REPLACE resets machine state class under public transition rules.
```

### reveal / reduce hiddenness

The candidate reduces uncertainty or hiddenness.

Example:

```text
INSPECT reduces health-hiddenness uncertainty.
```


### buffer / absorb

The candidate or public structure absorbs or routes incoming tension so it does not become operative burden at the active scale.

Example:

```text
A flexible branch absorbs ordinary wind variation without identity-breaking burden.
```

This must not be confused with masking. Buffering prevents conversion into operative burden; masking leaves burden operative but hidden or locally underreported.

### mask / postpone

The candidate preserves local support while a burden remains unresolved or becomes less visible.

Example:

```text
RUN continues to get high local reward while degradation burden accumulates.
```

### transfer / transform

The candidate moves burden to another scope or changes its type.

Example:

```text
a detour transfers obstruction burden into path-length burden;
inspection transforms hiddenness burden into revision burden.
```

### threshold / phase shift

The candidate or public condition crosses a boundary where the burden regime changes discontinuously.

Example:

```text
small accumulated degradation remains buffered until a failure threshold is crossed.
```

### require / dependency

The candidate depends on another public condition or continuation remaining available.

### exclude / rivalry

The candidate competes for the same commitment slot or resource.

### merge / equivalence

The candidate yields same-enough residual continuation profile under active tolerance.

---

## 6. Relation derivation from effects

RelationSurface may derive:

```text
relief(B, A)
```

when:

```text
A has carry/increase burden type X
B has reduce/relieve/prevent burden type X
scope overlaps
public basis is admissible
```

RelationSurface may derive:

```text
cancellation(B, A)
```

when:

```text
A carries burden/effect type X
B has reset/cancel operation for X
scope overlaps
public basis is admissible
```

RelationSurface may derive:

```text
hiddenness_reduction(B, A)
```

when:

```text
A's continuation is limited by hiddenness type X
B reveals/reduces uncertainty type X
```

RelationSurface may derive:

```text
equivalence(A, B)
```

when:

```text
A and B publish same residual continuation profile, same burden vector, same reachable frontier, or declared quotient key under tolerance.
```

RelationSurface may derive:

```text
rivalry(A, B)
```

when:

```text
A and B share a commitment slot, resource, exclusive local closure, or cannot both be enacted in the current step.
```

RelationSurface may derive:

```text
buffering_or_shielding(A, B)
```

when:

```text
A publicly buffers tension source X that would otherwise become operative burden for B under the active anchor.
```

RelationSurface may derive:

```text
phase_shift_or_critical_proximity(A, B)
```

when:

```text
A crosses or approaches a public threshold that changes B's burden regime, collapse-readiness, or admissibility condition.
```

---

## 7. Family examples

### Maintenance

Public facts may include:

```text
RUN:    increase/carry degradation burden
INSPECT: reveal/reduce health-hiddenness uncertainty
REPAIR: reduce degradation burden
REPLACE: reset degradation/state burden
WAIT:   preserve or carry temporal burden depending on declared dynamics
```

These are allowed only as public transition/effect facts. They must not encode threshold-optimality or hidden health.

### Bandit

Public facts may include:

```text
EXPLOIT: carry uncertainty/coverage debt when alternatives remain under-sampled
SAMPLE: reduce uncertainty/coverage debt for sampled arm/class
```

No UCB/Thompson/optimal-arm verdict may be published as a CO effect.

### Renewal

Public facts may include:

```text
WAIT/CONTINUE: carry phase/renewal burden when public cycle evidence indicates rising replacement pressure
RENEW: reset cycle/age burden under public dynamics
```

### Maze

Public facts may include:

```text
move into discovered obstruction: increase topological obstruction burden
move to frontier: reduce coverage/hiddenness burden
route segment sharing same corridor: shared-evidence/proximity
wall separation: reduces proximity despite spatial closeness
```

No hidden shortest path may be used in partial maps.

---

## 8. Forbidden schema contents

The following fields are forbidden as canonical public effects:

```text
optimal_action
best_action
value_estimate_from_DP
threshold_policy_decision
oracle_shortest_path_distance
true_hidden_health
winning_arm_label
benchmark_regime_label
reward_tuned_priority
```

Such values may exist in baselines or diagnostics, but not in the canonical CO candidate/effect path.

---

## 9. Telemetry

Every emitted public effect should be loggable with:

```text
candidate_id
continuation_id or branch_id when available
effect kind/type/operation
magnitude/confidence
public_basis
source layer
leakage_status
```

Relation telemetry should record which effect facts generated which relations.

---

## 10. Current status boundary

The current repo may contain candidate scalar fields such as `burden_pressure`, `burden_relief`, `preventive_support`, and `sampling_demand`. Those are useful but not sufficient. They must be supplemented or re-grounded by typed public effects before relation-publication claims are made.

Until this schema is implemented, RCF relation behavior remains provisional.



---

## Implementation note — 2026-05-06

A first minimal parser/consumer of `public_effects`, `burden_effects`, and `effect_facts` now exists in `relation_surface.py`. The implementation is deliberately strict: it rejects missing public basis and forbidden leakage statuses.
