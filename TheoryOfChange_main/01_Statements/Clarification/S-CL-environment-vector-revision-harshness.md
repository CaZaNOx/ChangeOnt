---
id: stmt.cl-environment-vector-revision-harshness
type: CL
title: Revision harshness states how costly delayed correction is once current support becomes wrong
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-kernel]]'
dependencies:
- '[[01_Statements/Clarification/S-CL-global-environment-shape-space]]'
parents:
- '[[01_Statements/Clarification/S-CL-global-environment-shape-space]]'
successors: []
symbols_used: []
sources:
- path: TheoryOfChange_main/00_Meta/CANONICAL_PROBLEM_DEFINITION_AND_PLACEMENT_BASIS_2026-04-19.md:1
flags: []
tags:
- clarification
- environment
- vector
- type/CL
- status/stable
---

# Revision harshness states how costly delayed correction is once current support becomes wrong
## Content
Revision harshness measures the cost of continuing on a stale or wrong line before revising. It is not just whether revision is allowed but what damage accumulates when revision is delayed.

## Why this vector is needed
The kernel needs to know not only whether current support is weak, but how dangerous it is to persist after weakness becomes visible. Otherwise it can harden in regimes where stale continuation is disproportionately punishing.

## Kernel relationship
High revision harshness lowers the legitimacy of premature hardening, keeps revision channels more open, and increases how quickly stale support should lose authority. Low revision harshness allows stronger carry-forward because delayed correction is less damaging.

## Placement guidance
Ask: If the current commitment turns out wrong, how much burden, regret, or irrecoverable loss accumulates before the system can revise? How steeply does delayed revision compound harm?

## Directional law
Increasing switching penalties, trap costs, regret accumulation, or irreversible branch loss should raise revision harshness. Making correction cheap and reversible should lower it.

## Misuse warning
This vector is global only if it is measured by the same admissible logic across problems. It must not be replaced by family labels or by hidden oracle information. If a problem makes this vector hard to estimate, the right output is a wider region or lower confidence—not a family-specific guess.
