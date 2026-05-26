# Repository Role Split — Canonical vs Transmission vs Experiment

Purpose
- Freeze the role of the major repo branches so philosophy, canonical derivation, and code experiments stop silently competing.

## Role assignment

### `TheoryOfChange/`
Role:
- philosophical transmission lane
- archival lineage
- long-form derivation narrative
- historical/explanatory material

Allowed:
- motivation
- objections
- readable derivation
- historical and rhetorical framing
- preservation of prior chains and exploratory material

Not authoritative for:
- final dependency truth of kernel components
- final code mapping truth

### `TheoryOfChange_main/`
Role:
- canonical derivation lane
- source of truth for atomic statements and dependency-clean concept records
- canonical bridge from theory to kernel/runtime through `ChangeOntCode/docs/kernel_spec/`

Allowed:
- exact dependency declarations
- exact grounding status
- exact relation between theory node and code artifact
- explicit drift ledgers

Binding rule:
- if a kernel primitive/element/header/operator has a canonical identity, that identity lives here

### `ChangeOntCode/`
Role:
- experimental realization lane
- proof-of-concept operationalization
- harness for seeing what proposed CO mechanisms actually do on tasks

Allowed:
- runtime contracts
- wiring
- implementation notes
- experiment docs
- family adapters
- honest approximation notes

Not authoritative for:
- final philosophical grounding of a component
- final dependency truth where it contradicts `TheoryOfChange_main/`

## Binding principles

1. One canonical dependency identity per serious concept.
2. Transmission may explain; it must not silently redefine the canonical dependency chain.
3. Code may approximate; it must not silently redefine the ontology.
4. Every runtime component must be classed as one of:
   - faithful implementation
   - approximation
   - placeholder
   - exploratory surrogate
5. Every active kernel component should have a canonical target entry in `ChangeOntCode/docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md` or the relevant kernel-spec file.

## Practical consequence

The intended live chain is now:

`TheoryOfChange/` (motivation and philosophical spine)
→ `TheoryOfChange_main/` (canonical statement graph and kernel map)
→ `ChangeOntCode/` (runtime realization and experiments)

## Current repo reality

This split already existed implicitly, but was not enforced. The goal of the new kernel map is to make that split explicit and give one stable place where:
- each primitive/element is grounded
- each code file is mapped
- each known drift is recorded
