# Relation-field / function-like collapse update — 2026-05-25

## What changed

The repo now records a bounded first-pass version of the conceptual correction that functions/states/points are earned collapses of relation-fields under shape/gauge.

Added theory/doc anchors:

- `TheoryOfChange_main/01_Statements/02_Outer_Formation/022B_S-DR-relation-field-function-like-collapse-from-shape.md`
- `TheoryOfChange_main/02_Concepts/C-relation-field-function-like-collapse.md`
- `ChangeOntCode/docs/kernel_spec/106_RELATION_FIELD_FUNCTION_LIKE_COLLAPSE.md`

Added runtime carrier:

- `ChangeOntCode/agents/co/runtime/surfaces/relation_field_concentration.py`

RelationSurface now emits bounded relation-field telemetry:

- `relation_field_domain`
- `relation_field_concentration`
- `relation_field_ambiguity`
- `relation_field_function_like_threshold`
- `relation_field_function_like`
- `relation_field_dominant_operation_class`
- `relation_field_domain_row_count`

DynamicShapeField now consumes relation ambiguity/concentration as public shape evidence.

## What this does not do

This does not implement a full probabilistic relation algebra. It does not choose actions, use native action names, use hidden state, use reward hindsight, use DP/baseline values, or tune to any problem family.

## Conceptual meaning

A many-valued relation can be function-like when the public relation mass is sufficiently concentrated under the current gauge. A flat or ambiguous relation remains grey/open. Shape modulates the threshold: coarsening and collapse permission make function-like collapse easier; urgency/path/contradiction sensitivity make it harder.

## Why this is bounded

The implementation stores summary telemetry, not full distributions. It is meant to prevent premature point/function collapse and support audits of relation concentration, not to expand the kernel into a general probabilistic programming engine.
