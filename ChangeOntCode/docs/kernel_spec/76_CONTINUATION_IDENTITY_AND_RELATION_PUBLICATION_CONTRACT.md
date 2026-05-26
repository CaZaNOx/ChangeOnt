# 76. Continuation Identity and Relation Publication Contract

Status: active conceptual closure / first-pass implementation contract. Code contains first-pass carriers, but broader telemetry and formula grounding remain open.

This document closes the first-pass conceptual gap between `_main` branch-identity derivation and runtime RCF behavior. It binds the new `_main` derivation:

```text
TheoryOfChange_main/01_Statements/Derivation/S-DR-continuation-branch-identity-from-bounded-continuation-profile.md
```

to the runtime docs:

```text
44_CANONICAL_CANDIDATE_SURFACE.md
47_RECURSIVE_CONTINUATION_FIELD.md
48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md
49_RECURSIVE_CONTINUATION_FIELD_RUNTIME_CONTRACT.md
77_PUBLIC_BURDEN_EFFECT_SCHEMA.md
```

It does not claim that the current code fully realizes the doctrine. It defines what the code must preserve before RCF behavior can be interpreted as relation-aware continuation-field behavior rather than action-score deformation.

---

## 1. Authority chain

The authority order is:

```text
_main derivation
→ kernel/spec contract
→ code implementation
→ tests/telemetry
→ evidence claim
```

Code may not demand a concept that the `_main`/docs chain has not grounded. Conversely, if current code does less than this contract, the code is partial rather than the doctrine being weakened.

---

## 2. Core distinction

### 2.1 Native action

A native action is the environment-facing move emitted at the boundary:

```text
RUN
REPAIR
INSPECT
REPLACE
move_north
arm_2
```

A native action is an interface expression. It is not automatically a continuation identity.

### 2.2 Candidate row

A candidate row is the kernel-facing publication of public, admissible candidate-local structure. It may include native action identity because the runtime must eventually return an action to the environment.

A candidate row is still not automatically a continuation branch. It is raw or partially processed support for possible continuation.

### 2.3 Continuation branch

A continuation branch is the minimally retained identity of a live admissible continuation whose support, burden, relation, or collapse-readiness is still unresolved.

A branch may be expressed by one or more native actions over time. A single native action may express different branches in different contexts.

Examples:

```text
stable-operation-continuation
hiddenness-reduction-continuation
degradation-relief-continuation
reset-continuation
frontier-probe-continuation
exploit-stable-supported-continuation
uncertainty-reduction-continuation
```

These names are examples only. Canonical implementation should derive anonymous or typed continuation identities from public structure, not from hand-written family policy.

---

## 3. Branch identity precedence rule

If a row contains multiple identity fields, the canonical precedence is:

```text
continuation_id
→ branch_id
→ candidate_id
→ action
```

`action` is the last-resort provisional identity, not the first identity.

Therefore, an implementation that does this is misaligned:

```python
row.get("action", row.get("branch_id", row.get("candidate_id", "branch")))
```

because it collapses a possible continuation identity back into a one-step action whenever `action` exists.

Correct doctrine:

```python
row.get("continuation_id", row.get("branch_id", row.get("candidate_id", row.get("action", "branch"))))
```

This rule is not a performance patch. It is required by the `_main` derivation of branch identity.

---

## 4. Relation publication purpose

RCF requires branch interaction. However, branch interactions may not be invented from hidden policy, action names, benchmark outcomes, or final action scores.

A relation may be published only when traceable to public continuation structure.

The purpose of relation publication is to transform public burden/effect facts into lawful branch relations such as:

```text
relief
cancellation
equivalence / quotient
rivalry / exclusive
similarity / proximity
shared evidence
dependency / prerequisite
hiddenness reduction
burden inheritance
```

---

## 5. Allowed public bases for relations

Relation publication may use only:

- admissible candidate identities;
- public legality / admissibility;
- public or parity-honest uncertainty;
- public candidate-local burden/effect fields;
- public task-anchor relation when not already a ranking;
- public costs and visible consequences;
- public transition semantics declared by the problem contract;
- kernel history generated from prior public observations;
- direct controls derived from `shape_prior6`, used only to modulate relation sensitivity, not to choose actions.

---

## 6. Forbidden relation bases

Relation publication may not use:

- family names as policy branches;
- action names as policy rules;
- hidden simulator state;
- true hidden health in hidden regimes;
- oracle future route costs;
- DP, value-iteration, Q-learning, UCB, MCTS, threshold-opt verdicts;
- post-hoc benchmark outcome information;
- reward-improvement tuning;
- labels such as “best,” “optimal,” “should choose,” or equivalent near-final policy hints.

