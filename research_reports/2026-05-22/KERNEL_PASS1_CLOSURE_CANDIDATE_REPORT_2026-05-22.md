# Kernel Pass-1 Closure Candidate Report — 2026-05-22

## Claim boundary

This report marks a **Pass-1 kernel closure candidate**, not a final kernel, not empirical proof, not SOTA comparison, and not publication readiness.  It means the known first-pass CO runtime mechanism set now exists in rough, auditable form.

## Implemented in this slice

Generic first-pass sequence-level continuation composition was added at:

- `ChangeOntCode/agents/co/runtime/surfaces/sequence_composition.py`

It is wired through `CandidateSurface` before the continuation field and after relation derivation.  It derives public phase signatures and sequence transitions from public effects and row telemetry.  It does not use family names, native action-name rules, hidden state, reward hindsight, DP/baseline values, shortest paths, or topology edits.

The rough sequence patterns are generic phase progressions such as:

- carried/unresolved burden → public exposure
- carried burden → direct relief
- public exposure → burden relief
- relief/exposure → stabilized continuation
- continued relief phase

This is not a planner and not a problem-specific sequence template.  Current-candidate phase topology is treated as weaker than observed selected-feedback sequence.

## New diagnostics and tests

Added:

- `ChangeOntCode/agents/co/tests/sequence_composition_first_pass_invariants.py`
- `ChangeOntCode/experiments/studies/sequence_composition_microcase_probe_v1.py`
- `ChangeOntCode/agents/co/tests/sequence_composition_microcase_probe_invariants.py`
- `research_reports/2026-05-22/SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md`

Updated:

- `current_kernel_diagnostic_map_v1.py` now includes a `no_sequence` ablation and sequence telemetry.
- `sequence_level_continuation_composition_audit_v1.py` now treats sequence composition as first-pass present while preserving the warning that adequacy is unproven.
- Generic readout/maintenance audits now distinguish “sequence missing” from “sequence present but readout consumption/action sensitivity still unresolved.”

## Key observed results

Selected reruns produced:

```text
sequence_composition_microcase_probe_v1:
  cases = 5
  passed = 5
  failed = 0
  all_passed = true

current_kernel_diagnostic_map_v1:
  runs_attempted = 48
  runs_succeeded = 48
  runs_failed = 0

sequence_level_continuation_composition_audit_v1:
  full_current_steps = 124
  row_trace_sample_rows = 511
  sequence_field_rows = 511
  sequence_active_rows = 176

generic_readout_swamping_trace_audit_v1:
  sequence_active_steps = 74
  sequence_active_rows = 176
  avg_support_stability_field_share ≈ 0.949
  avg_penalty_ratio ≈ 0.149
  carrier_with_resolver_alt_steps = 104
  carrier_with_resolver_no_shape_trigger_steps = 98

maintenance_action_insensitivity_audit_v1:
  insensitive_comparison_count = 10
  sensitive_comparison_count = 0

structural_trace_validation_v1:
  status = PASS_WITH_WATCHPOINTS
  cases_with_watchpoints = 1

architecture_acceptance_audit_v1:
  status = ACCEPTANCE_WATCHPOINTS_REMAIN
```

## Interpretation

The rough known kernel mechanism set is now present enough to freeze as a Pass-1 closure candidate:

- boundary/adapter split
- static shape prior
- DynamicShapeField
- CandidateSurface
- cross-action continuation memory
- burden operation typing
- RelationSurface
- quotient/equivalence helper
- recursion scheduler
- sequence-level composition
- CollapseCertificate
- CommitmentSurface
- mechanism ablation/diagnostic telemetry

This does **not** mean the kernel is good enough.  It means the next correct move is no longer “add the next missing known mechanism.”  The next move is freeze/evaluate.

## Remaining watchpoints

The current kernel still has serious watchpoints:

1. Sequence composition is first-pass and auditable, but behavioral adequacy is unproven.
2. Readout can still privilege support/stability/field mass over burden/resolver/sequence evidence.
3. Maintenance middle/renewal-like remain action-prefix insensitive under capped recent-mechanism ablations.
4. Quotient/equivalence remains conservative and needs real-trace false/missed quotient analysis.
5. Recursion scheduler annotates/gates demand but does not implement full second-layer unfolding.
6. Formula/coefficient grounding remains provisional.
7. Adapter boundary still needs adversarial validation.
8. Robot/simulation problems should wait until this closure candidate has been evaluated.

## Necessity gate after this point

No new kernel mechanism should be added unless all conditions hold:

1. Existing mechanisms cannot express the failure.
2. The missing structure is required by the CO theory/docs or by a lawful robot/sim boundary need.
3. The mechanism is generic, not family/action-name/benchmark-specific.
4. It has positive and negative microcases.
5. It can fail, be ablated, and be removed if it does not behave as expected.

## Recommended next step

Run a Pass-1 evaluation package:

- all-current-family diagnostics with sequence on/off and existing ablations;
- adapter-boundary stress tests;
- formula/coefficient sensitivity checks;
- readout-swamping post-sequence audit;
- quotient false/missed quotient audit;
- failure map explaining what CO actually does and where it degenerates into scoring.

Only after that should robot/simulation problem design begin.
