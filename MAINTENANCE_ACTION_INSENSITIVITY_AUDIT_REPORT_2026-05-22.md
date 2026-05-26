# Maintenance Action-Insensitivity Audit v1 — 2026-05-22

## Claim boundary

Maintenance action-insensitivity audit only. It diagnoses capped diagnostic traces. It is not a maintenance benchmark, not a tuning justification, not SOTA comparison, and not CO proof.

## Main verdict

The maintenance action-insensitivity watchpoint is real, but this audit does not justify a maintenance-specific rule. The current evidence points to generic readout dominance/stable-continuation swamping and incomplete sequence/readout consumption, not missing telemetry or a hidden solver issue.

## Findings

### MAI1_ABLATION_ACTION_INSENSITIVITY_CONFIRMED — medium

**Finding:** Maintenance middle and renewal_like capped diagnostics remain action-prefix insensitive to recent-mechanism ablations.

**Evidence:** insensitive_comparison_count=10, sensitive_comparison_count=0 for target maintenance modes.

**Next action:** Treat this as a kernel/readout diagnostic, not a performance failure or tuning license.

### MAI2_READOUT_DOMINANCE_EXPLAINS_MUCH_OF_THE_INERTIA — medium

**Finding:** Full-current maintenance traces often keep the same selected action because the selected branch remains ahead in dominance/stability assessment, even when dynamic shape/scheduler/quotient telemetry moves.

**Evidence:** See mode_summary avg_selected_dominance_gap and examples; this suggests readout dominance/stable-continuation swamping rather than missing telemetry alone.

**Next action:** Audit whether sequence evidence is being consumed by readout before changing coefficients.

### MAI3_PREBLOCKING_RESOLVER_TIMING_NOT_SOLVED_GENERALLY — medium

**Finding:** Some RUN selections still coexist with carrier-only pressure and resolver alternatives without necessarily triggering shape-gauged resolver timing. This is a structural watchpoint, not a maintenance-specific repair rule request.

**Evidence:** selected_run_with_carrier_and_resolver_alt and selected_run_shape_gauged_false counts in mode_summary identify candidate cases.

**Next action:** Use generic sequence/readout-swamping diagnostics before modifying readout formula.

## Mode summary

| mode | steps | actions | modes | shape-gauged steps | avg dominance gap | near-margin steps | RUN carrier+resolver alt | RUN carrier+resolver alt without shape-gauge |
|---|---:|---|---|---:|---:|---:|---:|---:|
| middle | 18 | `{"RUN": 18}` | `{"dominance": 18}` | 0 | 0.242 | 0 | 18 | 18 |
| renewal_like | 18 | `{"INSPECT": 13, "RUN": 5}` | `{"reopen_or_sample": 1, "stable_continuation": 17}` | 5 | 0.014 | 14 | 5 | 5 |

## Interpretation

If a selected branch has a large dominance/stability gap, telemetry-only ablations are expected. If the gap is small and resolver alternatives or sequence evidence are present but timing does not reopen, that indicates a generic readout-swamping/sequence-consumption issue. The remedy must be generic and cross-family, not a maintenance-specific repair-at-health rule.
