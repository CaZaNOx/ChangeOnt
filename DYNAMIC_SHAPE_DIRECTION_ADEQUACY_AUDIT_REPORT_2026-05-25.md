# DynamicShapeField Direction/Adequacy Audit — 2026-05-25

Audit-only DynamicShapeField direction/adequacy check. It does not change the kernel, does not use native family/action rules, and does not assert an optimal action. It only checks whether score/margin effects are structurally directional in public carrier/resolver contexts.

## Summary

The previous investigation showed that DynamicShapeField was not inert: many allegedly suspicious cases had score/margin effects. This audit asks the next question: in public carrier/resolver contexts, do those score effects move in a structurally plausible direction?

## Counts

```json
{
  "avg_margin_delta_by_classification": {
    "margin_narrows_toward_resolver_or_exposure": -0.0197473294307781,
    "margin_neutral": -0.0016776540064366203,
    "margin_widens_toward_selected_carrier": 0.01295140266172512,
    "not_directional_carrier_resolver_context": -0.032281589222538855
  },
  "counts": {
    "margin_narrows_toward_resolver_or_exposure": 16,
    "margin_neutral": 6,
    "margin_widens_toward_selected_carrier": 1,
    "not_directional_carrier_resolver_context": 101,
    "strong_margin_narrows_toward_resolver_or_exposure": 16,
    "strong_margin_neutral": 6,
    "strong_margin_widens_toward_selected_carrier": 1,
    "strong_not_directional_carrier_resolver_context": 93
  }
}
```

## By family/mode

| family/mode | counts |
|---|---|
| bandit/easy_public_bandit | `{"not_directional_carrier_resolver_context": 16, "total": 16}` |
| latent_mechanism/easy_visible | `{"not_directional_carrier_resolver_context": 14, "total": 14}` |
| latent_mechanism/hidden_depth2 | `{"not_directional_carrier_resolver_context": 16, "total": 16}` |
| maintenance_replacement/bandit_like | `{"not_directional_carrier_resolver_context": 18, "total": 18}` |
| maintenance_replacement/middle | `{"margin_narrows_toward_resolver_or_exposure": 16, "margin_neutral": 1, "margin_widens_toward_selected_carrier": 1, "total": 18}` |
| maintenance_replacement/renewal_like | `{"margin_neutral": 5, "not_directional_carrier_resolver_context": 13, "total": 18}` |
| maze/static_visible_5x5 | `{"not_directional_carrier_resolver_context": 8, "total": 8}` |
| renewal/noisy_renewal | `{"not_directional_carrier_resolver_context": 16, "total": 16}` |

## Findings

- **DS_DIRECTIONAL_CONTEXTS_EXIST** (info): Dynamic-shape directional contexts exist where a selected carrier/stabilizer is opposed by a public resolver/exposure runner-up. Evidence: directional_contexts=23, narrows=16, widens=1, neutral=6. Next: Use these directional contexts for future adequacy checks; do not rely on aggregate action changes alone.

## Interpretation

DynamicShapeField is readout-visible, but adequacy is not settled. The important remaining question is directional: when shape should make an exposure/relief alternative matter against a selected carrier/stabilizer, does dynamic shape narrow the margin toward that alternative, widen the selected carrier, or remain neutral?

This audit does not assert which action is optimal. It only marks generic public structural contexts for manual review. Widening the selected carrier may be legitimate if the local shape really supports stabilization; it is a watchpoint if CO expected pre-blocking exposure/relief pressure.

## Next recommended step

Manually inspect the directional contexts, especially maintenance modes. If widening toward the selected carrier is not justified by shape/certificate state, the issue is readout/control adequacy, not a missing new concept.
