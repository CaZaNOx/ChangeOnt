# docs/code_reference/agents/co/registries.md

# CO Registries

## Purpose

`registries/` contains registry/config metadata used to map names to kernel parts.

---

## Why it exists

Registries can make variant assembly and lookup explicit instead of hardcoding everything in one builder.

---

## Main files

### `registry.yaml`
#### Role
Registry key/value mapping for kernel parts, components, or wiring references.

#### Requirement
Registry keys must align with the active builder/runtime expectations.

If registry and builder disagree on key names or semantics, that is a real misalignment.

---

### `factories.py`
#### Role
Factory support for registry-driven object construction.

#### Requirement
Its status must be explicit:
- active canonical support,
- optional support,
- experimental,
- or legacy/inactive.

---

## Target-state rule

**Binding**

If a registry-driven path exists, it must not drift semantically from the active runtime path.

Either:
- it is the canonical assembly path,
- or it is clearly marked otherwise.

---

## Misalignment examples

This area is misaligned if:
- registry keys and builders expect different names,
- registry files suggest configurability that active runtime never honors,
- or factories represent a second competing assembly model with no status clarity.