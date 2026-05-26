# DynamicShapeField Suspicious-Case Investigation — 2026-05-25

Audit-only investigation of DynamicShapeField strong-context suspicious cases. It compares full_current against static_shape rows, treats score/margin changes as readout consumption evidence, and classifies classifier-overreach vs residual watchpoints. It is not a kernel change, not a tuning license, and not CO proof.

## Summary

This audit investigates the DynamicShapeField cases previously flagged as `suspicious_strong_context_non_effect` by the context-conditioned expectation audit.

The main correction is that the prior audit was too strict: it counted only action changes or named gate/readout booleans as dynamic-shape consumption. Comparing `full_current` against `static_shape` shows that the allegedly suspicious cases still changed dominance scores/margins. They were usually not true no-effects.

## Counts

```json
{
  "investigation_counts": {
    "prior_classifier_overreach_refined_to_weak": 3,
    "readout_score_effect_not_counted_by_prior_audit": 66,
    "residual_true_suspicious_non_effect": 1
  },
  "prior_suspicious_cases": 70,
  "refined_expectation_counts_for_prior_suspicious": {
    "strong": 30,
    "weak": 40
  }
}
```

## By family/mode

| family/mode | total prior suspicious | main classifications |
|---|---:|---|
| latent_mechanism/easy_visible | 5 | `{"readout_score_effect_not_counted_by_prior_audit": 5}` |
| maintenance_replacement/bandit_like | 18 | `{"prior_classifier_overreach_refined_to_weak": 2, "readout_score_effect_not_counted_by_prior_audit": 16}` |
| maintenance_replacement/middle | 18 | `{"readout_score_effect_not_counted_by_prior_audit": 17, "residual_true_suspicious_non_effect": 1}` |
| maintenance_replacement/renewal_like | 13 | `{"prior_classifier_overreach_refined_to_weak": 1, "readout_score_effect_not_counted_by_prior_audit": 12}` |
| maze/static_visible_5x5 | 5 | `{"readout_score_effect_not_counted_by_prior_audit": 5}` |
| renewal/noisy_renewal | 11 | `{"readout_score_effect_not_counted_by_prior_audit": 11}` |

## Findings

- **DS_INVESTIGATION_SCORE_EFFECT_MISCOUNTED** (high): Most or all prior dynamic-shape suspicious cases are not true non-effects; full_current vs static_shape changes dominance scores/margins even when actions/gate flags do not change. Evidence: score_effect_cases=66, prior_suspicious_cases=70. Next: Update expectation audits to count material score/margin effects as readout consumption, while still separately auditing whether the direction is desirable.
- **DS_INVESTIGATION_CLASSIFIER_OVERREACH** (medium): Some prior strong dynamic contexts were over-classified because projection horizon/default shape-state was treated as strong without enough local structural trigger. Evidence: refined_non_strong_cases=3, prior_suspicious_cases=70. Next: Use the refined classifier for future context-conditioned audits; projection alone should usually be weak unless paired with resolver/sequence/blocker structure.
- **DS_INVESTIGATION_RESIDUAL_TRUE_SUSPICIOUS** (medium): A smaller residual set remains genuinely suspicious after score-effect and classifier-overreach checks. Evidence: residual_true_suspicious=1, prior_suspicious_cases=70. Next: Manually inspect residual rows before changing DynamicShapeField or CommitmentSurface.

## Interpretation

The correct conclusion is not that DynamicShapeField is inert. The better conclusion is that DynamicShapeField is already readout-visible at the score/margin level, but often not decisive at the action level. The previous suspicious count mostly reflected an audit-method limitation, not a proven runtime no-effect.

This does not prove DynamicShapeField is adequate. In maintenance-like modes, score effects are often small and may still leave RUN/stable continuation dominant. The next question is therefore directional/adequacy: are the score changes pushing the right structural relation, and are they large enough in contexts where CO says shape should matter?

## Next recommended step

Run a direction-and-adequacy audit for DynamicShapeField score effects, especially maintenance. Do not add a new mechanism and do not tune family-specific behavior from the old suspicious count.
