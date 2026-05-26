# 17. Component Classification

Status: canonical classification aid for active kernel docs.  
Last consolidated: 2026-05-06.

This file prevents category collapse. It says what kind of thing a component is; it is not the primary explanation of what the component means.

## Classification legend

```text
core primitive / operation:
  minimal operation-type required by the current CO kernel target.

mechanism bundle:
  a coordinated runtime mechanism built from several primitives/operations.

runtime surface:
  implementation carrier or interface where primitives/elements are applied.

boundary / translator:
  problem-specific public-structure exposure, not kernel policy.

support / telemetry:
  logging, carrier, or diagnostic infrastructure.

investigatory:
  retained for comparison or future work, not active evidence-bearing doctrine.

inactive / deprecated alias:
  historical name/path not authoritative for active target.
```

## Core primitives / operations

| Item | Classification | Active role |
|---|---|---|
| P1 Bend / BendMetric | core primitive / operation | local deformation of continuation possibility; pressure direction/shape. |
| P2 Gauge | core primitive / operation | local comparison/tolerance regime for burden, quotient, hiddenness, collapse. |
| P4 ReID / Identity-through-change | core primitive / operation | branch continuity through changing expressions. |
| P5 Temporal Retention | core primitive / operation | carried trace/state across loops and transformations. |
| P10 ChangeOpsCore / EI ChangeOps | core operation bundle | carry, amplify, expose, buffer, mask, relieve, cancel, transfer, transform. |
| P12 Closure / Quotient | core primitive / operation | identify loss of continuation-relevant difference; prevent false grey/path explosion. |
| P16 Remaining Transformation Burden | core primitive / operation | continuation-relevant de-centering / anchored operative tension. |
| Thin Collapse | core operation | legitimate compression of live structure into row, scalar, branch, certificate, or action. |

## Provisional or investigatory primitives/elements

| Item | Classification | Note |
|---|---|---|
| EA_HAQ / adaptive quotienting | provisional | active tolerance idea; exact law and calibration still open. |
| ED_GaugeWarp | provisional | useful gauge modulation concept; needs formula grounding. |
| EG_DensityPrecision | provisional | support for discrimination/precision; not deepest core. |
| P7 Precision | provisional | active discrimination support, not full active primitive. |
| P3 MDL / EE_Compressibility | investigatory | may support collapse/retention analysis later; not canonical evidence path. |
| P8 Loopiness | investigatory | useful recurrence/cycle signal, not core unless behaviorally required. |
| P9 VariableBirth / creative option birth | investigatory | future continuation-generation work; not current kernel proof path. |
| P11 Residuation | investigatory | promising formalization of remaining burden; not final algebra. |
| EF_Router | investigatory | comparison/control path, not core ontology. |
| EH_BreadthDepth | investigatory | exploration-style bundle, not current canonical kernel. |
| EJ_OrderAsymmetry | investigatory/provisional | asymmetry is foundational, but EJ as a separate element is not yet required. |

## Mechanism bundles

| Component | Classification | Note |
|---|---|---|
| RecursiveContinuationField | mechanism bundle | coordinates burden/debt, relations, grey, quotient, recursion, viability, collapse readiness. Not a primitive. |
| CollapseCertificate | mechanism/readout gate | structured earned-collapse check. Not merely a score. |
| ContinuationState | runtime state mechanism | carries branch/viability history; not a deep primitive. |

## Runtime surfaces

| Component | Classification | Active role |
|---|---|---|
| CandidateSurface | runtime surface | kernel intake; publishes candidate expressions/rows without making actions into branches. |
| RelationSurface | runtime surface | derives branch-internal operations and cross-branch relations from public effects. |
| CommitmentSurface | runtime surface / readout | expresses earned collapse as native action; no non-CO rescue selector. |
| Problem contracts | boundary data structure | declarative family-to-kernel public problem contract under `agents/co/core/contracts/`. |
| Signal bus / telemetry helpers | support / telemetry | runtime support only; not action selection and not ontology mechanism. |

## Boundary / translator components

Adapters, observation mappers, action mappers, and problem contracts expose public problem structure. They may publish public facts and public_effects but must not publish policy advice, optimal action, hidden state strategy, or classical rescue.

## Non-active residues

Names or paths that do not have docs, active code, and diagnostics in the current loop are not evidence-bearing components. If such a path is retained for comparison or migration, it must be documented as support-only, investigatory, or invalid for evidence-bearing runs before use.

## Promotion rule

A component may be promoted only when:

```text
the conceptual need is clear;
the canonical doc states its role;
the runtime carrier is active;
diagnostics show it changes behavior for the documented reason;
it does not leak policy, fallback, or undocumented scoring.
```

## Demotion rule

A component must be marked provisional, investigatory, inactive, or support-only when:

```text
it is not required by the current kernel target;
it exists only as migration residue and is not required by the current target;
it cannot yet be distinguished behaviorally from known/classical machinery;
it lacks formula or trace grounding;
it belongs to future consciousness/math work rather than the current kernel.
```
