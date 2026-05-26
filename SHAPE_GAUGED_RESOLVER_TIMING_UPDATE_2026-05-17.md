# Shape-Gauged Resolver Timing Update — 2026-05-17

## Why this update exists

The mid-regime maintenance failure analysis exposed a generic doctrine issue: a branch could carry rising carrier-only burden while remaining below formal certificate blocking, so resolver preference only activated late or indirectly.  The user correctly objected that a fix must not be maintenance-specific tuning and must include current problem shape.

## Derived law

```text
A resolver branch may bend commitment before formal blockage when:
1. the current branch carries unresolved carrier-only burden;
2. another branch has explicit public resolver support for that burden class;
3. the local problem shape/direct-control gauge makes delay, consequence, revision, hiddenness, or nonlocality relevant;
4. the resolver is adequate relative to the carried burden;
5. the local support/score gap is not overwhelming;
6. transform/transfer alone are not treated as resolution.
```

## Shape update discipline

The base six-question problem shape remains the public prior.  The runtime now computes a local shape gauge for the commitment step by combining:

```text
six-question/direct-control urgency
+ current carrier-only pressure
+ public certificate/blocker pressure
```

This does not edit environment topology, does not modify the adapter's problem facts, and does not encode native policy.  It only changes the gauge under which current branch relations are interpreted.

## Files changed

- `ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py`
- `ChangeOntCode/experiments/studies/shape_gauged_resolver_timing_probe_v1.py`
- `ChangeOntCode/agents/co/tests/shape_gauged_resolver_timing_probe_invariants.py`
- `ChangeOntCode/experiments/studies/mid_regime_repair_timing_probe_v1.py`
- `ChangeOntCode/agents/co/tests/mid_regime_repair_timing_probe_invariants.py`
- `FORMULA_COEFFICIENT_LEDGER_2026-05-16.md`
- `OPEN_POINTS_AND_FUTURE_WORK.md`

## Probe status

```text
shape_gauged_resolver_timing_probe_v1:
  cases = 12
  low_urgency_resolver_switches = 0
  high_urgency_resolver_switches = 4
  transform_transfer_switches = 0

mid_regime_repair_timing_probe_v1:
  high_risk_run_case_count = 0
  synthetic matrix still includes both RUN and REPAIR choices
```

## Claim boundary

This is a structural/formula update, not reward evidence.  It is not proof that CO works.  It does not justify tuning to maintenance baselines.  The new formula constants are provisional and must remain frozen for evidence-bearing empirical runs.
