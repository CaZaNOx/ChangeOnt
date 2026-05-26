# DynamicShapeField Real-Trace Ablation — 2026-05-21

## Scope

This is a structural trace ablation.  It compares identical public candidate
facts with DynamicShapeField enabled vs disabled.  It is not reward evidence and
not a benchmark.

## Summary

```json
{
  "claim_boundary": "structural telemetry/ablation only; absence of action change is not hidden",
  "commitment_difference_observed": false,
  "disabled_run_has_no_dynamic_shape_update": true,
  "invariants": {
    "dynamic_shape_ablation_is_visible": true,
    "dynamic_shape_state_updates_from_public_trace": true,
    "no_behavior_change_is_allowed_and_reported": true
  },
  "next_cycle_effective_controls_changed": true,
  "state_changed_after_public_trace": true,
  "study": "dynamic_shape_real_trace_ablation_v1"
}
```
