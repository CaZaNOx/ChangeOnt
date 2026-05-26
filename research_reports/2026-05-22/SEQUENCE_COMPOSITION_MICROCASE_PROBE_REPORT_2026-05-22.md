# Sequence Composition Microcase Probe v1 — 2026-05-22

## Claim boundary

Sequence-composition microcase probe only. It is not a benchmark, not CO proof, and not a license for family-specific or native-action sequence templates.

## Summary

Cases: 5; passed: 5; failed: 0.

## Cases

| id | passed | expected active | observed active | phases | transition | support |
|---|---:|---:|---:|---|---|---:|
| SC1_EXPOSE_TO_RELIEVE | 1 | 1 | 1 | expose → stabilize | expose_to_stabilize | 0.265 |
| SC2_RELIEVE_TO_STABILIZE | 1 | 1 | 1 | relieve → stabilize | relieve_to_stabilize | 0.239 |
| SC3_DISABLED_ABLATION | 1 | 0 | 0 | disabled → disabled |  | 0.000 |
| SC4_NONPUBLIC_REJECTED | 1 | 0 | 0 | expose → stabilize |  | 0.000 |
| SC5_INCOMPATIBLE_DOMAIN_REJECTED | 1 | 0 | 0 | expose → stabilize |  | 0.000 |

## Interpretation

The sequence composer recognizes generic public phase progression across selected feedback and current candidate rows. It does not inspect family names, native action meanings, hidden state, reward hindsight, DP values, or baseline values.
