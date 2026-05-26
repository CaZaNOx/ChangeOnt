# Generic Carrier-Gate Calibration Report — 2026-05-22

Scope boundary: this is a first-pass generic kernel/readout calibration. It is not maintenance tuning, not a benchmark result, not CO proof, and not a novelty claim.

## Change made

`CommitmentSurface` changed one documented pre-blocking resolver timing coefficient:

```text
preblocking_carrier_shape_urgency_weight: 0.34 -> 0.37
```

This slightly increases the degree to which public shape urgency can lower the generic carrier-pressure gate before a resolver alternative is compared.

The change does not use family names, native action names, rewards, hidden state, DP/baseline values, shortest paths, or topology edits.

## Why this was allowed

The prior dominance/readout-swamping audit found a generic calibration site: high-urgency carrier/resolver microcases could fail before resolver comparison because the carrier-pressure gate remained too high. The fix is therefore attached to the generic local shape gauge, not to maintenance or any other family.

## Guardrails checked

`preblocking_resolver_cross_family_microcase_probe_v1` now reports:

```text
cases = 6
passed = 5
observed = 1
watchpoints = 0
```

The formerly borderline high-urgency carrier case now triggers the resolver. The negative controls remain protected:

```text
low urgency -> no resolver displacement
weak resolver -> no resolver displacement
large carrier advantage -> no resolver displacement
```

## Current-family diagnostic status

`current_kernel_diagnostic_map_v1` reran successfully:

```text
runs_attempted = 40
runs_succeeded = 40
runs_failed = 0
```

`dominance_readout_swamping_audit_v1` still finds real-trace readout-swamping cases:

```text
carrier_with_resolver_alt_cases_total = 69
gate_failure_counts = {'applied': 1, 'carrier_pressure_below_preblocking_gate': 28, 'other_or_unclassified': 40}
```

This means the calibration fixed the protected microcase watchpoint but did not eliminate broader readout-swamping behavior.

## Maintenance status

`maintenance_action_insensitivity_audit_v1` still reports:

```text
insensitive_comparison_count = 8
sensitive_comparison_count = 0
```

So this change did not solve maintenance action-prefix insensitivity. Do not add a maintenance-specific repair rule. The remaining issue should be treated as generic sequence-level continuation / readout-swamping work.

## Next work

Recommended next slice:

```text
sequence-level continuation composition audit
+ remaining generic readout-swamping trace audit
```

Robot/simulation expansion should still wait until these first-pass kernel watchpoints are better understood.
