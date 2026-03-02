# docs/code_reference/agents/co/core/primitives.md

# CO Primitives

## Purpose

Primitives are reusable structural lenses or basis terms.

They are not full mechanisms by themselves.  
They provide the structural ingredients that elements use.

---

## Why they exist

CO does not begin from fixed substance-like objects.

It begins from structured change.

Primitives therefore measure aspects of unfolding such as:
- deformation,
- fit,
- compressibility,
- recurrence,
- closure,
- density,
- asymmetry,
- operational structure.

---

## General contract

**Binding**

A primitive should:
- have a clearly documented structural meaning,
- expose a real runtime contribution,
- be reusable across multiple elements,
- and not be reduced to decorative config labels.

If a primitive is present in configs or docs but not meaningfully active in runtime, that is a misalignment.

---

## Primitive files and intended meanings

### `P1_bend_metric.py`
#### Meaning
Persistence-through-deformation / bend / continuity across change.

#### Why needed
Supports identity-sensitive reasoning and non-static persistence.

#### Typical users
Identity-like elements and any mechanism sensitive to deformation continuity.

---

### `P2_gauge.py`
#### Meaning
Adaptive fit / calibration / mismatch-reducing adjustment.

#### Why needed
Supports gauge-like local alignment and adaptive coherence reasoning.

#### Typical users
EA / adaptive-fit style elements.

---

### `P3_mdl.py`
#### Meaning
Compression / regularity / descriptive economy.

#### Why needed
Supports detecting structure that is more compact than noise.

#### Typical users
EB / compressibility-sensitive mechanisms.

---

### `P7_precision.py`
#### Meaning
Sharpness / precision / confidence-like structural discrimination.

#### Why needed
Helps distinguish vague from crisp local judgments.

---

### `P8_loopiness.py`
#### Meaning
Recurrence / self-return tendency / cyclic structure.

#### Why needed
Supports recurrence-sensitive and closure-sensitive reasoning.

---

### `P10_change_ops_core.py`
#### Meaning
Operational structure of change itself.

#### Why needed
Supports reasoning about how changes compose and differ.

---

### `P12_closure_quotient.py`
#### Meaning
Closure / quotient / stabilized equivalence-like return structure.

#### Why needed
Supports closure-sensitive and stabilization-sensitive mechanisms.

---

### `P15_order_asymetry.py`
#### Meaning
Directional / order-sensitive structure; irreversibility/path dependence.

#### Why needed
Supports asymmetry-sensitive reasoning.

#### Important note
Asymmetry itself is foundational and must not depend solely on this one primitive.

---

### `bandit_stats.py`
#### Meaning
Family-local state holder for bandit-related structure inside CO.

#### Status guidance
Must be clearly documented as either:
- active canonical family primitive support,
- or an adapter-side support primitive with limited scope.

---

### `ngram_model.py`
#### Meaning
Renewal/sequence-side regularity helper primitive.

#### Status guidance
Must have an honest documented API if used by renewal translation/selection logic.

---

### `visit_tracker.py`
#### Meaning
Spatial or local revisitation/density support primitive.

#### Typical users
Density/maze-like mechanisms.

---

## Primitive documentation requirements

For each primitive, docs should eventually state:
- conceptual role
- runtime inputs
- runtime outputs
- elements that use it
- whether it is core / optional / experimental
- any known contract mismatches

---

## Misalignment examples

Primitive documentation is incomplete or code is misaligned if:
- primitive names exist but meaning is unclear,
- primitive APIs do not match their callers,
- config claims to vary primitive behavior but runtime ignores it,
- or a primitive is treated as a full mechanism rather than a reusable basis term.