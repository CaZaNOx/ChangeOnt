# docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md

# Component Classification

## Status
- **Binding**: components must be classified as core / optional / experimental / legacy
- **Recommended starting point**: classification below
- **Open design space**: exact promotion criteria for some optional mechanisms

---

## 1. Principle

The codebase must not treat all components as equally canonical if they are not equally supported, wired, and stable.

Every major kernel component should be classified.

---

## 2. Core canonical kernel

**Recommended starting point**

The core canonical kernel should include:

- path-space fragment representation
- meta-header
- header
- primitive layer
- `EA_HAQ`
- `EB_GHVC`
- `EC_Identity`
- one density/precision mechanism
- contribution bridge / vote bridge
- final continuation fusion head
- translator boundary layer

---

## 3. Canonical optional extensions

**Recommended starting point**

These may be supported as canonical optional extensions:

- `EE_Compressibility`
- `EF_Router`
- `EH_BreadthDepth`
- `EI_ChangeOps`
- `EJ_OrderAsymmetry`

Note:
- asymmetry itself is foundational,
- but a separate explicit `EJ` element may still be optional.

---

## 4. Experimental

**Recommended starting point**

Experimental components include:
- mechanisms not yet fully integrated into the active runtime,
- mechanisms with incomplete contracts,
- or mechanisms whose role is still under active design.

Example:
- `ED_GaugeWarp` unless and until fully integrated cleanly.

---

## 5. Legacy / inactive

**Binding**

Historical code or older architecture paths that are not the canonical active runtime must be marked:
- legacy,
- inactive,
- or archival.

They must not compete as coequal runtime truths.

---

## 6. Promotion rule

**Binding**

A component should only be promoted toward core or canonical optional when:
- its role is clearly documented,
- its runtime path is active and honest,
- its interface contract is explicit,
- its config surface is real rather than decorative,
- and its contribution can be investigated honestly in the suite.

---

## 7. Misalignment examples

Code is misaligned with this spec if:
- experimental components masquerade as stable core runtime,
- legacy paths remain undocumented as legacy,
- or unsupported mechanisms remain in baseline configs as if fully canonical.