---

## 7. Generic relation laws

### 7.1 Relief

```text
If branch A carries, increases, or inherits public burden type X,
and branch B publicly reduces, relieves, or prevents burden type X
within the same relation scope,
then B may publish a relief relation toward A.
```

This is not “B is good.” It is only “B reduces a burden type currently carried by A.” Commitment must still decide whether that relief matters enough under the active field.

### 7.2 Cancellation

```text
If branch B publicly reverses, resets, compensates, or neutralizes
burden/effect type X carried by branch A,
then B may publish a cancellation relation toward A.
```

Cancellation is stronger than relief. It says the prior burden can be structurally neutralized, not merely reduced.

### 7.3 Equivalence / quotient

```text
If branches A and B have same-enough residual continuation profiles
under active identity tolerance,
then A and B may publish an equivalence / quotient relation.
```

Permitted evidence includes same residual burden vector, same public task-anchor relation, same reachable frontier, same public state class, or same continuation profile under declared tolerance.

### 7.4 Rivalry / exclusive

```text
If branches A and B compete for the same commitment slot,
consume the same exclusive resource,
or cannot both be pursued under the current local closure,
then A and B may publish rivalry / exclusive relation.
```

Rivalry is not an action ranking. It marks that unresolved comparison matters for collapse.

### 7.5 Similarity / proximity / shared evidence

```text
If branches A and B share public evidence source, burden type,
frontier, bottleneck, task-anchor relation, or reachable local region,
then A and B may publish similarity/proximity/shared-evidence relation.
```

Spatial closeness alone is insufficient where topology or public boundary separates continuations. Structural proximity, not Euclidean nearness, is the relevant basis.

### 7.6 Dependency / prerequisite

```text
If branch B must occur or remain available for branch A to stay admissible,
then A may publish dependency relation on B.
```

Dependency must be public and structural. It may not encode hidden planner order.

---

## 8. Where relation publication should live

Canonical target:

```text
adapters publish public burden/effect facts
→ RelationSurface derives branch relations from those facts
→ RecursiveContinuationField consumes relations
→ CommitmentSurface reads field-adjusted continuation state
```

The preferred architecture is a small kernel-side `RelationSurface` or clearly separated relation-publication helper, not relation logic hidden inside adapters or scattered inside RCF scoring.

Adapters should publish facts, not relations, unless the relation is a direct public structural fact already declared in the problem contract.

---

## 9. Adapter permission boundary

Adapters may publish public typed facts like:

```text
this candidate publicly tends to increase degradation burden
this candidate publicly tends to reduce hiddenness uncertainty
this candidate publicly resets the machine state class
this candidate is mutually exclusive with other one-step candidates in the current commitment slot
```

Adapters may not publish:

```text
this candidate is best
this candidate is optimal below threshold T
this candidate has higher DP value
this action should relieve that action because the hidden state says so
```

---

## 10. Telemetry requirement

Every runtime trace that uses RCF as evidence must report:

```text
branch identity source counts:
  continuation_id
  branch_id
  candidate_id
  action-label last-resort interface expression

relation coverage:
  explicit relation rows
  relations by type
  relations by public basis
  rejected relation hints
  action-name-derived relations detected
  hidden/oracle relation inputs detected

field effect:
  how relations changed debt
  how relations changed relief support
  how relations changed grey pressure
  how relations changed collapse readiness
```

If telemetry cannot show that branch relations were public and active, reward changes cannot be used as evidence for RCF novelty.

---

## 11. Implementation acceptance tests

Before relation-publication results are interpreted, the following abstract tests must exist:

1. `branch_id_precedes_action_when_both_present`.
2. `action_only_identity_is_marked_provisional`.
3. `relief_relation_requires_shared_public_burden_type`.
4. `cancellation_requires_public_reset_or_inverse_effect`.
5. `quotient_requires_same_residual_profile_or_declared_tolerance`.
6. `rivalry_requires_shared_commitment_slot_or_exclusion`.
7. `adapter_bestness_hint_is_rejected_or_ignored`.
8. `relation_surface_contains_no family/action policy literals`.
9. `relation_coverage_telemetry_reports_zero_when_no public facts exist`.
10. `relation_coverage_telemetry_reports_nonzero_when public facts justify relations`.

---

## 12. Claim boundary

The current repo contains first-pass implementation carriers and structural telemetry for this contract. Therefore RCF may be claimed as:

```text
a first-pass relation-aware recursive-continuation runtime path under structural diagnostics.
```

It may not yet be claimed as:

```text
a fully realized CO-native recursive continuation field;
a novel algorithmic family;
or empirically validated CO superiority.
```

