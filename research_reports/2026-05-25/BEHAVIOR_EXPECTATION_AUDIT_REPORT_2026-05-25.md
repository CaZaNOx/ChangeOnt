# Behavior Expectation Audit — 2026-05-25

## Claim boundary
Behavior expectation audit only. It does not change kernel behavior, does not tune coefficients, is not benchmark evidence, and does not prove CO. It compares observed diagnostic behavior against the expected role of each Pass-1 kernel mechanism.

## Overall verdict

The closure candidate **does not yet behave as expected for a strong/releasable CO kernel**. It behaves roughly as expected for a Pass-1 research kernel in the narrow sense that the mechanisms exist, their microcases pass, and ablations expose telemetry/action effects in some families. But real-trace commitment consumption remains too weak and uneven.

In cold terms: **mechanism presence is substantially achieved; mechanism use is not yet strong enough.**

## Diagnostic run status

- current_kernel_diagnostic_map: 48/48 runs succeeded; failures=0.
- sequence microcases: 5/5 passed.
- structural_trace_validation: PASS_WITH_WATCHPOINTS with cases_with_watchpoints=1.
- architecture_acceptance_audit: ACCEPTANCE_WATCHPOINTS_REMAIN.

## Mechanism expectation table

| Mechanism | Expected role | Observed | Verdict |
|---|---|---|---|
| Sequence composition microcases | positive/negative generic microcases pass without action/family rules | 5/5 passed | behaves_as_expected_in_microcases |
| Sequence composition real traces | sequence phase telemetry appears in real rows; no_sequence ablation should expose whether readout consumes it | sequence_field_rows=511; sequence_active_rows=176; no_sequence action-sensitive modes=1/8 | partially_expected_but_readout_effect_weak |
| DynamicShapeField | dynamic shape applied from public trace and changes controls; static_shape should change some traces but not all | static_shape action-sensitive modes=4/8; dynamic_step_delta_total=-124 | broadly_expected_for_first_pass |
| Quotient/equivalence | conservative grouping; no_quotient should affect only profiles where lawful quotient rows exist | no_quotient action-sensitive modes=2/8; quotient_delta_total=-6.143 | expected_conservative_but_needs_missed_false_quotient_audit |
| Recursion scheduler | recursion demand ablates and does not inflate weak procedural competition into collapse pressure | no_scheduler action-sensitive modes=2/8; demand_delta_total=-1.081 | partially_expected_first_pass |
| Readout consumption | CO structures should sometimes affect commitment; should not be completely swallowed by dominance mass | avg_support_stability_field_share=0.949; carrier_resolver_no_shape_trigger=98/104 | not_as_expected_for_strong_kernel; release_blocking_watchpoint |
| Maintenance behavior | if sequence/readout solved the previous issue, maintenance ablations should show at least some structurally explainable sensitivity | sensitive=0; insensitive=10 | not_as_expected_if_goal_was_behavioral_resolution; useful_failure_signal |
| Structural validation | no unresolved structural watchpoints for release; pass-with-watchpoints acceptable only for research state | status=PASS_WITH_WATCHPOINTS; cases_with_watchpoints=1 | research_ok_release_not_ok |
| Architecture acceptance | release requires accepted architecture; Pass 1 research may continue with watchpoints | status=ACCEPTANCE_WATCHPOINTS_REMAIN; summary={'adapter_public_effect_leakage': 'PASS_WITH_WATCHPOINTS', 'branch_identity_trace_quality': 'PASS_WITH_WATCHPOINTS', 'collapse_certificate_reason_quality': 'PASS_WITH_WATCHPOINTS', 'formula_grounding': 'PASS_WITH_WATCHPOINTS', 'relation_noise': 'PASS_WITH_WATCHPOINTS'} | release_not_ok |

## Ablation sensitivity

| Ablation | Action-sensitive modes | Total prefix action diffs | Metric-sensitive modes | Main interpretation |
|---|---:|---:|---:|---|
| minimal_recent_core | 4/8 | 32 | 4/8 | Recent mechanisms collectively matter in some modes. |
| no_quotient | 2/8 | 22 | 2/8 | Quotienting is conservative but behavior-visible in latent traces. |
| no_scheduler | 2/8 | 17 | 2/8 | Scheduler is behavior-visible in some traces, not globally decisive. |
| no_sequence | 1/8 | 5 | 1/8 | Sequence composition is mostly telemetry-visible; weak readout effect. |
| static_shape | 4/8 | 28 | 4/8 | DynamicShapeField is behavior-visible in some families. |

## Family/mode sensitivity

| Family/mode | Sensitive ablations | Total prefix action diffs | Interpretation |
|---|---:|---:|---|
| bandit/easy_public_bandit | 3/5 | 21 | Mechanisms behavior-visible, especially shape/scheduler/minimal-core. |
| latent_mechanism/easy_visible | 3/5 | 32 | Mechanisms clearly behavior-visible. |
| latent_mechanism/hidden_depth2 | 4/5 | 39 | Mechanisms clearly behavior-visible. |
| maintenance_replacement/bandit_like | 0/5 | 0 | Action-insensitive under all recent-mechanism ablations; major watchpoint. |
| maintenance_replacement/middle | 0/5 | 0 | Action-insensitive under all recent-mechanism ablations; major watchpoint. |
| maintenance_replacement/renewal_like | 0/5 | 0 | Action-insensitive under all recent-mechanism ablations; major watchpoint. |
| maze/static_visible_5x5 | 2/5 | 10 | Partly sensitive. |
| renewal/noisy_renewal | 1/5 | 2 | Weakly sensitive. |

## Red-team interpretation

1. The kernel is not merely dead telemetry: static shape, quotient, scheduler, and recent-core ablations change actions in some family/modes.
2. Sequence composition passes microcases and is present in real rows, but `no_sequence` changes actions in only 1/8 family/modes. That is weaker than expected if sequence composition is supposed to materially address the one-step/action-row problem.
3. Readout still appears too dominated by support/stability/field mass: avg support/stability/field share is about 0.949, and 98/104 carrier-with-resolver-alt steps had no shape-triggered resolver path.
4. Maintenance remains fully action-insensitive under the current ablation set. This is not proof of failure, but it is not behavior one should call solved.
5. Therefore, the next task should be a generic readout-consumption investigation, not a new ontology feature and not a maintenance-specific patch.

## Recommended next action

Freeze the mechanism set for now. Investigate why sequence/dynamic/quotient/scheduler telemetry is not sufficiently consumed by CommitmentSurface in the insensitive families. The fork is: legitimate non-decisiveness, weak readout integration, or collapse into support/stability scoring. Only after that fork is resolved should robot/sim or new mechanisms proceed.
