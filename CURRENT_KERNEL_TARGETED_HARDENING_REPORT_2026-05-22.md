# Current Kernel Targeted Hardening Report — 2026-05-22

## Claim boundary

This is a first-pass kernel hardening update. It is not benchmark evidence, not CO proof, not novelty evidence, and not a coefficient-tuning pass.

## What was hardened

### 1. DynamicShapeField is now commitment-visible

Before this update, `DynamicShapeField` deformed CandidateSurface effective controls and row telemetry, but `CommitmentSurface` still read mostly static header/direct controls during final shape-gauged resolver timing.

Now:

- `CommitmentSurface._direct_control_snapshot(...)` consumes `__dynamic_shape_effective_controls__` when CandidateSurface publishes it.
- Static values are preserved under `static_*` telemetry keys before override.
- Dynamic fields such as `dynamic_shape_urgency`, `dynamic_shape_coarsening`, `dynamic_shape_projection_horizon`, and `dynamic_shape_gauge_confidence` are logged in `direct_controls_used`.
- This remains generic: no family names, action names, reward hindsight, hidden state, DP/baseline values, or topology edits are used.

### 2. Recursion provenance is split

Before this update, `RecursionScheduler` mixed inherited `field_recursion_budget` / sampling-like pressure into the same channel as structural recursion demand.

Now it publishes separate channels:

- `recursion_scheduler_structural_channel`
- `recursion_scheduler_sampling_uncertainty_channel`
- `recursion_scheduler_weak_procedural_channel`
- `recursion_scheduler_inherited_field_channel`
- `field_recursion_budget_before_scheduler`

Only the structural channel becomes certificate-facing `field_recursion_budget` and `recursion_scheduler_demand`. Sampling/uncertainty and weak procedural competition are logged but do not by themselves request another unfolding layer.

### 3. Diagnostic trace depth was increased

`current_kernel_diagnostic_map_v1` now logs compact row-level traces per step, including:

- selected row identities and continuation memory ids;
- dynamic effective controls;
- recursion provenance channels;
- pre/post scheduler field recursion budget;
- quotient fields;
- collapse/certificate fields;
- final `direct_controls_used`;
- `canonical_commitment_assessment` summaries.

## Rerun results

After hardening, the current diagnostic map completed:

```text
runs_attempted = 40
runs_succeeded = 40
runs_failed = 0
```

The updated watchpoint audit reports:

```text
dynamic_controls_commitment_steps = 144
deep_trace_steps = 726
weak_only_high_recursion_count = 0
```

The prior high-severity watchpoints are now narrowed:

- Dynamic shape is readout-visible.
- Weak-only high structural recursion is no longer observed in the capped full-current map.
- Deep row-level traces exist.

## Remaining watchpoints

### Quotient missed/false-equivalence audit is still pending

Quotient output is visible, but rejected quotient-profile comparisons are not logged. Therefore the repo still cannot distinguish:

- correct non-equivalence;
- missed quotient;
- false quotient avoided by chance.

Next needed step:

```text
Add quotient accept/reject reason logging and a real-trace quotient audit.
```

### Maintenance action-insensitivity remains unresolved

Maintenance middle and renewal-like regimes remain mostly action-prefix-insensitive under static-shape, no-scheduler, and no-quotient ablations in the capped diagnostic. Some telemetry, modes, and metrics move, but action prefixes often do not.

This may be correct non-decisiveness, or it may mean dominance/stable-continuation readout still swamps field structure.

Next needed step:

```text
Use the new row-level traces to audit maintenance action-insensitivity before tuning coefficients or adding robot/sim.
```

## Checks run

Passed selected checks:

```text
python tools/validate_toc_main.py
python -m compileall -q agents environments experiments tools
python -m agents.co.tests.current_kernel_hardening_invariants
python -m agents.co.tests.current_kernel_watchpoint_audit_invariants
python -m agents.co.tests.current_kernel_diagnostic_map_invariants
python -m agents.co.tests.recursion_scheduler_first_pass_invariants
python -m agents.co.tests.quotient_equivalence_first_pass_invariants
python -m agents.co.tests.multi_step_continuation_identity_invariants
python -m agents.co.tests.dynamic_shape_field_invariants
python -m agents.co.tests.dynamic_shape_microcase_probe_invariants
python -m agents.co.tests.dynamic_shape_real_trace_ablation_invariants
python -m agents.co.tests.certified_runtime_alignment_invariants
python -m agents.co.tests.no_classical_fallback_fail_closed_invariants
python -m agents.co.tests.relation_surface_public_effect_invariants
python -m agents.co.tests.kernel_structure_carrier_alignment_invariants
python -m agents.co.tests.collapse_certificate_readout_invariants
python -m agents.co.tests.code_vs_docs_pipeline_compliance_invariants
python -m agents.co.tests.structural_trace_validation_invariants
python -m agents.co.tests.relation_path_trace_diagnostics
python -m agents.co.tests.shape_gauged_resolver_timing_probe_invariants
```

Studies rerun:

```text
python -m experiments.studies.current_kernel_diagnostic_map_v1
python -m experiments.studies.current_kernel_watchpoint_audit_v1
python -m experiments.studies.architecture_acceptance_audit_v1
python -m experiments.studies.structural_trace_validation_v1
python -m experiments.studies.relation_path_trace_v1
```

Important remaining status:

```text
architecture_acceptance_audit_v1 = ACCEPTANCE_WATCHPOINTS_REMAIN
structural_trace_validation_v1 = PASS_WITH_WATCHPOINTS, cases_with_watchpoints = 1
```

## Next recommendation

Do not add robot/simulation yet.

Next best step:

```text
1. Add quotient accept/reject reason logging.
2. Run a real-trace quotient false/missed-equivalence audit.
3. Use the new deep traces to audit maintenance action-insensitivity.
4. Only then decide whether the current first-pass kernel is ready for robot/sim problem introduction.
```
