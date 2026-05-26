# Multi-Step Continuation Identity Update — 2026-05-21

## Scope

This update implements a **first-pass continuation-memory layer** for the branch≠action doctrine.

It does not complete the full multi-step branch-identity problem.  It gives the runtime a bounded way to let different native action expressions inherit continuation memory when they operate on the same public burden domain, while preserving distinct RelationSurface branch identities for current-step relations, certificates, and commitment.

## Problem addressed

Before this update, `CandidateEvidenceSurface` updated `ContinuationStateTracker` using the native candidate/action expression before RelationSurface derived richer branch identities.  Downstream RelationSurface and RCF used the intended precedence:

```text
continuation_id → branch_id → candidate_id → action
```

but pre-relation temporal memory was still mostly action/candidate-expression keyed.

This left an implementation gap relative to docs `01B`, `44`, `76`, `95`, and `96`: CO says a branch is not an action and may persist across changing action expressions, but candidate-side memory did not yet reflect that.

## Implementation

New/changed code:

```text
ChangeOntCode/agents/co/runtime/surfaces/continuation_state.py
ChangeOntCode/agents/co/runtime/surfaces/candidate_surface.py
ChangeOntCode/agents/co/tests/multi_step_continuation_identity_invariants.py
ChangeOntCode/experiments/studies/multi_step_continuation_identity_probe_v1.py
```

Added:

```text
derive_continuation_memory_id(...)
ContinuationStateTracker.update_candidate_batch(...)
```

The new continuation-memory key derives from public burden-domain evidence:

```text
public_basis must be allowed;
leakage_status must be public/non-oracle;
decision-slot facts are ignored;
key uses coupling / scope / burden_type or relation_scope;
operation and native action name are not identity sources.
```

Thus, for example, two different current action expressions that both operate on public `degradation` under `health_continuation` can share continuation memory, while hiddenness and degradation remain distinct domains.

The memory key is deliberately weaker than `branch_id`:

```text
continuation_memory_id = persistence memory / cross-expression continuity hint
branch_id / continuation_id = current runtime branch identity for relation, RCF, certificate, commitment
```

RelationSurface branch IDs remain distinct when current action expressions/effects differ.  This prevents the memory layer from quotienting or merging live branches.

## Structural validation

New invariant/probe:

```text
python -m agents.co.tests.multi_step_continuation_identity_invariants
python -m experiments.studies.multi_step_continuation_identity_probe_v1
```

Observed probe summary:

```json
{
  "study": "multi_step_continuation_identity_probe_v1",
  "cases": 5,
  "passed": 5,
  "failed": 0,
  "all_passed": true,
  "claim_boundary": "first-pass structural continuation-memory validation only; not final multi-step branch identity"
}
```

Protected cases:

```text
- same public burden domain can persist across different action expressions;
- distinct public burden domains do not merge;
- batch tracker updates shared memory once per step, avoiding same-step artificial aging;
- CandidateSurface can share continuation memory without collapsing branch IDs;
- native action fallback remains last resort only.
```

## Claim boundary

This update does **not** prove the full multi-step branch identity doctrine.  It does not yet implement a higher-order continuation such as the whole sequence:

```text
INSPECT → REPAIR → RUN
```

as a single named or derived branch like `restore stable operation`.

It does implement the first required runtime distinction:

```text
candidate/action expression memory is no longer the only temporal memory key;
public burden-domain continuity can carry across different action expressions.
```

Still open:

```text
- multi-stage continuation composition across different burden domains;
- transition grammar between exposure, relief, and stable operation phases;
- relation between continuation-memory groups and future quotient/equivalence;
- robot/simulation cases where action expression changes are structurally necessary.
```
