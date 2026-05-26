# Dominance / Readout-Swamping Audit v1 — 2026-05-22

Claim boundary: Generic dominance/readout-swamping audit only. It is not a benchmark, not tuning evidence, not maintenance-specific diagnosis, not SOTA comparison, and not CO proof.

## Summary

- full-current steps inspected: 144
- carrier-with-resolver-alt cases: 69
- gate failure counts: `{'other_or_unclassified': 40, 'applied': 1, 'carrier_pressure_below_preblocking_gate': 28}`
- avg support/stability/field share of positive dominance mass: 0.949
- avg dominance penalty/positive-mass ratio: 0.219
- microcase summary: `{'cases': 6, 'passed': 5, 'observed': 1, 'watchpoints': 0}`

## Interpretation

The audit does not license a maintenance-specific repair rule. After generic carrier-gate calibration, the borderline high-urgency microcase is protected, but many real-trace carrier selections remain action-inert because support/stability/field mass or other generic readout gates still dominate. This is a kernel/readout question, not a problem-family patch.

## Sample cases

| family/mode | t | selected | alt | mode | failure | carrier | alt resolver | support-share | penalty-ratio |
|---|---:|---|---|---|---|---:|---:|---:|---:|
| bandit / easy_public_bandit | 0 | 0 | 1 | reopen_or_sample | other_or_unclassified | 1.000 | 1.000 | 0.948 | 0.395 |
| bandit / easy_public_bandit | 1 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.965 | 0.173 |
| bandit / easy_public_bandit | 2 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.966 | 0.199 |
| bandit / easy_public_bandit | 3 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.966 | 0.212 |
| bandit / easy_public_bandit | 4 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.967 | 0.219 |
| bandit / easy_public_bandit | 5 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.967 | 0.223 |
| bandit / easy_public_bandit | 6 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.967 | 0.224 |
| bandit / easy_public_bandit | 7 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.967 | 0.225 |
| bandit / easy_public_bandit | 8 | 0 | 1 | dominance | other_or_unclassified | 1.000 | 1.000 | 0.968 | 0.225 |
| bandit / easy_public_bandit | 9 | 1 | 2 | reopen_or_sample | applied | 1.000 | 1.000 | 0.927 | 0.396 |
| bandit / easy_public_bandit | 10 | 2 | 1 | reopen_or_sample | other_or_unclassified | 1.000 | 0.800 | 0.932 | 0.330 |
| bandit / easy_public_bandit | 11 | 1 | 2 | stable_continuation | other_or_unclassified | 0.925 | 0.800 | 0.968 | 0.128 |
| bandit / easy_public_bandit | 12 | 2 | 1 | stable_continuation | other_or_unclassified | 0.925 | 0.667 | 0.968 | 0.129 |
| bandit / easy_public_bandit | 13 | 2 | 1 | dominance | other_or_unclassified | 0.917 | 0.667 | 0.971 | 0.070 |
| bandit / easy_public_bandit | 14 | 2 | 1 | dominance | other_or_unclassified | 0.946 | 0.667 | 0.972 | 0.059 |
| bandit / easy_public_bandit | 15 | 2 | 1 | dominance | other_or_unclassified | 1.000 | 0.667 | 0.947 | 0.054 |

## Recommendation

Do not treat the generic carrier-gate calibration as problem-family tuning. After calibration, preserve cross-family negative controls and continue auditing remaining readout-swamping cases as generic kernel issues.
