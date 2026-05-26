# Generic Readout-Swamping Trace Audit v1 — 2026-05-22

## Claim boundary

Generic readout-swamping trace audit only. It is not a benchmark, not SOTA comparison, not CO proof, and not a license for family-specific tuning or action-name rules.

## Overall

Full-current steps: 124.
Average support/stability/field share of positive dominance mass: 0.949.
Average dominance penalty ratio: 0.149.
Carrier-with-resolver-alt steps: 104.
Carrier-with-resolver-alt without shape trigger: 98.
Steps with active sequence composition: 74.
Active sequence rows: 176.

## Findings

### GRS1_READOUT_SWAMPING_REMAINS_GENERIC_WATCHPOINT (medium)

Finding: Many selected commitments still have high support/stability/field dominance mass relative to burden/blocker penalties.

Evidence: avg_support_stability_field_share=0.949; avg_penalty_ratio=0.149

Next action: Do not tune a family. Sequence composition is now present; use sequence on/off diagnostics and generic resolver-readout tests before any further coefficient change.

### GRS2_CARRIER_RESOLVER_NO_TRIGGER_CASES_REMAIN (medium)

Finding: The trace still contains cases where a selected carrier coexists with generic resolver alternatives but shape-gauged timing does not trigger.

Evidence: carrier_with_resolver_alt_steps=104; no_shape_trigger=98

Next action: Separate legitimate non-decisiveness from insufficient sequence-readout consumption; no native action-name patch.

### GRS3_ABLATION_INSENSITIVITY_REMAINS_FAMILY_DEPENDENT (medium)

Finding: Some families/modes remain action-prefix insensitive to recent generic mechanism ablations while others are sensitive.

Evidence: insensitive_comparisons=27; sensitive_comparisons=13

Next action: Inspect whether insensitive families lack decisive structural relations, have dominance swamping, or fail to consume sequence evidence before adding robot/sim.

## By family/mode

| family/mode | steps | dominance steps | avg support-field share | avg penalty ratio | carrier+resolver | no trigger | seq steps | seq rows |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bandit::easy_public_bandit | 16 | 11 | 0.960 | 0.204 | 16 | 15 | 1 | 1 |
| latent_mechanism::easy_visible | 14 | 9 | 0.953 | 0.027 | 3 | 3 | 0 | 0 |
| latent_mechanism::hidden_depth2 | 16 | 0 | 0.948 | 0.465 | 13 | 13 | 13 | 15 |
| maintenance_replacement::bandit_like | 18 | 18 | 0.931 | 0.024 | 18 | 18 | 18 | 54 |
| maintenance_replacement::middle | 18 | 18 | 0.946 | 0.058 | 18 | 18 | 18 | 59 |
| maintenance_replacement::renewal_like | 18 | 0 | 0.968 | 0.110 | 18 | 13 | 14 | 35 |
| maze::static_visible_5x5 | 8 | 6 | 0.945 | 0.052 | 2 | 2 | 7 | 9 |
| renewal::noisy_renewal | 16 | 11 | 0.942 | 0.219 | 16 | 16 | 3 | 3 |

## Sample carrier/resolver/no-trigger cases

- `bandit::easy_public_bandit` t=0 action=`0` share=0.948 penalty=0.395 reason=`no_dominance_and_unresolved_sampling_or_revision_pressure`
- `bandit::easy_public_bandit` t=1 action=`0` share=0.965 penalty=0.173 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=2 action=`0` share=0.966 penalty=0.199 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=3 action=`0` share=0.966 penalty=0.212 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=4 action=`0` share=0.967 penalty=0.219 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=5 action=`0` share=0.967 penalty=0.223 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=6 action=`0` share=0.967 penalty=0.224 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=7 action=`0` share=0.967 penalty=0.225 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=8 action=`0` share=0.968 penalty=0.225 reason=`one_candidate_dominates_support_burden_stability`
- `bandit::easy_public_bandit` t=10 action=`2` share=0.932 penalty=0.330 reason=`no_dominance_and_unresolved_sampling_or_revision_pressure`
- `bandit::easy_public_bandit` t=11 action=`1` share=0.968 penalty=0.128 reason=`least_burden_stable_continuation_after_non_dominance`
- `bandit::easy_public_bandit` t=12 action=`2` share=0.968 penalty=0.129 reason=`least_burden_stable_continuation_after_non_dominance`

## Interpretation

The remaining watchpoint is generic: current readout can still privilege support/stability/field mass over unresolved burden and phase-like resolver alternatives. Generic sequence-composition is now present in first pass, so the next question is not whether to add a sequence layer, but whether the readout consumes sequence evidence appropriately or still collapses into dominance scoring. The trace does not justify a family-specific patch.
