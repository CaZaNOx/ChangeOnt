# 89 — Relation Path Trace Validation

Status: diagnostic contract / post-RelationSurface wiring check.

This file records the next validation layer after public-effect relation coverage.
It is not a reward benchmark and must not be cited as performance evidence.

## Purpose

The intended runtime path is:

```text
adapter public_effects
→ kernel-side RelationSurface
→ explicit branch relations
→ RecursiveContinuationField field deformation
→ CommitmentSurface / action expression, if collapse is earned
```

Coverage alone is insufficient.  A trace must show whether derived relation
topology changes field outputs, whether those changes are sparse/typed enough to
be meaningful, and whether commitment/readout actually consumes the resulting
field structure.

## Primary diagnostic comparison

For the same adapter observation, compare:

```text
public_effects present
vs
public_effects stripped
```

Candidate scalar hints are otherwise held fixed by the same adapter observation.
The relation-on case should derive branch relations and change RCF field outputs
for traceable relation reasons.

Required inspected fields:

```text
relations_by_type
field_relation_count
field_debt
field_viability
field_grey_pressure
field_recursion_budget
field_collapse_readiness
quotient_share_count
canonical_commitment_mode
action
```

## Interpretation boundaries

A positive field delta means:

```text
RelationSurface-derived topology reaches RCF field computation.
```

It does not by itself mean:

```text
CO performs better.
Collapse is earned.
CommitmentSurface is relation-aware enough.
The relation schema is complete.
```

If action/commitment does not change while field outputs do, the correct reading
is:

```text
The relation path affects the field, but downstream collapse/readout remains to
be validated.
```

## Noise risks

Relation counts must be inspected by type.  Generic single-slot rivalry can be
legitimate public grammar, but it must not swamp burden-specific relations such
as relief, cancellation, shared-evidence, buffering, or equivalence.

Useful telemetry:

```text
relations_total
relations_by_type
non_rival_relations
relations_per_candidate
field_delta_l1
field_delta_max
commitment_action_changed
commitment_mode_changed
```

## Current diagnostic artifact

```text
agents/co/tests/relation_path_trace_diagnostics.py
experiments/studies/relation_path_trace_v1.py
outputs/relation_path_trace_v1.json
```

The output should be read as forensic trace evidence only.
