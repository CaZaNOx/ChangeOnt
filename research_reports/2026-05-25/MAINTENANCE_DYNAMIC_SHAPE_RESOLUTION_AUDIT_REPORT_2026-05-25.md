# Maintenance DynamicShapeField Resolution Audit — 2026-05-25

## Claim boundary

Audit-only maintenance DynamicShapeField resolution check. It does not change kernel behavior, does not assert an optimal maintenance action, does not use hidden state, DP/baseline values, or native action-name rules for decisions, and does not license maintenance-specific tuning. It classifies public trace contexts where DynamicShapeField narrows margins without changing action.

## Main verdict

DynamicShapeField is not inert in maintenance-like traces. It often moves dominance margins, but most narrowing/no-action cases do not cross the current generic carrier/resolver gate or remain dominated by a selected branch with a sizeable margin. This means the remaining issue is not 'DynamicShapeField does nothing'; it is whether the generic gate/readout is too conservative in phase-structured maintenance-like contexts.

This audit does not justify a maintenance-specific rule or coefficient tune.

## Counts

```json
{
  "borderline_needs_manual_trace_review": 10,
  "directional_context_steps": 49,
  "generic_gate_or_readout_underweighting_watchpoint": 8,
  "narrowed_no_action_steps": 32,
  "not_narrowing_no_action_case": 22,
  "plausible_stable_continuation_under_current_gate": 14,
  "total_classified_steps": 54
}
```

## By mode

| mode | total | not narrowing | plausible stable/current gate | below generic gate | gate/readout watchpoint | hard underweighting | borderline |
|---|---:|---:|---:|---:|---:|---:|---:|
| bandit_like | 18 | 4 | 14 | 0 | 0 | 0 | 0 |
| middle | 18 | 2 | 0 | 0 | 8 | 0 | 8 |
| renewal_like | 18 | 16 | 0 | 0 | 0 | 0 | 2 |

## Findings

### MDS1_NARROWING_CASES_ARE_NOT_AUTOMATIC_FAILURES — info

**Finding:** Many maintenance DynamicShapeField narrowing/no-action cases remain non-decisive because the selected branch or resolver alternative does not pass the current generic preblocking gate.

**Evidence:** plausible_or_below_gate=14, narrowed_no_action_steps=32

**Next action:** Do not treat every score narrowing without action change as readout failure; retain context-conditioned classification.

### MDS2_GATE_READOUT_WATCHPOINT_REMAINS — medium

**Finding:** Some cases still look like generic gate/readout adequacy watchpoints rather than clean stable continuation.

**Evidence:** generic_gate_or_readout_underweighting_watchpoint=8, likely_underweighted_resolver_sequence_near_margin=0

**Next action:** Use targeted generic microcases before any coefficient change; do not tune maintenance-specific behavior.

### MDS3_MAINTENANCE_ACTION_INSENSITIVITY_REINTERPRETED — medium

**Finding:** Maintenance action insensitivity is not explained by DynamicShapeField being inert. It is mostly a question of whether current generic gates are too conservative in maintenance-like phase contexts.

**Evidence:** DynamicShapeField narrows margins in several maintenance steps, but most do not cross current carrier/resolver gate thresholds or dominance margins.

**Next action:** If future diagnostics require change, audit the generic preblocking/readout gate under shape-conditioned phase contexts across families, not just maintenance.

## Representative samples

### `not_narrowing_no_action_case`

```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.086617,
  "local_shape_urgency": 0.331741,
  "margin": 0.306426,
  "margin_delta": 0.016889,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.473362,
  "selected": "RUN",
  "sequence_support": 0.190559,
  "shape_gauged_trigger": false,
  "t": 0
}
```
```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.082525,
  "local_shape_urgency": 0.254394,
  "margin": 0.52385,
  "margin_delta": 0.008598,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.534839,
  "selected": "RUN",
  "sequence_support": 0.262611,
  "shape_gauged_trigger": false,
  "t": 1
}
```
```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.082875,
  "local_shape_urgency": 0.26131,
  "margin": 0.518045,
  "margin_delta": 0.001392,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.598531,
  "selected": "RUN",
  "sequence_support": 0.288742,
  "shape_gauged_trigger": false,
  "t": 2
}
```
```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.0831,
  "local_shape_urgency": 0.265727,
  "margin": 0.514493,
  "margin_delta": -0.003106,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.625125,
  "selected": "RUN",
  "sequence_support": 0.300868,
  "shape_gauged_trigger": false,
  "t": 3
}
```
```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.649739,
  "local_shape_urgency": 0.405501,
  "margin": 0.163141,
  "margin_delta": 0.012951,
  "mode": "middle",
  "resolver_req_ratio": 0.969448,
  "selected": "RUN",
  "sequence_support": 0.138034,
  "shape_gauged_trigger": false,
  "t": 0
}
```

### `plausible_stable_continuation_under_current_gate`

