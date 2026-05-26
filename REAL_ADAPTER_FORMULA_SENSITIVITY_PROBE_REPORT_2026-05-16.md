# Real-Adapter Formula Sensitivity Probe — 2026-05-16

## Scope

This report records a coefficient/formula sensitivity probe for the current real-adapter structural sweep. It is not a reward benchmark, not tuning, and not evidence that CO performs well. It asks whether the behavior-affecting coefficients introduced by certificate-aware stable continuation and resolver-aware reopen/sample selection are inert, sensitive, or dangerously brittle.

Study module:

```text
ChangeOntCode/experiments/studies/real_adapter_formula_sensitivity_probe_v1.py
```

Output:

```text
ChangeOntCode/outputs/real_adapter_formula_sensitivity_probe_v1.json
```

Invariant:

```text
ChangeOntCode/agents/co/tests/real_adapter_formula_sensitivity_probe_invariants.py
```

## Cases

The probe reuses the real-adapter public-observation sweep:

```json
{
  "cases": 311,
  "sources": {
    "standard_trace_sample": 5,
    "maintenance_public_observation_sweep": 216,
    "latent_public_observation_sweep": 90
  }
}
```

## Profiles tested

```text
baseline
strict_comparability_narrow_margins
permissive_comparability_wide_margins
low_resolver_threshold
high_resolver_threshold
zero_comparability_margins
resolver_threshold_nearly_disabled
flat_blocker_terms
```

These profiles are diagnostic perturbations only. They must not be treated as candidate tuned settings.

## Baseline behavior

```json
{
  "modes": {
    "dominance": 29,
    "reopen_or_sample": 111,
    "stable_continuation": 171
  },
  "certificate_aware_reopen_cases": 66,
  "certificate_aware_stable_cases": 0,
  "top_actions": {
    "INSPECT": 91,
    "REPAIR": 74,
    "RUN": 52,
    "INTERACT": 36,
    "UP": 24,
    "DOWN": 18,
    "RIGHT": 14,
    "0": 2
  }
}
```

## Sensitivity summary

| Profile | Action changes vs baseline | Mode changes | Reason changes | Main interpretation |
|---|---:|---:|---:|---|
| strict comparability / narrow margins | 0 | 0 | 0 | Baseline affected cases are not close to the lower margin boundary in this sweep. |
| permissive comparability / wide margins | 0 | 0 | 0 | Baseline already catches all currently available comparable alternatives in this sweep. |
| low resolver threshold | 0 | 0 | 0 | Real resolver supports in this sweep are already above the default threshold. |
| high resolver threshold | 0 | 0 | 0 | Raising threshold moderately does not matter; resolver supports are strong. |
| zero comparability margins | 5 | 0 | 5 | Comparable-alternative margins are behavior-causal but only in a small subset of real cases. |
| resolver threshold nearly disabled | 66 | 0 | 62 | Resolver recognition is strongly behavior-causal. If resolver support is not recognized, many choices revert toward carrier/high-pressure branches. |
| flat blocker terms | 1 | 0 | 1 | Blocker-pressure widening matters in at least one edge case, but is not broadly decisive in this sweep. |

## Interpretation

The current certificate-aware readout is not purely decorative. Resolver recognition is strongly causal: disabling resolver recognition changes 66 of 311 actions and removes 62 certificate-aware reopen/sample interventions.

The exact comparability margins are less fragile than expected in this sweep. Narrowing or widening them within moderate ranges changes no actions. However, forcing margins to zero changes 5 actions, so the comparable-alternative gate is active in a small but real subset.

The blocker-pressure widening terms are weakly active in this sweep: removing them changes one action. This does not prove the terms are unnecessary. It means they should be treated as provisional and should be tested on targeted blocker-pressure microcases before paper-level use.

## Formula-ledger consequences

Highest-priority ledger items after this probe:

1. `resolver_support_threshold` — high causal importance. Needs grounding first.
2. `sampling_gate_margin` / `sampling_support_advantage_limit` — active but less fragile in the observed sweep. Needs conceptual grounding and edge-case tests.
3. `continuation_gate_margin` / `support_advantage_limit` — active in microcases, inert in this real sweep because stable-continuation alternatives did not trigger. Needs continued microcase + future real-trace validation.
4. blocker-pressure margin weights — low real-sweep sensitivity but conceptually important. Needs targeted blocker-pressure probes.

## Claim boundary

Allowed claim:

```text
The current real-adapter sweep shows that resolver recognition and certificate-aware reopen/sample rules are behavior-causal structural mechanisms, not merely logged explanations.
```

Forbidden claim:

```text
The current constants are final, optimal, empirically validated, or evidence that CO outperforms baselines.
```

## Next step

Build the formula ledger entries for the high-causal coefficients, beginning with `resolver_support_threshold`, then add targeted sensitivity microcases for blocker-pressure margins and continuation-gate margins.
