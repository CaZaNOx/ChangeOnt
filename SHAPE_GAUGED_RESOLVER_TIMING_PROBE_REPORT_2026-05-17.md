# Shape-Gauged Resolver Timing Probe — 2026-05-17

## Scope

This probe tests the generic pre-blocking resolver-timing law.  It is not a
maintenance repair heuristic and it is not reward evidence.

The same branch relation is evaluated under two public gauges:

```text
low urgency: high local/collapse authority, low revision/nonlocal/path pressure
high urgency: high revision/nonlocal/path pressure, low local/collapse authority
```

A valid resolver may bend commitment before formal certificate blocking only
under the shape gauge where carried burden is urgent enough.  Transform/transfer
alone must not count as resolution.

## Summary

```json
{
  "cases": 12,
  "high_urgency_resolver_switches": 4,
  "invariants": {
    "high_urgency_allows_resolver_timing": true,
    "low_urgency_does_not_force_resolver": true,
    "transform_transfer_do_not_count_as_resolvers": true
  },
  "low_urgency_resolver_switches": 0,
  "nonresolver_ops": [
    "transform",
    "transfer"
  ],
  "nonresolver_transform_transfer_switches": 0,
  "resolver_ops": [
    "reduce",
    "reveal",
    "reset",
    "buffer"
  ]
}
```

## Interpretation

The probe confirms the intended doctrine boundary:

```text
branch relation alone is insufficient;
problem shape supplies the gauge that says when the relation should matter now.
```

The update is local and runtime-gauge based.  It does not edit environment
topology, does not infer native policy, and does not inspect action names.
