# docs/code_reference/agents/co/core/engine_and_pipeline.md

# CO Engine and Pipeline

## Purpose

This document explains the runtime orchestration layer inside the CO core.

It covers:
- the active runtime path,
- pipeline orchestration,
- engine-like components,
- and how element/primitives are stepped or updated.

---

## Why it exists

The kernel must have a clearly documented execution path.

This documentation exists to prevent:
- multiple competing runtime truths,
- hidden bypasses,
- and drift between architectural intent and actual execution.

---

## Main files

### `pipeline.py`
High-level or wrapper pipeline-related logic.

#### Role
Should expose the canonical or near-canonical orchestration entrypoint for kernel execution.

#### Requirement
Its relationship to the lower-level combinator/pipeline implementation must be explicit.

---

### `combinators/C_pipeline.py`
Primary pipeline combinator / runtime orchestration logic.

#### Expected role
- execute the active element path in the correct staged order
- preserve the select/update distinction
- ensure action/final continuation logic is not mixed incorrectly into the update pass

#### Binding expectations
A canonical pipeline must:
- preserve select/update separation
- enforce action/final fusion at the correct stage
- apply dependency/order logic honestly
- not silently swallow critical failures in a way that hides semantic breakage

---

### `engine.py`
Engine-style orchestration object.

#### Role
Represents an engine-level abstraction over the kernel.

#### Important note
This file must not silently compete with the canonical active adapter → builder → pipeline runtime path unless explicitly documented as:
- canonical,
- experimental,
- or legacy/inactive.

---

### Other combinator files
Examples:
- `C_gate`
- `C_fuse`
- `C_math_policy`
- `C_transform_chain`
- etc.

#### Role
Potentially supply local operator or routing structures.

#### Requirement
Their status must be explicit:
- active canonical,
- optional canonical,
- experimental,
- or legacy/drifting.

---

## Canonical target-state execution structure

**Binding**

The active runtime path must preserve:

1. translated path-space update is available
2. header/meta-header relevant interpretation may occur
3. primitives/elements operate
4. element contribution packets are emitted
5. packets are fused into group outputs
6. group outputs fuse with header/meta-header/classical stream
7. final continuation surface is produced
8. translator collapses continuation surface into concrete task action
9. feedback returns into update path

---

## Select/update separation

**Binding**

The runtime path must preserve a real distinction between:

### Select path
Produces continuation/action-relevant structure.

### Update path
Integrates feedback and adjusts internal state without pretending to be another select pass.

---

## Misalignment examples

The engine/pipeline layer is misaligned if:
- there are two competing active execution paths without status clarity,
- adapters bypass the canonical orchestration in a way that makes documented control logic inactive,
- update semantics silently mutate state multiple times in structurally incorrect ways,
- strict checking claims exist but are effectively disabled by silent exception swallowing.

---

## Status guidance

- the canonical active pipeline should be **Binding**
- alternative engine-like orchestrators are acceptable only if explicitly marked and non-competing
- silent ambiguity here is especially dangerous because it makes the docs→code pipeline impossible to trust