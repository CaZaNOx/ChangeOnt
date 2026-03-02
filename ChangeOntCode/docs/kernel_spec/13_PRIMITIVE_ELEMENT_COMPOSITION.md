# docs/kernel_spec/13_PRIMITIVE_ELEMENT_COMPOSITION.md

# Primitive and Element Composition

## Status
- **Binding**: primitives are reusable basis terms; relation form matters
- **Recommended starting point**: explicit primitive use, combinators, transforms, and weights inside element definitions
- **Open design space**: exact config syntax and exact transform library

---

## 1. Principle

Primitives are not full mechanisms by themselves.

Primitives are reusable basis terms or structural lenses.

Elements are mechanism forms built by composing primitives under:
- relation forms,
- transforms,
- weights,
- and element-specific semantics.

---

## 2. Primitive reuse

**Binding**

The same primitive may appear in multiple elements.

Its role in those elements may differ because:
- the combinator differs,
- the transform differs,
- the weight differs,
- the target interpretation differs.

Example:
- `P1` in one element need not mean exactly what `P1` means in another.

---

## 3. Relation form matters

**Binding**

Primitive meaning in an element is not exhausted by bare inclusion.

Meaningful differences include:
- additive use,
- subtractive use,
- multiplicative use,
- divisive use,
- thresholded use,
- gated use,
- nonlinear or transformed use,
- order-sensitive use.

This is a core part of CO and must not be reduced to “primitive present = same mechanism”.

---

## 4. Weights are first-class

**Binding**

Weights are not mere engineering clutter.

Weights are part of the mechanism definition.

They may exist at multiple layers:
- primitive contribution weight inside an element,
- element contribution weight inside a group,
- group contribution weight in final fusion.

---

## 5. Recommended element definition shape

**Recommended starting point**

Each element definition should specify:

- element identity
- purpose
- primitives used
- primitive transforms
- primitive combinators
- primitive weights
- local element parameters
- expected output packet types

---

## 6. Group composition

**Binding**

Elements may be grouped into higher-order structures.

Examples:
- `EA + EB`
- `EA - EB`
- weighted mixtures
- gated mixtures
- order-sensitive mixtures

This composition is a distinct layer from primitive→element composition.

---

## 7. Misalignment examples

Code is misaligned with this spec if:
- element semantics are hardcoded but weights/combinators are decorative,
- the same primitive cannot be meaningfully reused across elements,
- group composition is only an ad hoc special case,
- or config claims to vary primitive/combinator/weight choices that runtime ignores.