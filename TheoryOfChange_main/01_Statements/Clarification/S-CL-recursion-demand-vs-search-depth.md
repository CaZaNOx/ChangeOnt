---
id: stmt.cl-recursion-demand-vs-search-depth
title: Recursion demand is not search depth
status: target-state clarification; conceptually closed as distinction; operational scheduler remains watchpoint
parents:
  - '[[01_Statements/Clarification/S-CL-structural-proximity-path-density-and-recursion-demand]]'
  - '[[01_Statements/Derivation/S-DR-burden-relations-to-quotient-collapse-and-recursion]]'
  - '[[01_Statements/Derivation/S-DR-quotient-equivalence-as-continuation-tolerance]]'
type: CL
concepts:
  - '[[02_Concepts/C-kernel]]'
  - '[[02_Concepts/C-change-space-metric]]'
tags:
  - layer/kernel-bridge
  - type/CL
  - concept/recursion-demand
---

# Recursion demand is not search depth

## Core distinction

Search depth asks:

```text
What happens after more future actions are expanded?
```

CO recursion demand asks:

```text
Would another layer of unfolding change burden status, relation topology, quotient/equivalence, grey preservation, or collapse legitimacy?
```

The two can overlap, but they are not identical. CO recursion is not justified merely by difficulty, uncertainty, path count, or high expected reward. It is justified when preserving or unfolding another layer can change whether collapse is lawful.

## Positive trigger

Recursion demand rises when:

```text
structurally proximate,
non-equivalent,
continuation-relevant branches
carry unresolved burden or hiddenness
such that further unfolding may change relation, quotient, grey, or collapse status.
```

This means path density alone is insufficient. Path density matters only after quotient filtering:

```text
dense equivalent paths -> quotient / merge / no recursion explosion;
dense non-equivalent live paths -> grey preservation / bounded recursion;
sparse high-consequence unresolved branch -> recursion may still be demanded;
dense irrelevant paths -> thin / ignore.
```

## What the next recursive layer computes

A recursive layer is justified only if it can change at least one of these:

```text
burden operation classification;
branch relation topology;
quotient/equivalence status;
hiddenness/exposure status;
barrier or threshold regime;
collapse certificate status;
readout admissibility.
```

If the next layer only adds more action-tree nodes without changing these statuses, it is ordinary lookahead rather than CO recursion.

## Stop condition

Recursion should stop or thin when:

```text
rivals are quotient-equivalent, canceled, or nonoperative;
burden is resolved, bounded, or outside the active gauge;
hiddenness is below tolerance or no exposure path exists within the regime;
further unfolding would not change collapse status;
resource budget is exhausted and the runtime must fail-closed or mark non-evidential rather than fallback-rescue.
```

## Open operational watchpoint

The conceptual distinction is closed. The exact scheduler is not final. Runtime code must prove, through diagnostics, that recursion demand is not simply a proxy for branching factor, uncertainty, or search depth.

Required diagnostics:

```text
many equivalent paths -> quotient, not recursion;
many non-equivalent paths -> grey/recursion;
few high-consequence paths -> recursion despite low density;
many irrelevant paths -> no recursion;
same scalar rows, different relation topology -> different recursion demand.
```
