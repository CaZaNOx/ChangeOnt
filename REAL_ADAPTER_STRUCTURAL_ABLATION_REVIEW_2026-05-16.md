# Real Adapter Structural Ablation Review — 2026-05-16

Status: structural mechanism-causality review.  
Claim boundary: not reward evidence, not novelty proof, not broad benchmark evidence.

## Why this review exists

The previous real-adapter certificate review showed that the certificate-aware
readout corrections are live on public adapter rows, especially through
`reopen_or_sample`.  That is not enough by itself.  The next integrity question
is whether the current runtime actually depends on CO public-effect structure,
or whether the same decisions would occur from candidate support alone.

This review therefore runs the same broad public-observation sweep under
structural ablations of adapter `public_effects`.

## Probe added

```text
ChangeOntCode/experiments/studies/real_adapter_structural_ablation_review_v1.py
ChangeOntCode/agents/co/tests/real_adapter_structural_ablation_review_invariants.py
```

The sweep covers:

```text
standard trace samples: 5
maintenance public-observation sweep: 216
latent-mechanism public-observation sweep: 90
total: 311 cases
```

## Variants

| Variant | Meaning |
|---|---|
| `full` | Adapter candidate rows unchanged. |
| `no_public_effects` | Removes public burden/effect facts. |
| `weak_competition_only` | Keeps only procedural decision-slot facts. |
| `no_weak_competition` | Removes decision-slot facts while keeping burden/effect facts. |
| `branch_internal_only_unique_scope` | Keeps burden/effect facts but breaks shared relation scopes, suppressing cross-branch topology. |
| `no_resolver_ops` | Removes exposure/reduction/cancellation/buffer/transform facts. |
| `carrier_only_no_resolver` | Keeps carry/mask/postpone/defer plus decision-slot facts only. |

## Aggregate result

```json
{
  "cases": 311,
  "full_modes": {
    "dominance": 29,
    "reopen_or_sample": 111,
    "stable_continuation": 171
  },
  "full_certificate_aware_reopen_cases": 66,
  "full_certificate_aware_stable_cases": 0,
  "comparisons_vs_full": {
    "no_public_effects": {
      "action_changes": 76,
      "mode_changes": 28,
      "reason_changes": 93,
      "selected_blocked_changes": 42,
      "certificate_aware_reopen_changes": 66,
      "positive_structural_relation_delta_cases": 309,
      "positive_branch_internal_delta_cases": 311
    },
    "weak_competition_only": {
      "action_changes": 76,
      "mode_changes": 28,
      "reason_changes": 93,
      "selected_blocked_changes": 42,
      "certificate_aware_reopen_changes": 66,
      "positive_structural_relation_delta_cases": 309,
      "positive_branch_internal_delta_cases": 311
    },
    "no_weak_competition": {
      "action_changes": 0,
      "mode_changes": 0,
      "reason_changes": 0,
      "selected_blocked_changes": 0,
      "certificate_aware_reopen_changes": 0,
      "positive_structural_relation_delta_cases": 0,
      "positive_branch_internal_delta_cases": 0
    },
    "branch_internal_only_unique_scope": {
      "action_changes": 19,
      "mode_changes": 19,
      "reason_changes": 32,
      "selected_blocked_changes": 12,
      "certificate_aware_reopen_changes": 16,
      "positive_structural_relation_delta_cases": 309,
      "positive_branch_internal_delta_cases": 0
    },
    "no_resolver_ops": {
      "action_changes": 71,
      "mode_changes": 16,
      "reason_changes": 81,
      "selected_blocked_changes": 65,
      "certificate_aware_reopen_changes": 66,
      "positive_structural_relation_delta_cases": 309,
      "positive_branch_internal_delta_cases": 254
    },
    "carrier_only_no_resolver": {
      "action_changes": 71,
      "mode_changes": 16,
      "reason_changes": 81,
      "selected_blocked_changes": 65,
      "certificate_aware_reopen_changes": 66,
      "positive_structural_relation_delta_cases": 309,
      "positive_branch_internal_delta_cases": 254
    }
  }
}
```

## Interpretation

### 1. Public-effect structure is behavior-causal in the real sweep

Removing public effects changes 76 actions, 28 modes, and 93 reasons across 311
public-observation cases.  That is a meaningful structural signal: the active
runtime is not identical to scalar candidate support with relations merely logged
beside it.

### 2. Resolver operations are specifically causal

Removing resolver operations produces nearly the same action-level effect as
removing all public effects in the tested sweep:

```text
no_public_effects action changes: 76
no_resolver_ops action changes: 71
carrier_only_no_resolver action changes: 71
```

This means the recent resolver-aware `reopen_or_sample` correction is not only a
microcase artifact.  It is active in real maintenance/latent public rows.

### 3. Weak decision-slot competition is not driving behavior

Removing weak decision-slot competition while keeping burden/effect facts changes
nothing in this sweep:

```text
no_weak_competition action changes: 0
no_weak_competition mode changes: 0
```

This supports the intended separation:

```text
weak procedural competition != strong rivalry / burden relation
```

### 4. Cross-branch relation topology matters less than resolver presence, but is not inert

Breaking shared scopes while preserving branch-internal facts changes 19 actions
and 19 modes.  That is weaker than removing all public effects or resolver ops,
but not zero.  The current mechanism appears more sensitive to resolver/carrier
operation typing than to full cross-branch topology in this sweep.

This is not automatically bad, but it is important: if CO later claims relation
topology is central, future probes need cases where same scalar support and same
operation types but different relation topology produce stronger, explainable
behavior differences.

## What this does and does not show

Shows:

```text
- public-effect structure changes real adapter commitments;
- resolver operations are behaviorally important;
- weak procedural competition is not being mistaken for burden structure;
- branch-internal burden/resolver carriers are active in real sweeps;
- cross-branch topology has some effect but is not yet the dominant causal source.
```

Does not show:

```text
- reward improvement;
- CO novelty over known algorithms;
- final formula correctness;
- final quotient/recursion correctness;
- broad empirical success.
```

## Next implication

The next integrity task is formula/coefficient grounding for the behavior-affecting
readout rules that now demonstrably change real-adapter decisions:

```text
- resolver_support threshold;
- sampling_gate_margin;
- sampling_support_advantage_limit;
- continuation_gate_margin;
- support_advantage_limit;
- blocker_pressure construction;
- branch-internal carrier/resolver magnitudes.
```

The ablation result makes these ledgers more urgent, not less: the coefficients
are now known to alter real commitments.
