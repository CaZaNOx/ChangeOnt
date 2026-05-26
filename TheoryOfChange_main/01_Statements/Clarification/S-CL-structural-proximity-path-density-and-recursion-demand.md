---
id: stmt.structural-proximity-path-density-recursion-demand
type: CL
aliases:
- S-CL-structural-proximity-path-density-and-recursion-demand
- StructuralProximity
- PathDensityRecursionDemand
title: Structural proximity, path density, and recursion demand
concepts:
- '[[02_Concepts/C-change-space-metric]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
- '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
- '[[01_Statements/Derivation/S-DR-pressure-signature-continuation-branch-identity.md]]'
parents:
- '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
successors:
- '[[../ChangeOntCode/docs/kernel_spec/81_STRUCTURAL_PROXIMITY_PATH_DENSITY_AND_RECURSION_CONTRACT.md]]'
symbols_used: []
flags:
- recursion-not-search-depth
- path-density-requires-quotient-filter
status: canonical-scaffold
tags:
- layer/foundations
- domain/operational
- type/CL
- concept/proximity
- concept/path-density
- concept/recursion
- concept/kernel-bridge
---
# Structural proximity, path density, and recursion demand

## Claim
Structural proximity is not spatial closeness. Two continuations are structurally proximate when a deformation, burden change, evidence update, quotient, cancellation, or collapse in one changes the continuation-status of the other.

Path density matters only after equivalence filtering. Many paths do not automatically demand recursion.

## Path-density distinction
```text
dense equivalent paths
→ quotient / merge / collapse pressure

dense non-equivalent live paths
→ grey preservation / recursion pressure

dense irrelevant paths
→ no special continuation-field demand
```

## Recursion demand
Recursion demand rises when structurally proximate, non-equivalent continuations carry unresolved burden whose further unfolding may change relation, quotient, cancellation, or collapse status.

This differs from search depth. Search depth expands because future states may improve expected value. CO recursion expands because unresolved continuation structure remains operative and cannot yet be lawfully thinned without losing relevant pressure topology.

## Operational signals
Potential signals of recursion demand include:

- high non-equivalent path density near the active branch;
- unresolved burden shared by nearby branches;
- rivalry among branches with similar local support but different pressure signatures;
- hiddenness that may change quotient or relation status;
- cancellation/relief candidates whose effect is not yet resolved;
- high consequence span of premature collapse.

## Anti-bloat rule
Path density alone is not enough. If additional paths are equivalent under active continuation tolerance, they should quotient. If they are nonoperative for burden, relation, admissibility, or collapse, they should thin. Recursion is justified only when another layer can change the live continuation field.

## Tags
#type/CL #layer/foundations #domain/operational #concept/proximity #concept/path-density #concept/recursion #concept/kernel-bridge #status/canonical-scaffold
