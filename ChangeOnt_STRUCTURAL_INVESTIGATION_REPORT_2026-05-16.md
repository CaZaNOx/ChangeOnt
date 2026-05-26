# ChangeOnt structural investigation report — 2026-05-16

## Claim boundary

This pass investigated the current CO runtime structurally. It is not reward evidence, not a proof of CO, and not a novelty claim. The question was whether the current RelationSurface / branch-internal burden carriers / RCF / CollapseCertificate / CommitmentSurface path behaves for structurally inspectable reasons rather than merely wrapping scalar action scoring in CO vocabulary.

## What was run

From `ChangeOnt_semantic_relevance_audited_2026-05-15.zip`, I ran and/or added:

- `python -m compileall -q agents environments experiments tools`
- `agents.co.tests.no_classical_fallback_fail_closed_invariants`
- `agents.co.tests.relation_surface_public_effect_invariants`
- `agents.co.tests.kernel_structure_carrier_alignment_invariants`
- `agents.co.tests.collapse_certificate_readout_invariants`
- `agents.co.tests.structural_trace_validation_invariants`
- `agents.co.tests.relation_path_trace_diagnostics`
- `agents.co.tests.code_vs_docs_pipeline_compliance_invariants`
- `agents.co.tests.certified_runtime_alignment_invariants`
- `experiments/studies/structural_trace_validation_v1.py`
- `experiments/studies/relation_path_trace_v1.py`
- `experiments/studies/architecture_acceptance_audit_v1.py`
- new: `experiments/studies/structural_ablation_probe_v1.py`

## Fixes made during investigation

### 1. Branch-internal carrier metric no longer counts weak slot facts

Problem found:
`branch_internal_operation_rows` could be satisfied by procedural `decision_slot` facts alone. That meant a weak-competition-only packet could appear to carry branch-internal burden operations even when no actual burden/effect operation existed.

Fix:
`RelationSurface` now excludes `decision_slot` / pure legal-constraint facts from `branch_internal_operation_count` and `branch_internal_operation_rows`. These facts remain relation telemetry only. A regression assertion was added to `kernel_structure_carrier_alignment_invariants.py`.

Result:
The real sampled full cases still report `branch_internal_operation_rows = 20`, because all sampled rows have non-slot burden/effect facts. But the metric is now meaningful: weak competition alone reports `0` branch-internal burden-operation rows.

### 2. Removed unreachable stale guide-like code from latent adapter

Problem found:
`latent_mechanism_adapter.py` contained unreachable code after an early `return` in `_problem_contract`. That dead block referenced `active_switch_hint` and a best-move style guide computation. It was not executed, but it was confusing and looked like potential hidden-solver residue.

Fix:
Removed the unreachable block. No runtime behavior changed because the block was dead.

### 3. Added structural ablation probe

Added `experiments/studies/structural_ablation_probe_v1.py`, which runs five variants on the sampled adapter cases:

- `full`
- `no_public_effects`
- `weak_competition_only`
- `no_weak_competition`
- `branch_internal_only_unique_scope`

This separates procedural weak competition from actual burden/effect carriers and gives a first view of whether relation topology, branch-internal burden, and certificate gates are doing different things.

## Current diagnostic results

### Existing structural traces

`structural_trace_validation_v1.py`:

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

`relation_path_trace_v1.py`:

```json
{
  "relations_total": 80,
  "non_rival_relations": 16,
  "commitment_action_changed_cases": 0,
  "commitment_mode_changed_cases": 1,
  "field_delta_positive_cases": 5
}
```

`architecture_acceptance_audit_v1.py` still reports:

```text
ACCEPTANCE_WATCHPOINTS_REMAIN
```

### New ablation probe aggregate

`structural_ablation_probe_v1.py`:

```json
{
  "cases": 5,
  "full_vs_no_public_action_changes": 0,
  "full_vs_no_public_mode_changes": 1,
  "full_vs_weak_only_action_changes": 0,
  "full_vs_weak_only_mode_changes": 1,
  "weak_only_branch_internal_rows": 0
}
```

## Content interpretation

### What looks structurally good

1. Weak decision-slot competition is now cleanly separated from burden carriers. Weak-only variants reproduce no-public-effect behavior and do not create branch-internal burden-operation rows.

2. In bandit and renewal initial cases, the behavior is driven by branch-internal uncertainty/evidence burden rather than cross-branch relations. Removing public effects opens certificate gates and lowers recursion/blocker pressure; keeping non-slot effects restores the blockers.

3. In latent-mechanism, public burden/effect structure changes the readout mode from `dominance` to `stable_continuation` by closing the certificate gate and setting `certificate_blocks_dominance = 1`. That is the strongest current sample showing the certificate actually changes the kind of commitment being claimed.

4. In maze, visible public structure increases the selected branch's dominance and continuation scores, but the action was already locally obvious. This is structurally unsurprising and should not be overclaimed.

### What remains weak or fragile

1. Original sampled cases show no action changes between full and no-public-effects; only one mode change. That means current evidence for relation/certificate influence on actual action choice is still thin.

2. Maintenance structural effects are weak in the sampled mid-health case. They reorder some internal rankings (`REPAIR` vs `RUN`) but do not change the selected action or mode. This may be acceptable, but it needs more targeted maintenance states before claiming the mechanism matters there.

3. Latent-mechanism synthetic branch-internal-only ablation selects `INTERACT` via sampling/reopen pressure while the full relation topology selects `RIGHT` as stable continuation. This suggests relation topology can stabilize against hiddenness-driven over-sampling, but it also exposes a formula-risk: branch-internal hiddenness pressure can drive sampling strongly even when the candidate does not publish an explicit reveal/reduce operation.

4. Formula grounding remains the largest integrity gap. The structural path is traceable, but many behavior-affecting coefficients remain provisional.

5. The architecture audit remains watchpoint-level, not acceptance-clean.

## Recommended next investigation

1. Keep this as the first ablation baseline. Do not tune constants from it.

2. Add targeted hand-designed microcases where the expected structural outcome is known:
   - weak competition only must never block dominance;
   - hiddenness carry without exposure should block dominance but not automatically prefer arbitrary probing;
   - explicit reveal/reduce should beat pure carry under high hiddenness only when public basis supports it;
   - relief/cancellation should alter only branches coupled by burden type/scope;
   - quotient/equivalence should lower grey pressure without erasing real burden differences.

3. Run a maintenance state sweep, not for reward, but for structural transitions:
   - healthy/low degradation should allow stable continuation;
   - mid degradation should produce repair/inspect tension;
   - high degradation should expose replacement/cancellation pressure;
   - hidden health should increase inspect/reveal relevance without using hidden state.

4. Build a formula ledger from these microcases. Every coefficient that decides dominance/reopen/stability should be tied to a structural expectation.

5. Only after these pass should broader reward baselines be interpreted.
