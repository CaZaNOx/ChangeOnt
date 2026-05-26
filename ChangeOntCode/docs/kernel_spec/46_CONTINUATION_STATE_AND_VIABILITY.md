# 46. Continuation State and Viability

Status: active working runtime bridge.

This file defines `ContinuationState` as the explicit implementation-side bridge from identity-through-change to candidate publication and commitment readout.

## Classification

`ContinuationState` is:

- a kernel-runtime support object;
- not an ontology primitive;
- not a deep element;
- not a six-question placement axis;
- not adapter logic;
- not a family policy.

Its job is to prevent the runtime from collapsing candidate evaluation into one-step action scoring.

## Ontological source

The relevant CO chain is:

```text
trace / residue
→ recurrence
→ remaining transformation burden
→ identity-through-change
→ collapse / commitment
```

A candidate should not be treated only as an immediate action. It should be treated as a possible continuation whose support, burden, and fracture can persist, accumulate, or decay across updates.

## Runtime definition

`ContinuationState` := bounded runtime memory of a candidate continuation's support, burden, fracture, uncertainty, and viability through recent change.

Canonical fields:

- `support_persistence`: whether support is carrying across updates;
- `burden_accumulation`: whether unresolved transformation burden is accumulating;
- `burden_trend`: recent positive burden growth;
- `fracture_trend`: recent positive fracture growth;
- `support_decay`: recent loss of support;
- `continuation_instability`: generic pressure that the continuation is losing coherence;
- `continuation_viability`: bounded estimate of whether the continuation remains supportable through change.

These are runtime measurements of continuation condition. They are not optimal values and not hidden policy labels.

## Allowed inputs

The tracker may consume only generic candidate-publication fields, for example:

- support magnitude;
- burden pressure;
- fracture / contradiction pressure;
- uncertainty.

It must not consume:

- family names;
- action names as policy branches;
- hidden/oracle state;
- optimal-action labels;
- threshold/control-limit decisions;
- planner scores.

## Layer relation

`ContinuationState` is a per-continuation memory carrier used inside candidate publication. It is not the whole kernel path. The current route is:

```text
public problem packet
→ shape_prior6 / direct controls
→ CandidateSurface + ContinuationState update
→ Continuation Identity / Burden Operations
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
→ action
```

So `ContinuationState` makes the candidate row more processive, but cross-branch interaction belongs to RelationSurface and RCF, and earned-collapse gating belongs to CollapseCertificate before CommitmentSurface.

## Why it is needed

Without this object, a candidate can remain strong because its local support is high even while its burden is rising. That recreates a classical action-score path:

```text
action has current support → choose action
```

The CO path should instead ask:

```text
candidate continuation has support
but is its support still viable through unfolding burden?
```

## Anti-smuggling invariant

If a proposed continuity/viability field cannot be expressed in terms of support persistence, burden accumulation, fracture trend, uncertainty, or direct-control modulation, it does not belong in `ContinuationState`.

## Current implementation locus

- `agents/co/runtime/surfaces/continuation_state.py`
- `agents/co/runtime/surfaces/candidate_surface.py`
- `agents/co/runtime/surfaces/fusion_support.py`
- `agents/co/runtime/surfaces/commitment_surface.py`
- `agents/co/tests/continuation_state_invariants.py`

## ContinuationState versus recursive continuation field

`ContinuationState` is per-continuation memory. It does not by itself define how continuations affect one another. `47_RECURSIVE_CONTINUATION_FIELD.md` supplies the interaction doctrine: branch debt, grey preservation, quotient/merge, cancellation, neighbor recursion-depth spread, and field-shaped collapse. Future runtime work should keep this distinction explicit.

### Recursive field invariant dependency

`ContinuationState` remains per-branch memory. It should provide support/burden/fracture/uncertainty trends to the field, but the cross-branch laws are governed by `48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md`: debt relief, proximity influence, quotient/merge, cancellation, grey preservation, and collapse-delay.


---

Implementation note: the minimal runtime contract for the first executable version is recorded in `49_RECURSIVE_CONTINUATION_FIELD_RUNTIME_CONTRACT.md`. That file is not a success claim; it is the v1 contract for abstract invariants and diagnostics.
