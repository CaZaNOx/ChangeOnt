# 49. Recursive Continuation Field Runtime Contract

Status: active first-pass runtime contract; updated for RelationSurface and CollapseCertificate path.

This file records what was implemented after `47_RECURSIVE_CONTINUATION_FIELD.md` and `48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md`. It is intentionally narrow. It does not claim that the full CO-native kernel is complete. It defines the minimal v1 mechanic needed to test whether recursive continuation-field dynamics can be expressed without family-specific policy leakage.

---

## 1. Runtime placement

The v1 runtime path is:

```text
Boundary / Adapter
→ CandidateSurface
→ Continuation Identity / ContinuationState
→ Branch-internal Burden Operations
→ RelationSurface
→ RecursiveContinuationField v1
→ CollapseCertificate
→ CommitmentSurface
→ action
```

The field sits after candidate rows, continuation identity, per-continuation memory, branch-internal operation carriers, and relation derivation. It sits before earned-collapse certification and final commitment. It reshapes branch rows by adding field-level quantities:

```text
field_debt
field_relief_support
field_grey_pressure
field_recursion_budget
field_collapse_readiness
field_viability
quotient_id
quotient_share_count
```

These are not problem policies. They are anonymous branch-field quantities.

---

## 2. What v1 implements

`ChangeOntCode/agents/co/runtime/surfaces/continuation_field.py` defines:

```text
ContinuationBranch
BranchRelation
ContinuationField
apply_continuation_field
```

The implemented relation vocabulary includes:

```text
relief
cancellation
equivalence / quotient / merge
similarity / proximity / shared_evidence
dependency / prerequisite where public
strong rivalry / exclusion where structurally warranted
weak decision-slot competition as procedural telemetry only
```

The field update performs only generic operations:

1. Converts candidate-publication rows into anonymous continuation branches.
2. Preserves branch-internal burden operations even when no cross-branch relation is derived.
3. Consumes RelationSurface relations derived from public burden/effect facts.
4. Propagates debt pressure to relief-capable branches.
5. Preserves grey pressure around close unresolved structural rivals.
6. Marks equivalent branches with a quotient identity.
7. Allows compensating branches to reduce debt.
8. Allocates local recursion budget from shape-conditioned nonclosure pressure.
9. Computes collapse readiness after debt, relief, grey, quotient, and recursion effects.
10. Feeds CollapseCertificate rather than allowing CommitmentSurface to treat scalar field output as sufficient collapse.

---

## 3. What v1 must not do

The field must not inspect:

```text
problem-family names
action names
hidden state
oracle future route costs
threshold policies
DP / UCB / MCTS rollout values
```

The v1 source is guarded by abstract invariants that scan for active problem/action literals in the canonical field implementation.

---

## 4. What v1 does not yet prove

This implementation does not prove novelty. It only creates an executable place where novelty could be tested.

It does not yet prove that:

- CO is a new algorithmic family;
- maintenance failure is solved;
- robot/sim should be implemented immediately;
- branch interaction is superior to known planning/message-passing methods;
- continuation debt is irreducible to future cost.

Those remain open empirical/conceptual questions.

---

## 5. Acceptance tests

The initial executable contract is:

```text
ChangeOntCode/agents/co/tests/recursive_continuation_field_invariants.py
```

The tests use anonymous branch ids and check:

- high local support plus rising debt lowers collapse readiness;
- relief branches gain field viability from debtful branches;
- close grey rivals preserve nonclosure under cautious shapes;
- equivalent branches share quotient identity;
- compensating branches reduce debt;
- candidate rows acquire field terms without family policy;
- canonical field source contains no active family/action policy literals.

These tests are necessary but not sufficient. The next test layer is cross-family diagnostics that check whether v1 causes lawful branch-field telemetry without benchmark-specific tuning.

## Runtime contract closure update — 2026-05-15 live-read correction

The v1 runtime contract is partial but no longer merely pre-relation scaffold. The current code/docs path contains first-pass carriers for:

- branch identity precedence: `continuation_id → branch_id → candidate_id → action`;
- lawful public burden/effect facts;
- RelationSurface derivation from those facts;
- branch-internal operation carriers;
- relation coverage telemetry;
- CollapseCertificate gating before commitment;
- no forbidden fallback as defined in `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md`.

Evidence claims must still distinguish:

```text
first-pass relation/certificate-aware RCF path implemented and structurally traced
```

from:

```text
full CO-native recursive continuation field proven or empirically superior
```

The latter remains blocked by formula-ledger incompleteness, quotient/recursion open work, multi-step continuation identity, broader trace quality, controlled ablations, and known-algorithm comparisons.
