# Data Contracts

## Purpose

This page defines the canonical contracts between layers of the kernel and between the kernel and task environments.

It is binding for the current codebase.

---

## Observation Envelope

All adapters/translators must provide an observation dict with these required keys:

- `family: str`
- `t: int`

Optional keys may include:

- `episode: int`
- `action_space: list`
- `feedback: dict`
- `history: list`
- `trace: list`
- `residuals: dict`
- `probes: dict`
- task-specific geometry/statistics needed by translators

Adapters must not inject hidden oracle state.

---

## Mask Semantics

`translator_mask` is a **blocklist**.

If a translator returns a mask:
- any action in `translator_mask` is considered forbidden
- ActionHead must respect the mask in final action selection
- if all actions are blocked, this must be explicitly flagged by `translator_mask_blocks_all = 1`

Translators must not guess validity from hidden information.

If validity cannot be determined from runner-exposed observation, return an empty mask.

---

## Votes and Signals

### Votes
Elements publish action-affecting votes to the bus.

Votes are:
- family-scoped
- drained once per decision step
- transport objects, not final policy decisions

### Scalar Signals
Elements publish scalar signals to the bus.

Signals are:
- canonical inter-element communication and telemetry values
- snapshotted by ActionHead into `signals`

Canonical required keys currently include:
- `EC_Identity.same`
- `EC_Identity.last_d`
- `EB_GHVC.pressure`
- `EB_GHVC.mdl_gain`
- `EB_GHVC.birth_suggest`

---

## Layer Contracts

### Primitives
Primitives expose reusable semantic quantities/operations.
They must:
- be task-agnostic
- be reusable by many elements
- not directly decide final actions

### Semantic Combinators
Semantic combinators expose reusable laws of composition between primitive outputs.
They must:
- be explicit
- be reusable
- not be hidden inside element internals

### Elements
Elements consume primitives via semantic combinators.
They must:
- declare their primitive dependencies
- declare their combinator dependencies
- emit votes/signals
- not directly call other elements

### Header
Header consumes canonical signals and internal state.
It must:
- update only on update pass
- not depend on hidden task specifics
- not silently redefine primitive meaning

### Meta Header
Meta header consumes external priors and explicit task-family assumptions.
It must:
- remain separate from internal header logic
- be explicitly logged

### Translators
Translators convert task-specific observations into canonical forms.
They must:
- not contain ontology logic that belongs in primitives/elements
- not smuggle hidden state

### ActionHead
ActionHead is the final action surface.
It must:
- respect masks
- snapshot signals
- not become a hidden ontology layer

---

## Telemetry Schema

`metrics.jsonl` is JSONL.

CO telemetry records use:
- `metric = "co_debug"`

Canonical top-level fields may include:
- `action`
- `co_policy`
- `co_weight`
- `co_bus_votes`
- `signals`
- `birth_count`
- `prototype_count`
- `class_count`
- `cap_hits`
- `translator_mask`
- `mask_mode`
- `translator_mask_blocks_all`
- `header_update_count`
- `header_update_source`

---

## Current Binding Rule

The current codebase may be incomplete, but any new code must preserve the layer boundaries defined here.

If implementation and this contract disagree:
- either update code to match contract
- or record the disagreement explicitly in `09_ACCEPTANCE/SPEC_GAPS.md`