```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.083245,
  "local_shape_urgency": 0.26855,
  "margin": 0.512334,
  "margin_delta": -0.005916,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.636862,
  "selected": "RUN",
  "sequence_support": 0.306578,
  "shape_gauged_trigger": false,
  "t": 4
}
```
```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.083338,
  "local_shape_urgency": 0.270356,
  "margin": 0.511062,
  "margin_delta": -0.007671,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.642423,
  "selected": "RUN",
  "sequence_support": 0.30867,
  "shape_gauged_trigger": false,
  "t": 5
}
```
```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.083397,
  "local_shape_urgency": 0.271509,
  "margin": 0.510337,
  "margin_delta": -0.008769,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.645265,
  "selected": "RUN",
  "sequence_support": 0.309445,
  "shape_gauged_trigger": false,
  "t": 6
}
```
```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.083435,
  "local_shape_urgency": 0.272245,
  "margin": 0.509981,
  "margin_delta": -0.009451,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.646817,
  "selected": "RUN",
  "sequence_support": 0.309736,
  "shape_gauged_trigger": false,
  "t": 7
}
```
```json
{
  "alt_resolver": "WAIT",
  "carrier_gate_ratio": 0.083459,
  "local_shape_urgency": 0.272713,
  "margin": 0.509887,
  "margin_delta": -0.009868,
  "mode": "bandit_like",
  "resolver_req_ratio": 0.64771,
  "selected": "RUN",
  "sequence_support": 0.309847,
  "shape_gauged_trigger": false,
  "t": 8
}
```

### `borderline_needs_manual_trace_review`

```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.640741,
  "local_shape_urgency": 0.384628,
  "margin": 0.287734,
  "margin_delta": -0.005069,
  "mode": "middle",
  "resolver_req_ratio": 0.978532,
  "selected": "RUN",
  "sequence_support": 0.272598,
  "shape_gauged_trigger": false,
  "t": 2
}
```
```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.642723,
  "local_shape_urgency": 0.389276,
  "margin": 0.283295,
  "margin_delta": -0.010533,
  "mode": "middle",
  "resolver_req_ratio": 0.976494,
  "selected": "RUN",
  "sequence_support": 0.30313,
  "shape_gauged_trigger": false,
  "t": 3
}
```
```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.643998,
  "local_shape_urgency": 0.39225,
  "margin": 0.280472,
  "margin_delta": -0.013991,
  "mode": "middle",
  "resolver_req_ratio": 0.975195,
  "selected": "RUN",
  "sequence_support": 0.321536,
  "shape_gauged_trigger": false,
  "t": 4
}
```
```json
{
  "alt_resolver": "REPLACE",
  "carrier_gate_ratio": 0.86532,
  "local_shape_urgency": 0.424435,
  "margin": 0.142765,
  "margin_delta": -0.027477,
  "mode": "middle",
  "resolver_req_ratio": 0.927075,
  "selected": "RUN",
  "sequence_support": 0.2966,
  "shape_gauged_trigger": false,
  "t": 13
}
```
```json
{
  "alt_resolver": "REPLACE",
  "carrier_gate_ratio": 0.865294,
  "local_shape_urgency": 0.42439,
  "margin": 0.160063,
  "margin_delta": -0.027452,
  "mode": "middle",
  "resolver_req_ratio": 0.927092,
  "selected": "RUN",
  "sequence_support": 0.301156,
  "shape_gauged_trigger": false,
  "t": 14
}
```

### `generic_gate_or_readout_underweighting_watchpoint`

```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.644816,
  "local_shape_urgency": 0.394154,
  "margin": 0.278718,
  "margin_delta": -0.016177,
  "mode": "middle",
  "resolver_req_ratio": 0.974365,
  "selected": "RUN",
  "sequence_support": 0.332628,
  "shape_gauged_trigger": false,
  "t": 5
}
```
```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.645342,
  "local_shape_urgency": 0.395374,
  "margin": 0.277673,
  "margin_delta": -0.017555,
  "mode": "middle",
  "resolver_req_ratio": 0.973834,
  "selected": "RUN",
  "sequence_support": 0.339311,
  "shape_gauged_trigger": false,
  "t": 6
}
```
```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.645679,
  "local_shape_urgency": 0.396155,
  "margin": 0.277144,
  "margin_delta": -0.018422,
  "mode": "middle",
  "resolver_req_ratio": 0.973495,
  "selected": "RUN",
  "sequence_support": 0.343337,
  "shape_gauged_trigger": false,
  "t": 7
}
```
```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.645895,
  "local_shape_urgency": 0.396655,
  "margin": 0.276935,
  "margin_delta": -0.018963,
  "mode": "middle",
  "resolver_req_ratio": 0.973277,
  "selected": "RUN",
  "sequence_support": 0.345761,
  "shape_gauged_trigger": false,
  "t": 8
}
```
```json
{
  "alt_resolver": "INSPECT",
  "carrier_gate_ratio": 0.646032,
  "local_shape_urgency": 0.396973,
  "margin": 0.276916,
  "margin_delta": -0.019296,
  "mode": "middle",
  "resolver_req_ratio": 0.973139,
  "selected": "RUN",
  "sequence_support": 0.34722,
  "shape_gauged_trigger": false,
  "t": 9
}
```

## Verdict

```json
{
  "all_narrowing_non_effects_are_failures": false,
  "dynamic_shape_inert_in_maintenance": false,
  "generic_gate_or_readout_watchpoints_found": 8,
  "hard_underweighting_cases_found": 0,
  "kernel_change_made": false,
  "maintenance_specific_tuning_justified": false,
  "next_recommended_step": "design generic gate/readout adequacy microcases if the team wants to test whether current thresholds are too conservative; otherwise proceed to broader first-pass evaluation with this watchpoint logged"
}
```

## Interpretation

The audit narrows the question: maintenance insensitivity is not caused by DynamicShapeField absence or pure readout invisibility. Dynamic shape often changes margins. The unresolved issue is whether the current generic carrier/resolver gate and support-stability dominance are calibrated correctly for phase-structured contexts. This should be tested with generic cross-family microcases before any runtime change.
