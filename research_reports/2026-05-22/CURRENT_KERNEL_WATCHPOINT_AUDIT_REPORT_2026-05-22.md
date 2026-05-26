# Current Kernel Watchpoint Audit v1 — 2026-05-22

## Claim boundary

Audit of first-pass diagnostic-map watchpoints only. It interprets mechanism visibility/action sensitivity and code-path alignment. It is not benchmark evidence, not CO proof, not novelty evidence, and not a coefficient-tuning pass.

## Data source

This audit reads `ChangeOntCode/outputs/current_kernel_diagnostic_map_v1/runs.jsonl` and `steps.jsonl`. It does not rerun benchmarks and does not change kernel behavior.

## Main verdict

The targeted hardening pass made DynamicShapeField readout-visible, split recursion-pressure provenance, and added compact row-level traces. Remaining watchpoints are narrower: quotient missed/false-equivalence audit and maintenance action-insensitivity under capped diagnostic ablations.

## Findings

### HF1_DYNAMIC_SHAPE_NOW_READOUT_VISIBLE — resolved-watchpoint

**Finding:** DynamicShapeField effective controls are now consumed by CommitmentSurface direct-control snapshot when present, so dynamic shape is no longer only CandidateSurface telemetry.

**Evidence:** 144 full-current diagnostic steps report dynamic_shape_controls_applied_in_commitment=true; direct_controls_used now logs dynamic_shape_* gauge fields.

**Next action:** Continue treating dynamic shape as first-pass: audit whether remaining telemetry-only cases are legitimate non-decisiveness or readout dominance.

### HF2_RECURSION_PROVENANCE_SPLIT — resolved-watchpoint

**Finding:** RecursionScheduler now publishes structural, sampling/uncertainty, weak-procedural, and inherited-field channels separately; only the structural channel becomes certificate-facing recursion demand.

**Evidence:** 0 full-current steps had avg structural recursion demand >= 0.35 with only decision_slot_competition relations after the split.

**Next action:** Audit false negatives/positives on real traces before changing coefficients.

### HF3_DEEP_TRACE_LOGGING_ADDED — partially-resolved-watchpoint

**Finding:** Diagnostic map now logs compact row-level traces, final direct controls, DynamicShapeField effective controls, recursion provenance channels, and canonical commitment assessments.

**Evidence:** 726 diagnostic steps contain row_trace_sample data.

**Next action:** Still add quotient accept/reject reason logging; row trace now exposes quotient output but not every rejected profile comparison.

### WF3_QUOTIENT_CONSERVATIVE_BUT_UNAUDITED_FOR_MISSES — medium

**Finding:** Quotienting remains conservative and appears where public residual profiles match, but missed-quotient status is not yet auditable because rejected profile reasons are not logged.

**Evidence:** quotient rows are mainly latent/maze/maintenance-bandit_like; renewal and maintenance middle/renewal_like still show zero quotient rows despite relation traffic.

**Next action:** Log quotient profile accept/reject reasons per step and add a false-quotient/missed-quotient audit before calibration.

### WF4_MAINTENANCE_ACTION_INSENSITIVITY_REMAINS — medium

**Finding:** Maintenance middle/renewal_like remain mostly action-insensitive under recent mechanism ablations in this capped diagnostic even after readout visibility hardening. Some metrics/modes move, but action prefixes remain unchanged.

**Evidence:** maintenance middle and renewal_like still have zero prefix action differences for static_shape/no_scheduler/no_quotient in the map.

**Next action:** Use the new row-level traces to decide whether this is legitimate non-decisiveness or dominance/stable-continuation swamping before tuning coefficients.

## Telemetry-only ablations

These are cases where a recent-mechanism ablation changed mechanism telemetry but did not change the action prefix in the capped run.

