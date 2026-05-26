# Context-Conditioned Expectation Audit — 2026-05-25

## Claim boundary

Context-conditioned expectation audit only. It uses public shape/gauge telemetry, public relation/burden/sequence/certificate signals, and named ablations from the diagnostic map. It is not a benchmark, not CO proof, not a tuning license, and not a kernel change.

This audit was added because aggregate ablation counts are too naive. A mechanism can be active and correctly non-decisive. The audit first asks what the public context expects, then checks whether observed action/gate/readout effects match that expectation.

## Input

- Source trace: `outputs/current_kernel_diagnostic_map_v1/steps.jsonl`
- Full-current steps inspected: `124`
- Kernel behavior changed by this audit: `false`

## Context buckets observed

- `carrier_plus_resolver`: 58
- `collapse_blocked_or_grey`: 24
- `dynamic_shape_relevant`: 124
- `quotient_active`: 42
- `sequence_present`: 74

## Mechanism expectation/effect table

| mechanism | expected none | expected weak | expected strong | strong action effect | strong gate/readout effect only | suspicious strong non-effect |
|---|---:|---:|---:|---:|---:|---:|
| dynamic_shape | 0 | 8 | 116 | 24 | 22 | 70 |
| sequence | 50 | 34 | 40 | 1 | 36 | 3 |
| quotient | 0 | 82 | 42 | 16 | 26 | 0 |
| recursion | 21 | 79 | 24 | 10 | 13 | 1 |

## Findings

- **CCE_DYNAMIC_SHAPE_STRONG_CONTEXT_UNDERCONSUMPTION** (medium): dynamic_shape has many strong-context cases without action or gate/readout effect. Evidence: strong=116, suspicious=70, action_effect=24, gate_effect_only=22, suspicious_rate=0.603
- **CCE_SEQUENCE_STRONG_CONTEXT_PARTIALLY_CONSUMED** (low): sequence strong-context cases show at least some action/gate consumption. Evidence: strong=40, suspicious=3, action_effect=1, gate_effect_only=36, suspicious_rate=0.075
- **CCE_QUOTIENT_STRONG_CONTEXT_PARTIALLY_CONSUMED** (low): quotient strong-context cases show at least some action/gate consumption. Evidence: strong=42, suspicious=0, action_effect=16, gate_effect_only=26, suspicious_rate=0.000
- **CCE_RECURSION_STRONG_CONTEXT_PARTIALLY_CONSUMED** (low): recursion strong-context cases show at least some action/gate consumption. Evidence: strong=24, suspicious=1, action_effect=10, gate_effect_only=13, suspicious_rate=0.042

## Interpretation

The prior global statement “sequence only changed actions in 1/8 modes” was too coarse. This audit conditions on public shape/gauge and local triggers such as carrier burden, resolver alternatives, sequence phase, quotient activity, and structural recursion pressure.

A `suspicious_strong_context_non_effect` does not prove CO failure. It means the trace satisfied generic CO conditions where the mechanism should plausibly affect commitment/gating, but the capped diagnostic showed neither an action difference under the corresponding ablation nor an explicit gate/readout effect. These cases should be manually inspected before changing formulas.

## Verdict

```json
{
  "aggregate_action_counts_were_insufficient": true,
  "context_conditioning_added": true,
  "kernel_change_made": false,
  "next_recommended_step": "inspect strong-context suspicious cases and decide whether readout consumption is a wiring/formula bug, legitimate non-effect, or architecture limitation",
  "strong_context_suspicion_remaining": true
}
```

## Next step

Inspect the suspicious strong-context samples, especially for sequence and dynamic-shape contexts. The next action should be a readout-consumption/wiring audit, not a new ontology concept and not a family-specific tuning patch.
