# Domain-Relative Coarseness Field Update — 2026-05-25

## What changed

This update refines coarseness from a single scalar fallback into a bounded anisotropic profile:

- `coarseness_radius` remains the global fallback;
- `coarseness_by_domain` records active public relation/burden-domain coarseness;
- rows now expose `dynamic_shape_domain_coarseness` when a public relation-field domain exists.

## Why

A system may be fine-grained in one invariant and coarse in another. A single coarseness scalar can wrongly imply that resolution transfers across all domains. CO requires coarseness to follow retained differences: domains become finer/coarser only when public relation/burden/hiddenness/admissibility/sequence evidence earns that distinction.

## Guardrails

The implementation does not introduce arbitrary dimensions. Domain keys come from public relation/burden domains already emitted by RelationSurface / relation-field telemetry. It does not use family names, action names, hidden state, reward hindsight, baseline values, or post-hoc performance.

## Status

First-pass telemetry/control-gauge support. This is not a final metric theory and does not claim performance improvement.
