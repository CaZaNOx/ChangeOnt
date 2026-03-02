# docs/code_reference/agents/co/utils.md

# CO Utilities

## Purpose

`utils/` contains CO-side helper utilities that do not fit cleanly into primitives, elements, or orchestration.

---

## Why it exists

Support code should not be scattered invisibly across the kernel.

This folder keeps helper behavior explicit.

---

## Likely covered files

### `log_hook.py`
#### Role
CO-side logging helper.

#### Requirement
Must align with the project’s artifact and logging contract.

---

### `residuals.py`
#### Role
Residual/tension helper support.

#### Requirement
Its role should be documented clearly if EB or related mechanisms depend on it.

---

## Status guidance

Utility files should state whether they are:
- canonical active support,
- optional support,
- experimental,
- or legacy/inactive.

Invisible helper drift is still real drift.