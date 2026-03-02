# docs/kernel_spec/11_INTERNAL_REPRESENTATION.md

# Internal Representation

## Status
- **Binding**: path-based, time-free, asymmetry-preserving kernel representation
- **Recommended starting point**: k-local weighted directional path-space fragment
- **Open design space**: exact field naming, exact normalization formulas, exact default `k`

---

## 1. Principle

The canonical internal representation of the CO kernel must not be:
- a flat state vector,
- a purely task-local object snapshot,
- or a time-indexed state table.

Instead, the canonical internal form is a **time-free, order-based, path-structured representation of unfolding**.

---

## 2. Canonical representation

**Recommended starting point**

The canonical internal representation should be a:

> **k-local weighted directional path-space fragment**

This means the kernel represents:
- realized local unfolding,
- directional ordering,
- branch-space,
- weighted continuation tendencies,
- bend/deformation,
- recurrence,
- closure,
- asymmetry,
- stabilization and destabilization pressure.

---

## 3. What is primitive

**Binding**

The representation treats the following as primitive or near-primitive kernel structure:

- order / precedence
- prior-pointer relation
- path continuity
- branch-space
- structural deformation
- reach / structural separation
- recurrence / loop tendency
- closure / opening tendency
- stability / instability pressure

---

## 4. What is not primitive

**Binding**

The representation must not treat the following as primitive kernel coordinates:

- wall-clock time
- elapsed seconds
- timestamps as ontological anchors
- substance-like object identity as a primitive given

These may appear in outer harness logs, but not as canonical kernel structure.

---

## 5. Required core fields

**Recommended starting point**

The path-space fragment should include the following core fields.

### 5.1 Anchoring and order
- `now_ref`
- `anchor_id`
- `prior_refs`
- `k_window`
- `path_depth`

### 5.2 Realized local segment
- `realized_segment`

Each realized segment entry should include:
- `from_ref`
- `to_ref`
- `action_ref` if relevant
- `order_rank`
- `transition_weight`
- `bend_local`
- `delta_signature`

### 5.3 Local branch-space
- `branch_space`

Each branch candidate should include:
- `candidate_ref`
- `parent_ref`
- `branch_weight`
- `selection_bias`
- `constraint_status`

### 5.4 Structural profiles
- `bend_profile`
- `loop_profile`
- `closure_profile`
- `density_profile`
- `asymmetry_profile`
- `compressibility_profile`
- `gauge_profile`
- `tension_profile`
- `stabilization_profile`

### 5.5 Regime-control profiles
- `meta_regime_prior`
- `runtime_regime_profile`
- `classicality_profile`
- `reeval_pressure`
- `cadence_profile`

### 5.6 Decision surface
- `continuation_surface`
- `constraint_surface`
- `confidence_profile`

---

## 6. Branch-space explicitness

**Recommended starting point**

The implementation should maintain an explicit **local top-k branch-space**.

Rationale:
- implicit-only continuation scores lose too much path geometry,
- richer full local graphs are more expensive and harder to stabilize,
- top-k explicit branch-space is a good compromise between CO-faithfulness and practical implementation.

---

## 7. Bus role

**Binding**

The bus is not the deepest ontology of the kernel.

The bus is an implementation carrier for structured kernel signals.

The deeper canonical representation is path-space based.

---

## 8. Derived notions

**Binding**

Time-like or rate-like notions may be derived from structured unfolding, but only as derived quantities.

Examples:
- deformation per structural advance,
- recurrence span,
- stability persistence across many ordered advances.

These must not be treated as primitive coordinates.

---

## 9. Misalignment examples

Code is misaligned with this spec if it:
- treats `t` or clock time as a primitive kernel axis,
- collapses the kernel to flat state features,
- erases order and prior-pointer structure,
- lacks branch-space entirely,
- or treats the bus as the ontologically primary internal representation.