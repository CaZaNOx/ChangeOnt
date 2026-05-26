# 106 — Relation-field concentration and function-like collapse contract

Status: first-pass structural contract and minimal implementation.

## Purpose

CO should not treat functions as primitive point-to-point assignments in the runtime interpretation. A function-like mapping is an earned collapse of a relation-field under a shape/gauge.

This contract adds a bounded runtime requirement: RelationSurface may summarize public relation-field concentration and ambiguity, and DynamicShapeField may consume those summaries as shape evidence. The mechanism must not become a full probabilistic relation algebra or a hidden solver.

## Allowed inputs

Only already-validated public effect facts may contribute:

- public burden/effect operation;
- burden type or relation scope;
- magnitude/confidence already accepted as public;
- generic controls/effective shape gauge.

## Forbidden inputs

- family names;
- native action-name policies;
- hidden state;
- reward hindsight alone;
- DP/baseline values;
- shortest paths;
- outcome labels such as “best action.”

## Required telemetry

Rows may expose:

- `relation_field_domain`;
- `relation_field_concentration`;
- `relation_field_ambiguity`;
- `relation_field_domain_ambiguity`;
- `relation_field_function_like_threshold`;
- `relation_field_function_like`;
- `relation_field_dominant_operation_class`;
- `relation_field_domain_row_count`.

Telemetry may expose:

- `relation_field_domains`;
- `relation_field_profiles`;
- `relation_field_avg_concentration`;
- `relation_field_avg_domain_ambiguity`;
- `relation_field_function_like_count`;
- `relation_field_ambiguous_count`;
- `relation_field_function_like_threshold`.

## Semantics

A relation-field is function-like when the public relation mass for a generic domain is concentrated enough under current shape/gauge. The threshold is shape-sensitive: coarsening and collapse permission lower the threshold; urgency, path sensitivity, and contradiction sensitivity raise it.

This is not action selection. It is collapse-readiness evidence.

## DynamicShapeField use

DynamicShapeField may treat relation ambiguity as public shape evidence. Ambiguity can increase burden persistence/hiddenness pressure and lower gauge confidence. Function-like concentration can support gauge confidence. These updates remain bounded and cannot choose an action directly.

## Interpretation boundary

This implementation is not a claim that CO has a final probability theory. It is a first-pass guard against premature point/function collapse: preserve enough relation-field concentration information to test whether a function-like collapse is earned.
