# 87. RelationSurface Public-Effect Implementation

Status: minimal runtime implementation / microdiagnostic validated / not benchmark evidence.

This document records the first runtime implementation of the kernel-side RelationSurface contract defined in:

```text
80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md
77_PUBLIC_BURDEN_EFFECT_SCHEMA.md
84_BURDEN_OPERATION_ALGEBRA.md
85_RELATION_TO_COLLAPSE_DIAGNOSTIC_CONTRACT.md
86_MINIMAL_BURDEN_FORMAL_SKELETON.md
```

It is intentionally narrow. It does not claim a completed burden algebra or performance success. It closes the immediate implementation gap where RCF could consume explicit branch relations but no kernel-side layer derived those relations from public burden/effect facts.

---

## 1. Runtime location

Implemented file:

```text
ChangeOntCode/agents/co/runtime/surfaces/relation_surface.py
```

Integration point:

```text
CandidateSurface
→ RelationSurface
→ RecursiveContinuationField
```

`candidate_surface.py` now preserves candidate `public_effects` / `burden_effects` / `effect_facts`, calls `apply_relation_surface(...)`, and passes the derived `BranchRelation` list into `apply_continuation_field(...)`.

---

## 2. What RelationSurface does

RelationSurface derives, from public burden/effect facts only:

```text
continuation / branch identity metadata
burden operation readings
relief relations
cancellation relations
shared-evidence / exposure relations
buffering / shielding relations
dependency relations
proximity / phase-shift relations
strong rivalry relations when a public incompatibility basis exists
decision-slot competition telemetry when only one candidate can be selected now
equivalence / quotient relations
```

It does not inspect family names, benchmark names, reward-optimality, baseline values, or hidden state truth.

---

## 3. Public-effect acceptance boundary

A public effect is accepted only when it has an allowed public basis and an allowed leakage status.

Accepted public bases include:

```text
visible_observation
declared_transition_rule
legal_constraint
public_cost
public_history
parity_honest_uncertainty
kernel_history
problem_contract
```

Accepted leakage statuses include:

```text
public
parity_honest
kernel_history
investigatory
```

Forbidden or rejected statuses include:

```text
forbidden
hidden_policy
optimal_policy
oracle
baseline_value
```

Facts without public basis are rejected. Solver-like facts are rejected. Burden-derived relations generally require a typed `burden_type`; pure legal/resource rivalry may instead use a public relation/resource scope.

---

## 4. Relation derivation rules implemented

### Relief

```text
source: reduce / relieve / prevent burden type X
target: carry / increase / amplify / consume / require / mask / postpone burden type X
→ relief(source, target)
```

### Cancellation

```text
source: reset / cancel burden type X
target: carry / increase / mask / relieve burden type X
→ cancellation(source, target)
```

### Shared evidence / exposure

```text
source: reveal / expose / reduce_hiddenness burden/evidence type X
target: carry or mask X, or uncertainty/evidence fact X
→ shared_evidence(source, target)
```

### Buffering

```text
source: buffer / absorb tension/burden type X
target: carry / threshold burden type X
→ buffering(source, target)
```

### Dependency

```text
source: transfer / transform burden type X
target: carry burden type X
→ dependency(source, target)
```

### Proximity / phase-shift

```text
source or target: threshold / phase_shift burden type X
other side has overlapping type/scope
→ proximity(source, target)
```

### Strong rivalry

```text
source and target: public exclude / rival / compete facts with same relation/resource scope
where the basis is stronger than mere membership in one immediate action set
→ rivalry(source, target)
```

A single-readout-slot fact is emitted as `decision_slot_competition`, not strong rivalry, unless another public incompatibility basis exists.

### Equivalence / quotient

```text
source and target: same accepted public pressure/effect signature
→ equivalence(source, target)
```

This equivalence rule is deliberately conservative. It does not infer quotient from scalar closeness.

---

## 5. Branch identity status

`ContinuationField` now uses the intended identity precedence:

```text
continuation_id
→ branch_id
→ candidate_id
→ action
```

Native action remains an interface expression and last-resort placeholder, not the preferred branch identity.

RelationSurface may derive a runtime branch handle from public pressure-signature evidence. When it does so, action/candidate identity is used only as a row-expression disambiguator; the pressure signature is recorded separately as `continuation_signature`.

Known limitation: this is not yet a full continuation-identity aggregator. Equivalent pressure signatures are currently linked by quotient/equivalence relations rather than pre-aggregated into one branch object.

---

## 6. Telemetry exposed

RelationSurface records:

```text
candidate_rows
branches_derived
relations_total
relations_by_type
rows_with_public_effects
rows_with_relations
identity_source_counts
accepted_public_effects
rejected_* counts
operation_* counts
relation_* counts
```

Candidate rows also carry local fields such as:

```text
relation_surface_identity_source
relation_surface_public_effect_count
relation_surface_effect_signature
relation_surface_relation_count
relation_surface_telemetry
```

This makes relation starvation visible.

---

## 7. Tests added

New invariant file:

```text
ChangeOntCode/agents/co/tests/relation_surface_public_effect_invariants.py
```

It verifies:

```text
public reduce/carry facts derive relief;
forbidden hidden-policy effects are rejected;
missing public basis is rejected;
reset/carry derives cancellation distinct from relief;
reveal/carry derives shared_evidence;
same public pressure signature derives equivalence/quotient;
branch_id outranks action in identity precedence.
```

`candidate_surface_publication_invariants.py` also verifies the integrated CandidateSurface → RelationSurface → RCF path using public effects.

---

## 8. Verification snapshot

The following modules were run after implementation and passed in isolation:

```text
agents.co.tests.relation_surface_public_effect_invariants
agents.co.tests.burden_relation_microdiagnostics
agents.co.tests.recursive_continuation_field_relation_support_invariants
agents.co.tests.recursive_continuation_field_invariants
agents.co.tests.continuation_state_invariants
agents.co.tests.candidate_surface_publication_invariants
agents.co.tests.commitment_surface_readout_invariants
agents.co.tests.shape_prior6_contract_invariants
agents.co.tests.shape_prior6_active_path_invariants
agents.co.tests.runtime_contract_invariants
agents.co.tests.problem_contract_invariants
agents.co.tests.maintenance_replacement_family_invariants
agents.co.tests.maintenance_replacement_runtime_wiring_invariants
agents.co.tests.maintenance_replacement_stoa_baseline_invariants
agents.co.tests.smoke_co_runner
```

This is mechanism/invariant evidence only. It is not reward/performance evidence.

---

## 9. Remaining limitations

This implementation does not yet prove that real problem adapters publish rich public effects. Existing family rows may remain relation-sparse unless adapters expose lawful public burden/effect facts.

Open work:

```text
adapter public-effect publication;
relation coverage diagnostics on real family traces;
collapse-certificate telemetry beyond field scalar readiness;
formula-level grounding for scalar integration;
known-algorithm comparison;
broad family benchmarking only after relation coverage is real.
```

---

## 10. Acceptance correction implemented by follow-up patch

The architecture audit found that generic `rivalry` dominated relation topology. The corrected implementation must use:

```text
decision_slot_competition
```

for public single-readout-slot facts produced by `single_decision_slot_effect(...)`, and reserve:

```text
rivalry
```

for strong continuation rivalry. CollapseCertificate must ignore `decision_slot_competition` as an unresolved-rival blocker unless another strong relation makes the rivalry continuation-relevant.

The implementation also derives public-effect branch signatures using coarse burden-regime bands rather than raw magnitudes. This allows material pressure regime changes to change branch identity without making tiny magnitude jitter create new branches.
