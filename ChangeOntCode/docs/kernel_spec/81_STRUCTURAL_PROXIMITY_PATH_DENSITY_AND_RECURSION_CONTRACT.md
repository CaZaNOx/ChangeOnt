# 81. Structural Proximity, Path Density, and Recursion Contract

Status: conceptual contract / implementation pending.

This document binds:

```text
S-CL-structural-proximity-path-density-and-recursion-demand.md
S-CL-breath-as-field-expansion-and-contraction.md
```

to RCF and future RelationSurface behavior.

---

## 1. Structural proximity

Two branches are structurally proximate when changing one branch changes the continuation-status of the other. Spatial distance may contribute in spatial domains, but it is not the definition.

Proximity may arise through:

- shared burden type;
- shared evidence source;
- shared task-anchor relation;
- shared admissibility constraint;
- possible relief/cancellation relation;
- rivalry for a commitment slot or resource;
- quotient/equivalence uncertainty;
- reachable-frontier overlap;
- historical coupling inside kernel state.

---

## 2. Path density

Path density is the local abundance of possible continuations around a branch or region. It matters only after equivalence filtering.

```text
dense equivalent paths
→ quotient / merge / collapse pressure

dense non-equivalent paths
→ grey preservation / recursion pressure

dense irrelevant paths
→ no special field demand
```

A runtime must not equate many available actions with high recursion demand.

---

## 3. Recursion demand

Recursion is justified when an additional unfolding layer may change:

- relation topology;
- quotient/equivalence status;
- cancellation or relief status;
- grey-preservation need;
- collapse readiness;
- burden transfer or transformation;
- admissibility under the task anchor.

If another layer cannot change any of these, recursion becomes ordinary search or bloat.

---

## 4. Breath interpretation

Operational breath is field regulation:

```text
expansion:
  preserve grey, expose relations, recurse, retain non-equivalent branches

contraction:
  quotient, cancel, thin, collapse, commit
```

The term does not introduce a new primitive. It describes the alternation between widening and thinning live continuation structure.

---

## 5. Required tests before paper use

A future implementation should include tests where:

1. scalar candidate values are held fixed;
2. path density or relation topology changes;
3. RCF changes recursion/collapse behavior for traceable structural reasons;
4. dense equivalent paths quotient rather than inflate recursion;
5. dense non-equivalent paths preserve grey or trigger bounded recursion.

---

## 6. Current status note

This contract is not yet implemented as a runtime scheduler. It sets the conceptual target for future recursion and path-density telemetry.

## Diagnostic binding update — 2026-05-06

`85_RELATION_TO_COLLAPSE_DIAGNOSTIC_CONTRACT.md` provides the concrete microdiagnostics for this contract. In particular:

```text
dense equivalent branches must quotient;
dense non-equivalent branches may preserve grey or recurse;
sparse high-consequence branches may recurse even without high path density.
```

This prevents path density from being mistaken for ordinary path-count search.
