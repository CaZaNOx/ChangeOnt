# Systematic Mechanism Ablation Review — 2026-05-16

Status: **structural causality review, not reward evidence**.

Input: `ChangeOntCode/experiments/studies/real_adapter_structural_ablation_review_v1.py` over 311 real-adapter public-observation cases.

## Results

| Ablation | Action changes | Mode changes | Reason changes | Certificate-aware reopen changes | Selected-blocked changes |
|---|---:|---:|---:|---:|---:|
| `branch_internal_only_unique_scope` | 19 | 19 | 32 | 16 | 12 |
| `carrier_only_no_resolver` | 71 | 16 | 81 | 66 | 65 |
| `no_public_effects` | 76 | 28 | 93 | 66 | 42 |
| `no_resolver_ops` | 71 | 16 | 81 | 66 | 65 |
| `no_weak_competition` | 0 | 0 | 0 | 0 | 0 |
| `weak_competition_only` | 76 | 28 | 93 | 66 | 42 |

## Interpretation

- Public effects are behavior-causal: stripping them changes 76 / 311 actions.
- Resolver operations are behavior-causal: removing them changes 71 / 311 actions.
- Weak decision-slot competition alone is not the driver: removing weak competition changes 0 actions and 0 modes.
- Cross-branch relation topology matters, but current real sweeps show branch-internal resolver/carrier typing as the strongest structural lever.

## Boundary

This supports structural causality, not performance or novelty. It does not show that CO beats baselines. It shows that the active CO mechanisms are not merely decorative in the sampled real-adapter traces.
