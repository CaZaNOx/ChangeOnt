# 94. Real-Trace Structural Validation and Formula Grounding

Status: active diagnostic contract / not reward evidence.  
Last verified in this working tree: 2026-05-15 against the current code path.

This document records the current structural trace validation target and the latest verified trace summary for the post-certificate-gate runtime. It is intentionally not a performance benchmark. Its purpose is to check whether the current kernel path can be inspected as a CO mechanism:

```text
public_effects
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

The pass also tracks formula-grounding debt for active scalar formulas.

---

## 1. Why this pass exists

The architecture-acceptance fixes corrected the immediate hard failures:

- weak decision-slot competition is separated from strong rivalry;
- branch identity includes coarse burden-regime bands;
- branch-internal burden operations survive even without cross-branch relations;
- CollapseCertificate separates weak competition from unresolved structural rivals;
- CommitmentSurface respects certificate gates and blocks dominance-style commitment when a certificate is non-ready under active blocker/recursion pressure;
- the initial formula ledger exists for readout-critical fields.

Those fixes are not evidence that the architecture is finished. The next question is whether sampled traces show coherent structural behavior rather than hidden rescue selection, relation noise, or scalar-only readout.

---

## 2. Validation method

The diagnostic compares the same representative adapter cases with relation-bearing public effects active and, internally, public effects stripped. It records:

- public effects and burden/effect types;
- branch-internal burden-operation rows;
- relations produced by RelationSurface;
- weak decision-slot competition versus structural relations;
- RCF field deltas;
- CollapseCertificate status and reasons;
- CommitmentSurface action and mode;
- formula coefficient scan and formula-ledger coverage watchpoints.

This pass uses representative cases from:

```text
bandit_initial
maintenance_partial_midhealth
maze_visible_local
latent_mechanism_visible
renewal_initial
```

---

## 3. Current verified result

Command:

```bash
cd ChangeOntCode
python -m experiments.studies.structural_trace_validation_v1
```

Output:

```text
outputs/structural_trace_validation_v1.json
```

Verified summary in this working tree:

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "relations_total": 80,
  "structural_relations": 16,
  "weak_decision_competition_relations": 64,
  "branch_internal_operation_rows": 20,
  "field_delta_positive_cases": 5,
  "commitment_changed_cases": 1,
  "cases_with_watchpoints": 0
}
```

The study status is still `PASS_WITH_WATCHPOINTS` because broader architecture-quality and formula-grounding work remains open. The case-level structural trace watchpoint count is now zero in this representative pass.

---

## 4. Interpretation by case type

### Bandit

- No cross-branch structural relations in the initial representative case.
- Branch-internal uncertainty operations are active.
- Mode remains `reopen_or_sample`, which is consistent with unresolved sampling/uncertainty pressure.

### Maintenance

- Relief, cancellation, and shared-evidence structures are present.
- Selected action remains stable under exposure/hiddenness handling.
- This is structurally inspectable, but public-effect magnitudes and certificate reasons still require broader formula grounding before paper claims.

### Maze

- Structural relations and quotient/topology-count changes are present.
- The selected branch has an earned-collapse-ready certificate in the sampled visible-local case.
- Topology/count shifts should not be confused with destabilizing scalar-field deltas.

### Latent mechanism

- The same native action may remain selected, but after the certificate-gate fix the mode changes from dominance-style commitment to stable continuation when hiddenness/recursion structure prevents earned dominance.
- This is a structural correction, not reward evidence.

### Renewal

- No cross-branch structural relations in the initial representative case.
- Branch-internal recurrence/uncertainty operations are active.
- Mode remains `reopen_or_sample`, consistent with unresolved sequence/phase uncertainty.

---

## 5. Acceptance condition for this trace diagnostic

A trace is structurally acceptable when:

1. public effects are leakage-safe;
2. weak decision-slot competition is logged separately from strong rivalry;
3. branch-internal operations survive even without cross-branch relations;
4. structural relations are sparse and typed;
5. RCF field changes can be traced to branch-internal operations and/or relation topology;
6. collapse certificates preserve structured reasons;
7. commitment changes, if any, are justified by certificate reasons;
8. unchanged commitments under field deltas are explainable as stable/earned, not ignored relation structure.

This diagnostic does not require every relation change to alter the final action. It requires that when actions do or do not change, the trace tells us why.

---

## 6. Formula grounding status

The current formula scan still detects many active coefficient lines across adapters and runtime surfaces. This is not automatically wrong, but it means the implementation remains a conceptually motivated provisional implementation rather than a final derived algorithm.

Critical active formula areas:

- adapter public-effect magnitudes;
- relation weights;
- burden-regime bands;
- RCF fields: debt, relief, grey, recursion, collapse readiness, viability;
- CollapseCertificate fields: blocker pressure, resolver support, earnedness, recursion demand;
- CommitmentSurface fields: dominance, sampling, stable continuation, certificate terms.

Before final paper claims, every active scalar that affects readout needs a ledger entry with:

```text
source structure
allowed inputs
forbidden inputs
monotonic direction
formula/constants
status class
family-tuning risk
tests/telemetry
paper-claim status
```

---

## 7. Relation to architecture acceptance audit

This trace diagnostic and the architecture acceptance audit answer different questions.

```text
structural_trace_validation_v1:
  representative trace cases currently show zero case-level watchpoints.

architecture_acceptance_audit_v1:
  still reports ACCEPTANCE_WATCHPOINTS_REMAIN for broader relation quality,
  branch identity trace quality, certificate reason quality, public-effect
  formula grounding, and formula-ledger completeness.
```

Do not collapse these into one status. A clean representative structural trace does not mean the architecture is critic-ready or empirically validated.

---

## 8. What this pass does not prove

This pass does not prove:

- performance improvement;
- algorithmic novelty;
- final burden algebra;
- final formula correctness;
- final quotient tolerance;
- six-question prior sufficiency;
- consciousness/meaning claims.

It only establishes that the current architecture can be structurally inspected on the sampled cases and that remaining issues are visible in trace/audit form.

---

## 9. Next required work

1. Expand manual trace review beyond the five representative cases.
2. Add later-history bandit/renewal traces where structural uncertainty/phase relations should appear.
3. Expand the formula ledger for adapter public-effect magnitudes and RCF/CollapseCertificate constants.
4. Add RelationSurface on/off and certificate on/off ablations.
5. Review same-scalar/different-relation-topology cases.
6. Only after this: broader family diagnostics and reward/performance comparisons.
