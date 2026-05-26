# Resolver Threshold Microcase Probe Report — 2026-05-16

Status: structural formula-grounding diagnostic; not reward evidence.

## Why this probe exists

`resolver_formula_grounding_audit_v1` showed that resolver recognition is behavior-causal.  That made the flat resolver floor (`resolver_support >= 0.08`) too important to leave untested.  The risk was that the runtime could treat a tiny public resolver fact as adequate to a much larger unresolved carrier burden.

## What changed

`CommitmentSurface` now distinguishes:

```text
resolver recognition floor
resolver adequacy to the blocked branch's carried burden/blocker pressure
```

A resolver must now satisfy an effective requirement:

```text
required_resolver_support = max(
    base resolver floor,
    scaled adequacy from carrier_only_pressure and blocker pressure
)
```

This prevents a weak resolver at the old floor from displacing a high-burden carrier-only branch.

## Probe result

`resolver_threshold_microcase_probe_v1` swept 65 carrier/resolver magnitude cases plus operation-class checks.

Summary:

```json
{
  "watchpoint_count": 0,
  "first_switch_by_carrier": {
    "0.25": null,
    "0.45": 0.20,
    "0.65": 0.35,
    "0.85": 0.35,
    "1.00": 0.35
  }
}
```

Key checks:

```text
0.079 resolver support does not switch high-carrier case.
0.08 resolver support does not switch high-carrier case.
0.35 resolver support switches high-carrier case.
reduce / expose / cancel / buffer can switch when adequate.
transform / transfer do not count as resolvers by themselves.
```

## Real-adapter effect

The stricter adequacy law did not change the 311-case real-adapter sweep relative to the previous resolver-grounding state, because the real resolver alternatives in that sweep are already materially stronger than the scaled requirement.  The rule therefore fixes a controlled formula error without currently altering the sampled real-adapter behavior.

## Boundary

This is a structural readout-law correction, not empirical evidence that CO performs well.  The new adequacy constants remain provisional global proxies and require further ledger grounding before paper-level algorithm claims.
