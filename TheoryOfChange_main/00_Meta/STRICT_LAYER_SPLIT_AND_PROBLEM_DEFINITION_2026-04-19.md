# STRICT_LAYER_SPLIT_AND_PROBLEM_DEFINITION_2026-04-19

Status: historical/superseded bridge note. Retained for background only; it does not override `CANONICAL_REFERENCE_STACK.md`, `TARGET_KERNEL_ARCHITECTURE_DOCTRINE.md`, or the current `ChangeOntCode/docs/kernel_spec/` execution loop. If this file conflicts with the current Boundary → CandidateSurface → RelationSurface → RCF → CollapseCertificate → CommitmentSurface route, the current route wins.

## Purpose

This file hardens the repository against drift in two ways:

1. it freezes the distinct runtime layers that must remain separate,
2. it defines the generic CO notion of a problem so later code does not silently inherit classical assumptions.

## Core rule

A clean CO execution route must be decomposed into the following distinct layers:

1. **Runner**
   - parity, execution, logging, evaluation only
   - no family-side assistance to CO or baselines beyond their admitted interfaces

2. **Environment**
   - native transition law
   - legality
   - hidden structure
   - reward / outcome / termination
   - environment is not CO-aware

3. **Boundary / translation**
   - native observation -> generic packet
   - generic decision -> native action
   - native outcome -> generic update packet
   - boundary may expose only lawful visible facts, legality/masking, and justified shared-axis measurements
   - boundary may not perform family-local ranking, planning, or target proposal

4. **Shared placement / vector map**
   - receives only generic packets
   - estimates location in one shared regime space
   - similar problems in similar regimes must induce similar placement and similar kernel shaping
   - no family may introduce a private regime space

5. **Kernel**
   - support / contradiction / continuity / rivalry / identity / commitment / revision
   - kernel must not need to know benchmark family in order to operate

6. **Boundary return**
   - projects generic decision into native action
   - does not repair, rescue, or reinterpret the decision through family-local strategy

## Prohibition on forbidden non-CO rescue

The canonical CO route must not recover competence through forbidden non-CO rescue, family rescue hooks, or benchmark-local planners.

The claim is not that CO performs well because a classical method is silently waiting underneath it.
The claim is that lawful placement in the shared regime map should modulate the kernel so that discrete/classical-looking behavior emerges from the kernel when appropriate.

Therefore:

- no forbidden non-CO rescue in the canonical CO action path,
- no classical proposal blended into the canonical CO action path,
- no family-local rescue logic inside shared runtime surfaces,
- no translator-side candidate ranking that functions as a hidden planner.

Comparative or investigatory code may still exist separately, but it must be physically and conceptually separate from the canonical CO route.

### Fail-closed clarification

The canonical route must fail closed when required public structure is absent.
It may not convert missing evidence into first-legal, uniform, greedy, or baseline-policy action choice.

Therefore:

- the boundary may return an empty/non-evidential packet, but must not invent a uniform candidate field;
- CandidateSurface may log missing candidate evidence, but must not publish uniform candidate votes;
- CommitmentSurface may reject a malformed/non-evidential step, but must not select from bare legal action space;
- an experiment runner may report the failure, but may not count the failed step as CO evidence.

This is not an engineering preference. It is required by the layer split: missing kernel evidence cannot be repaired by problem-local or baseline-policy action choice without invalidating the CO claim.

## Problem (CO)

**Problem (CO)** := A constrained episode of unresolved continuation in which current stabilization is insufficient to carry an operative path, such that intervention, revision, commitment, or lawful nonclosure becomes necessary.

This definition matters because CO must not import an unexamined classical notion of problem as primitive.
A classical optimization problem, MDP, or constraint satisfaction problem may be treated as a late stabilized special case of this more general structure.

## Task vs problem

- **Task** := the externally specified requirement (maximize reward, reach goal, open door, identify regime, etc.)
- **Problem** := the actual unresolved continuation structure encountered while attempting the task

A task may be simple while the problem is difficult because the operative identity, action meaning, or abstraction is wrong.

## Structural coding consequences

The repository should physically reflect the following role split:

- `boundary/` for packet mapping only
- `placement/` for shared-axis measurement and posture derivation
- `kernel/` for primitives, elements, and kernel state only
- `runtime/surfaces/` for decision/telemetry surfaces that are not ontological elements
- `runtime/support/` for buses, trackers, budgets, and helper memories
- `integration/` for assembly and registration only

Support-only runtime modules must not be stored as if they were canonical primitives or elements.