---
id: concept.relation-field-function-like-collapse
title: Relation-field and function-like collapse
status: draft
tags: [concept/relation-field, concept/shape, concept/collapse]
---

# Relation-field and function-like collapse

A **relation-field** is a shape-conditioned field of reach/support/burden/ambiguity between retained regions. It is prior to a classical function in the CO runtime interpretation.

A **function-like collapse** occurs when a many-valued or noisy relation-field is sufficiently concentrated or aggregate-stable under the current shape/gauge that it can be treated as a single mapping without losing continuation-relevant structure.

## Key distinctions

- Exact function: formal ideal or earned strict collapse.
- Function-like relation: relation distribution is concentrated enough under a gauge.
- Open relation: several outcomes remain live.
- Ambiguous relation: no target is concentrated enough for collapse.
- Aggregate-stable relation: noisy individual events still preserve a stable global structure.

## Shape relation

Shape is not identical to a probability distribution. A distribution is one expression of shape through a relation under a gauge. Shape also controls coarseness, admissibility, hiddenness, projection horizon, burden persistence, collapse threshold, and sequence sensitivity.

## Runtime implication

The kernel should preserve bounded telemetry for relation concentration and ambiguity before allowing function-like collapse. This does not require a full probability distribution over all targets. The first-pass implementation records lightweight concentration/ambiguity fields in RelationSurface and lets DynamicShapeField consume them as public shape evidence.

