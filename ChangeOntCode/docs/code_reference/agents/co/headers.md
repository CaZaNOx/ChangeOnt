# docs/code_reference/agents/co/headers.md

# CO Headers

## Purpose

`headers/` contains:
- meta-header
- common header support
- concrete header variants or families

This is the control layer for regime framing and live regime modulation.

---

## Why it exists

The kernel must distinguish between:
- prior regime information known from the task/environment
and
- live runtime regime interpretation based on observed structure.

Headers exist to make that distinction explicit and executable.

---

## Main files

### `meta_header.py`
#### Role
Meta-header layer.

#### Why needed
Provides prior regime framing such as:
- rule stability
- prior classicality
- known fixed action schemas
- known strong stabilization of identities or rules

#### Target-state requirement
Must remain distinct from the runtime header.

---

### `H_common.py`
#### Role
Shared/common header support.

#### Why needed
Provides common header state, shared logic, and shared fields.

---

### `H_CS.py`
#### Role
Classical-stability oriented or similarly named header family.

#### Why needed
Supports one regime interpretation family.

#### Requirement
Must have an honest documented role and update behavior if active.

---

### `H_ID.py`
#### Role
Identity-sensitive header family.

#### Why needed
Supports a distinct regime interpretation emphasis.

#### Requirement
Must not be treated as fully canonical if update behavior is incomplete.

---

### `H_SSI.py`
#### Role
Stability/sensitivity/state-interpretation style header family.

#### Why needed
Supports live runtime modulation in at least one canonical baseline header form.

---

## Binding target-state distinctions

### Meta-header
- prior regime frame

### Header
- live local runtime modulation

These roles must not be blurred.

---

## Required documented controls

Headers/meta-headers should document whether they affect:
- classicality modulation
- reevaluation pressure
- structural cadence
- regime labels
- gating of certain fusion paths
- reopening of stabilized assumptions

---

## Misalignment examples

This area is misaligned if:
- meta-header and header are conflated,
- header weighting is documented but not actually used,
- header family initialization is inconsistent with documented family/regime semantics,
- or some header families silently fail in update paths.