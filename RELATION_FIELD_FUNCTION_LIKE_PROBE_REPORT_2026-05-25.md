# Relation-field function-like collapse probe report — 2026-05-25
## Purpose
Test the bounded first-pass implementation of function-like collapse as relation-field concentration under shape/gauge. This is not a full probabilistic relation algebra and not an action-selection mechanism.
## Summary
- cases: 4
- cases with at least one function-like row: 2
- cases with ambiguous relation-field telemetry: 4

## Case results
### highly_concentrated_function_like
- dominant: concentration=0.999, ambiguity=0.001, threshold=0.708, function_like=True
- tiny: concentration=0.001, ambiguity=0.999, threshold=0.708, function_like=False
- shape evidence: ambiguity=0.175, concentration=0.5, function_like_ratio=0.5

### flat_ambiguous_relation
- a: concentration=0.500, ambiguity=0.500, threshold=0.708, function_like=False
- b: concentration=0.500, ambiguity=0.500, threshold=0.708, function_like=False
- shape evidence: ambiguity=0.5, concentration=0.5, function_like_ratio=0.0

### shape_coarse_allows_borderline_collapse
- dominant: concentration=0.780, ambiguity=0.220, threshold=0.554, function_like=True
- minor: concentration=0.220, ambiguity=0.780, threshold=0.554, function_like=False
- shape evidence: ambiguity=0.21999999999999997, concentration=0.5, function_like_ratio=0.5

### shape_urgent_keeps_borderline_open
- dominant: concentration=0.780, ambiguity=0.220, threshold=0.832, function_like=False
- minor: concentration=0.220, ambiguity=0.780, threshold=0.832, function_like=False
- shape evidence: ambiguity=0.21999999999999997, concentration=0.5, function_like_ratio=0.0

## Interpretation
Highly concentrated public relation mass becomes function-like under the current gauge. Flat relations remain ambiguous. Coarse/collapse-permissive shape can treat a borderline relation as function-like, while urgent/fine shape keeps the same concentration open. DynamicShapeField consumes relation-field ambiguity/concentration as bounded public shape evidence.

## Guardrails
The implementation does not use family names, native action-name policies, hidden state, reward hindsight, DP/baseline values, or shortest paths. It emits telemetry and shape evidence only.
