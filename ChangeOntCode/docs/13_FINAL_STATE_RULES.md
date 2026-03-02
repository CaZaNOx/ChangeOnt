# docs/13_FINAL_STATE_RULES.md

# Final State Rules

This file states the canonical project-level rules for the desired final state.

## 1. Docs to code rule

**Binding**

The documentation must capture the target state precisely enough that any meaningful code divergence can be classified as:
- compliant,
- incomplete,
- incorrect,
- experimental,
- or legacy.

The docs are the target-state authority. The code is the implementation.

---

## 2. Canonical runtime rule

**Binding**

There must be exactly one canonical active runtime path for:
- suite orchestration,
- runner execution,
- translator boundaries,
- CO kernel construction,
- CO kernel execution,
- artifact generation,
- summary generation.

Competing active runtime paths are a failure state unless one is explicitly marked experimental and isolated.

---

## 3. CO-honesty rule

**Binding**

The codebase must not claim to implement CO honestly unless:
- the kernel is wired in a way faithful to the theory,
- primitive/element/fusion/header/meta-header behavior is real rather than decorative,
- classicality is treated as a regime judgment rather than silently smuggled as primitive truth,
- plots and summaries are semantically correct,
- the suite compares CO and STOA honestly.

---

## 4. Classical collapse rule

**Binding**

CO does not need to dominate all domains.

Highly classical, fixed-rule, strongly stabilized domains may legitimately collapse toward near-total classical/STOA dominance.

This collapse must be:
- explicit,
- regime-conditioned,
- and reopenable when instability or deformation increases.

---

## 5. Asymmetry rule

**Binding**

Asymmetry is foundational.

The canonical kernel must preserve asymmetry in:
- internal representation,
- update semantics,
- and at least some fusion/composition behavior.

Symmetry may appear only as a local or derived special case where justified.

---

## 6. Time rule

**Binding**

External time is not primitive in the kernel.

The kernel must be based on:
- order,
- precedence,
- path relation,
- reach,
- structural spacing,
- deformation,
- recurrence.

Time-like measures may be derived from structured unfolding, but must not be assumed as primitive kernel coordinates.

---

## 7. Extensibility rule

**Binding**

The final architecture must support:
- adding new environments,
- adding new runners,
- adding new translators,
- adding new primitives,
- adding new elements,

without architectural drift or ad hoc rewiring of unrelated subsystems.

---

## 8. Status rule

**Binding**

Every major kernel and harness concept should be documented with one of:
- Binding
- Recommended starting point
- Open design space
- Experimental
- Legacy / inactive

This avoids smuggling provisional implementation choices as if they were uniquely derived.

---

## 9. Full configuration rule

**Binding**

`CO_full` denotes the maximal coherent supported kernel configuration, not merely “many flags enabled”.

It should represent the fullest honest active kernel configuration that the project currently supports.

---

## 10. Investigation rule

**Binding**

The suite is not only a benchmark harness. It is also a philosophical/mechanistic investigation harness.

It must support honest investigation of:
- primitive effects,
- element effects,
- combinator effects,
- weighting effects,
- threshold effects,
- interaction effects between elements,
- full vs reduced kernel configurations,
- and cross-context stability of parameter choices.