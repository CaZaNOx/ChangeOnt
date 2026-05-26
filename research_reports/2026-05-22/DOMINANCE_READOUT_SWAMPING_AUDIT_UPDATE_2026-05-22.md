# Dominance / Readout-Swamping Audit Update — 2026-05-22

## Claim boundary

This update is a first-pass kernel audit. It is not a benchmark, not tuning evidence, not maintenance-specific policy repair, not SOTA comparison, and not proof that CO works.

## What was added

- `ChangeOntCode/experiments/studies/dominance_readout_swamping_audit_v1.py`
- `ChangeOntCode/experiments/studies/preblocking_resolver_cross_family_microcase_probe_v1.py`
- `ChangeOntCode/agents/co/tests/dominance_readout_swamping_audit_invariants.py`
- `ChangeOntCode/agents/co/tests/preblocking_resolver_cross_family_microcase_invariants.py`
- row-level readout component telemetry in `CommitmentSurface`:
  - dominance positive/negative mass
  - support/stability/field/relation components
  - burden/trend/blocker penalties
  - sampling component decomposition
  - continuation component decomposition
- `local_shape_gauge` export in the current-kernel diagnostic map.

## Main finding

Generic carrier/readout swamping is real but not uniform. In the capped full-current diagnostic map, many steps selected a carrier branch while an explicit resolver alternative existed. Most failures were not due to missing resolver telemetry; they occurred because the generic pre-blocking resolver timing path failed before resolver comparison or because support/stability/field mass outweighed burden/blocker penalties.

The diagnostic report found:

- `carrier_with_resolver_alt_cases_total = 69`
- `gate_failure_counts = {'applied': 1, 'carrier_pressure_below_preblocking_gate': 28, 'other_or_unclassified': 40}`
- `avg_support_stability_field_share ≈ 0.949`
- `avg_dominance_penalty_ratio ≈ 0.219`

This supports the earlier suspicion: some action-inert behavior is a generic readout/gate calibration issue, not merely absent mechanism telemetry.

## Microcase result

The cross-family microcase probe used anonymous `CARRY_CONTINUATION` / `RESOLVE_CONTINUATION` rows under public shape profiles. It found:

- high urgency + high carrier pressure + adequate resolver: trigger passes;
- low urgency: protected from premature resolver displacement;
- weak resolver: protected;
- large carrier advantage: protected;
- high urgency + borderline carrier pressure: watchpoint.

This identifies a generic carrier-gate calibration site. It does not license a maintenance-specific repair rule or family-specific threshold.

## Open decision

The next lawful implementation step, if chosen, is a small generic carrier-gate calibration guarded by the negative microcases. The alternative is to keep the kernel unchanged and gather broader traces first. Either way, no problem-family patch should be introduced.
