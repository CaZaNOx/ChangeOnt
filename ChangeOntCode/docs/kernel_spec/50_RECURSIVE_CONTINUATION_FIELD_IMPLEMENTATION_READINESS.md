# 50. Recursive Continuation Field Implementation Readiness

Status: retained readiness/maintenance gate. First-pass RCF v1 has been implemented; this file now states what must remain true before any behavior-affecting RCF change is accepted.

This file prevents RCF work from becoming benchmark tuning, renamed tree search, renamed value propagation, or family-specific policy leakage.

## 1. Source chain that must remain visible

The implementation is allowed only as an operational bridge from existing CO structure. Relevant `_main` sources include:

- `TheoryOfChange_main/01_Statements/01_Change_Clarification/005_S-CL-process-philosophy-difference.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/011_S-DF-invariant-regime.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/016_S-DF-identity-through-change.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/017_S-DF-bounded-local-unfolding-operative-substrate.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/020_S-DF-regime-signature.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/021_S-DF-minimal-adequate-retention.md`
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law.md`
- `TheoryOfChange_main/01_Statements/Definition/S-DF-prm-closure-quotient.md`
- `TheoryOfChange_main/01_Statements/Definition/S-DF-prm-reid-kernel.md`
- `TheoryOfChange_main/01_Statements/Definition/S-DF-prm-change-ops.md`

Any implementation or modification must cite these concepts as the reason it exists. It must not cite maintenance performance as its reason.

## 2. Kernel-spec sources that must be current

The implementation must conform to:

- `42_CANONICAL_READOUT_AND_ACTION_SELECTION_RULE.md`
- `43_CANONICAL_COMMITMENT_RULE.md`
- `44_CANONICAL_CANDIDATE_SURFACE.md`
- `46_CONTINUATION_STATE_AND_VIABILITY.md`
- `47_RECURSIVE_CONTINUATION_FIELD.md`
- `48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md`
- `50_RECURSIVE_CONTINUATION_FIELD_IMPLEMENTATION_READINESS.md`

## 3. Required abstract invariants before family tests matter

Executable tests must be added using anonymous branches such as `A`, `B`, `C`, `RELIEF`, `SAMPLE`, not problem-family actions.

At minimum they must test:

1. support is not viability;
2. rising debt lowers collapse readiness;
3. debt creates relief pressure;
4. close unresolved rivals preserve grey or increase recursion;
5. flat reliable regions collapse cheaply;
6. shape controls alter recursion/debt sensitivity, not action labels;
7. branch influence depends on structural proximity;
8. quotient-equivalent branches merge/share state;
9. cancellation lowers debt;
10. anti-smuggling: no family names, action names, hidden state, threshold policies, shortest-path oracles, UCB scores, DP scores, or active-inference/free-energy objectives may appear in the generic field.

## 4. Implementation placement

The current first-pass implementation sits after candidate publication, continuation identity, branch-internal burden-operation carriers, and RelationSurface, then feeds CollapseCertificate before CommitmentSurface:

```text
CandidateSurface / ContinuationState
→ Continuation Identity / Burden Operations
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
→ action expression
```

The translator/adapters may provide only public, parity-honest evidence and public burden/effect facts. They may not publish branch relations as policy conclusions or identify the optimal branch. Relation derivation remains kernel-side.

## 5. What the first implementation may do

`RecursiveContinuationField v1` may:

- maintain anonymous branch objects;
- maintain generic branch relations such as rivalry, relief, similarity/proximity, quotient/equivalence, cancellation, and dependency;
- propagate continuation debt to relief branches through generic relation weights;
- delay collapse or increase recursion for close unresolved rivals;
- merge quotient-equivalent branches where same-enough evidence is public;
- reduce debt through cancellation relations;
- emit telemetry for debt, grey preservation, quotient, cancellation, recursion depth, and collapse readiness.

## 6. What it may not do

It may not:

- inspect family names;
- inspect action names for policy meaning;
- use hidden state;
- hardcode maintenance thresholds;
- compute shortest paths in the generic field;
- implement UCB/Q-learning/DP/MCTS/active-inference objectives and relabel them as CO;
- tune parameters from family reward until the result improves.

Known algorithms may inspire implementation tools, but the organizing law must be the CO law from `48`: continuation identity under change, continuation debt, quotient-aware grey preservation, and earned collapse.

## 7. Go / no-go rule

Implementation may proceed when:

```text
47 doctrine exists
48 invariants/novelty boundary exists
50 readiness gate exists
abstract invariant tests are written first
runtime code contains no family/action-name policy logic
```

Family-level benchmarks are evidence only after those conditions are met.

