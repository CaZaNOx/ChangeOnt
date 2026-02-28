# Naming and Canonical Keys

## Purpose

This page defines canonical naming rules for kernel spec docs and kernel code-facing semantic units.

It exists to stop naming drift, duplicate meanings, and mixed-key chaos.

---

## Core Principle

A semantic unit should have:
- one canonical name
- one canonical role
- one canonical key/location where applicable

Aliases may exist temporarily in legacy code, but the docs must define the target canonical form.

---

## Layer Prefix Conventions

### Primitives
Use `P#_Name`

Examples:
- `P1_BendMetric`
- `P2_Gauge`
- `P3_MDL`

### Elements
Use `E*_Name`

Examples:
- `EA_HAQ`
- `EB_GHVC`
- `EC_Identity`

### Headers
Use `H_*`

Examples:
- `H_SSI`
- `H_CS`
- `H_ID`

### Runtime combinators
Use `C_*`

Examples:
- `C_Pipeline`

### Translators
Use task-facing descriptive names

Examples:
- `bandit_translator`
- `maze_translator`
- `renewal_translator`

---

## Canonical Naming Rule

A name must reflect the unit’s architectural role.

Bad examples:
- naming a state store like a mechanism
- naming a mechanism like a primitive
- naming a control layer like an ontology claim

If the current implementation name is imperfect but stable, docs may keep it while clarifying its true role.

---

## Canonical Store / Key Rule

If a unit has a canonical shared store/key, docs must name it explicitly.

Examples:
- canonical bus store
- canonical prototype store
- canonical signal keys

There must not be multiple competing canonical keys in binding docs.

---

## Signal Key Rule

Signals should use:

`ElementName.field`

Examples:
- `EC_Identity.same`
- `EC_Identity.last_d`
- `EB_GHVC.pressure`
- `EB_GHVC.mdl_gain`

This keeps semantic ownership explicit.

---

## Telemetry Field Rule

Top-level telemetry fields should be:
- stable
- few
- intentionally named
- not arbitrary aliases of the same thing

If a field is only a convenience alias, docs must say so.

Canonical semantic ownership stays with the `signals[...]` dict.

---

## Temporary Legacy Rule

Legacy or implementation-mess names may still exist in code temporarily.

When they do:
- docs define the target canonical form
- legacy names are treated as migration debt
- new docs must not re-legitimize old inconsistent aliases

---

## Philosophical Naming Rule

Names should not overclaim.

For example:
- if something is a minimal local grouping primitive, do not name/spec it as full final metaphysical quotient theory
- if something is only a modulation primitive, do not write it as if it is the full control layer

This rule is binding.

---

## Current Guidance

Prefer:
- stable names
- role-accurate names
- minimal aliasing
- docs that explain imperfect historical names when needed

Avoid:
- proliferating renamed near-duplicates
- mixing semantic and runtime roles in one label
- code names that imply more philosophical completion than actually present