# Canonical Code Layer Split (2026-04-19)

Status: historical/superseded bridge note. Retained for background only; it does not override `CANONICAL_REFERENCE_STACK.md`, `TARGET_KERNEL_ARCHITECTURE_DOCTRINE.md`, or the current `ChangeOntCode/docs/kernel_spec/` execution loop. If this file conflicts with the current Boundary → CandidateSurface → RelationSurface → RCF → CollapseCertificate → CommitmentSurface route, the current route wins.

This file freezes the active code-layer doctrine.

## Canonical execution layers

1. runner
2. environment
3. boundary
4. placement
5. kernel primitives / elements
6. runtime surfaces
7. runtime support

These layers are distinct and must not be silently blended.

## Canonical directories

- `ChangeOntCode/experiments/runners/`
- `ChangeOntCode/environments/`
- `ChangeOntCode/agents/co/boundary/`
- `ChangeOntCode/agents/co/placement/`
- `ChangeOntCode/agents/co/core/primitives/`
- `ChangeOntCode/agents/co/core/elements/`
- `ChangeOntCode/agents/co/runtime/surfaces/`
- `ChangeOntCode/agents/co/runtime/support/`

## Role rules

### Boundary
Boundary exposes only lawful visible facts, legal/native action mapping, and realized updates.
It must not contain family-specific policy logic.

### Placement
Placement estimates shared regime location only.
It must not rank actions or solve a family.
Historical note: this older file named `axes.py`, `measure.py`, and `estimate.py`; the current active placement locus is `ChangeOntCode/agents/co/placement/shape_prior6.py`, `control.py`, `control_defaults.py`, and `regime.py`.

### Kernel primitives / elements
These are the only places where the CO workers live.
They must remain family-blind on the canonical path.

### Runtime surfaces
Runtime surfaces consume already-shaped candidate/evidence fields and commit/publish them.
They are not ontology elements.

### Runtime support
Runtime support contains buses, trackers, ledgers, memory helpers, and other support utilities.
These are not primitives.

## New-problem extension rule

A new problem family should normally require edits only in:
- `environments/<family>/...` or the family environment file
- `agents/co/adapters/<family>_adapter.py`
- runner registration/config

A new family should **not** require edits in:
- `agents/co/core/primitives/`
- `agents/co/core/elements/`
- `agents/co/runtime/surfaces/`

If a new family appears to require changing kernel elements or runtime surfaces, treat that as an architectural failure until justified.

## Canonical surface/support names

Historical names are retired on the active path.

- `CandidateSurface` -> `CandidateEvidenceSurface`
- `CommitmentSurface` -> `CommitmentSurface`
- `CoVoteBus` -> `KernelSignalBus`