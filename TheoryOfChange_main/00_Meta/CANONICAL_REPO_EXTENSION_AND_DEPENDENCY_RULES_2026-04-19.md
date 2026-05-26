# Canonical Repo Extension and Dependency Rules (2026-04-19)

This file freezes the practical repository-side consequence of the current code-layer doctrine.

## Canonical repository claim

A new problem family should normally be admitted by adding a new environment, one family adapter, and runner/config registration.
If a new family requires changing shared placement, shared runtime surfaces, or kernel workers, the burden of proof is on the change.

## Canonical extension loci

- `ChangeOntCode/environments/`
- `ChangeOntCode/agents/co/adapters/`
- runner/config registration
- family tests

## Canonical non-extension loci

A new family should not normally require edits in:
- `ChangeOntCode/agents/co/placement/`
- `ChangeOntCode/agents/co/runtime/surfaces/`
- `ChangeOntCode/agents/co/runtime/support/`
- `ChangeOntCode/agents/co/core/primitives/`
- `ChangeOntCode/agents/co/core/elements/`

## Dependency rule

Shared layers must remain family-blind on the canonical path.
Boundary may package lawful visible facts; placement may estimate one shared regime location; kernel and runtime surfaces must not recover family-specific behavior by importing boundary or adapter logic.

## Why this matters

Without this repository rule, the architecture can look clean in prose while silently drifting in code.