| family | mode | ablation | metric Δ | dyn-step Δ | recursion Δ | quotient-row Δ | full modes | ablation modes |
|---|---|---|---:|---:|---:|---:|---|---|
| latent_mechanism | easy_visible | no_scheduler | 0.000 | 0 | -0.108 | 0.000 | `{"dominance": 9, "stable_continuation": 5}` | `{"dominance": 9, "stable_continuation": 5}` |
| maintenance_replacement | bandit_like | static_shape | 0.000 | -24 | -0.002 | 0.000 | `{"dominance": 24}` | `{"dominance": 24}` |
| maintenance_replacement | bandit_like | no_scheduler | 0.000 | 0 | -0.006 | 0.000 | `{"dominance": 24}` | `{"dominance": 24}` |
| maintenance_replacement | bandit_like | no_quotient | 0.000 | 0 | 0.004 | -2.000 | `{"dominance": 24}` | `{"dominance": 24}` |
| maintenance_replacement | bandit_like | minimal_recent_core | 0.000 | -24 | -0.006 | -2.000 | `{"dominance": 24}` | `{"dominance": 24}` |
| maintenance_replacement | middle | static_shape | 4.050 | -24 | -0.018 | 0.000 | `{"dominance": 18, "stable_continuation": 6}` | `{"dominance": 22, "stable_continuation": 2}` |
| maintenance_replacement | middle | no_scheduler | 0.000 | 0 | -0.092 | 0.000 | `{"dominance": 18, "stable_continuation": 6}` | `{"dominance": 18, "stable_continuation": 6}` |
| maintenance_replacement | middle | minimal_recent_core | 4.050 | -24 | -0.092 | 0.000 | `{"dominance": 18, "stable_continuation": 6}` | `{"dominance": 22, "stable_continuation": 2}` |
| maintenance_replacement | renewal_like | static_shape | 0.000 | -24 | -0.015 | 0.000 | `{"reopen_or_sample": 1, "stable_continuation": 23}` | `{"reopen_or_sample": 1, "stable_continuation": 23}` |
| maintenance_replacement | renewal_like | no_scheduler | 0.000 | 0 | -0.105 | 0.000 | `{"reopen_or_sample": 1, "stable_continuation": 23}` | `{"reopen_or_sample": 1, "stable_continuation": 23}` |
| maintenance_replacement | renewal_like | minimal_recent_core | 0.000 | -24 | -0.105 | 0.000 | `{"reopen_or_sample": 1, "stable_continuation": 23}` | `{"reopen_or_sample": 1, "stable_continuation": 23}` |
| maze | static_visible_5x5 | static_shape | 0.000 | -10 | -0.006 | 0.000 | `{"dominance": 6, "stable_continuation": 4}` | `{"dominance": 6, "stable_continuation": 4}` |
| maze | static_visible_5x5 | no_scheduler | 0.000 | 0 | -0.038 | 0.000 | `{"dominance": 6, "stable_continuation": 4}` | `{"dominance": 6, "stable_continuation": 4}` |
| maze | static_visible_5x5 | no_quotient | 0.000 | 0 | 0.010 | -0.800 | `{"dominance": 6, "stable_continuation": 4}` | `{"dominance": 6, "stable_continuation": 4}` |
| maze | static_visible_5x5 | minimal_recent_core | 0.000 | -10 | -0.038 | -0.800 | `{"dominance": 6, "stable_continuation": 4}` | `{"dominance": 6, "stable_continuation": 4}` |
| renewal | noisy_renewal | no_scheduler | 0.000 | 0 | -0.162 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| renewal | noisy_renewal | minimal_recent_core | 0.000 | -16 | -0.162 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |

## Full-current relation summaries

| family | mode | avg recursion | max recursion | avg quotient rows | shape resolver steps | relations by type | modes |
|---|---|---:|---:|---:|---:|---|---|
| bandit | easy_public_bandit | 0.190 | 0.234 | 0.000 | 1 | `{"decision_slot_competition": 96}` | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| latent_mechanism | easy_visible | 0.108 | 0.378 | 2.143 | 0 | `{"decision_slot_competition": 154, "equivalence": 24, "relief": 22, "shared_evidence": 15}` | `{"dominance": 9, "stable_continuation": 5}` |
| latent_mechanism | hidden_depth2 | 0.370 | 0.593 | 1.500 | 0 | `{"decision_slot_competition": 148, "equivalence": 15, "relief": 25, "shared_evidence": 13}` | `{"reopen_or_sample": 16}` |
| maintenance_replacement | bandit_like | 0.006 | 0.066 | 2.000 | 0 | `{"cancellation": 72, "decision_slot_competition": 480, "equivalence": 24, "relief": 48}` | `{"dominance": 24}` |
| maintenance_replacement | middle | 0.092 | 0.173 | 0.000 | 0 | `{"buffering": 24, "cancellation": 48, "decision_slot_competition": 480, "relief": 24, "shared_evidence": 24}` | `{"dominance": 18, "stable_continuation": 6}` |
| maintenance_replacement | renewal_like | 0.105 | 0.340 | 0.000 | 5 | `{"buffering": 24, "cancellation": 48, "decision_slot_competition": 480, "relief": 24, "shared_evidence": 6}` | `{"reopen_or_sample": 1, "stable_continuation": 23}` |
| maze | static_visible_5x5 | 0.038 | 0.070 | 0.800 | 0 | `{"decision_slot_competition": 52, "equivalence": 4, "relief": 18}` | `{"dominance": 6, "stable_continuation": 4}` |
| renewal | noisy_renewal | 0.162 | 0.267 | 0.000 | 0 | `{"decision_slot_competition": 192}` | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |

## Weak-only high-recursion watchpoint

Count: `0` full-current steps had avg recursion demand >= 0.35 while relation types were only `decision_slot_competition`.


## Recommendation

Do not add robot/simulation yet. Next audit quotient missed/false equivalence and maintenance action-insensitivity using the newly deepened row-level traces.

## Publication/evidence boundary

This audit supports only a local engineering/theory-alignment conclusion: the first-pass kernel has visible generic mechanisms, but the current traces expose specific alignment gaps. It should not be cited as performance evidence or as evidence that CO is useful or novel.
