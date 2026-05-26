# Pre-blocking Resolver Cross-Family Microcase Probe v1 — 2026-05-22

Claim boundary: Cross-family pre-blocking resolver microcase audit only. It is not a benchmark, not maintenance tuning, not SOTA comparison, and not CO proof.

## Summary

- cases: 6
- passed: 5
- observed-only: 1
- watchpoints: 0

## Case table

| case | profile | expected | status | selected | applied | gate | pressure | resolver_required |
|---|---|---:|---:|---|---:|---:|---:|---:|
| PB1_HIGH_URGENCY_HIGH_CARRIER_TRIGGERS | high_hidden_consequence | trigger | passed | RESOLVE_CONTINUATION | True | 0.452 | 0.500 | 0.277 |
| PB2_HIGH_URGENCY_BORDERLINE_CARRIER_AUDIT | high_hidden_consequence | trigger | passed | RESOLVE_CONTINUATION | True | 0.456 | 0.460 | 0.269 |
| PB3_MEDIUM_MIXED_MODERATE_CARRIER_OBSERVE | medium_mixed | observe | observed | CARRY_CONTINUATION | False | 0.521 | 0.360 | 0.233 |
| PB4_LOW_URGENCY_NO_TRIGGER | low_urgency_local | no_trigger | passed | CARRY_CONTINUATION | False | 0.562 | 0.500 | 0.247 |
| PB5_WEAK_RESOLVER_NO_TRIGGER | high_hidden_consequence | no_trigger | passed | CARRY_CONTINUATION | False | 0.450 | 0.520 | 0.281 |
| PB6_LARGE_CARRIER_ADVANTAGE_NO_TRIGGER | high_hidden_consequence | no_trigger | passed | CARRY_CONTINUATION | False | 0.452 | 0.500 | 0.277 |

## Interpretation

The probe uses anonymous `CARRY_CONTINUATION` / `RESOLVE_CONTINUATION` rows and public shape profiles only. It does not inspect family names, native action semantics, rewards, hidden state, baselines, or topology.

A watchpoint here is not a license to tune maintenance or any other problem. After the generic carrier-gate calibration, the borderline high-urgency positive case should pass while the low-urgency, weak-resolver, and large-carrier-advantage negative controls remain protected.
