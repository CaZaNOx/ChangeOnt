---
id: stmt.cl-anchor-stability-as-intervention-invariant
type: CL
title: Anchor Stability should be measured as a shared intervention-response invariant
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-kernel]]'
dependencies:
- '[[01_Statements/Clarification/S-CL-environment-vector-anchor-stability]]'
- '[[01_Statements/Clarification/S-CL-problem-to-environment-placement-protocol]]'
parents:
- '[[01_Statements/Clarification/S-CL-environment-vector-anchor-stability]]'
successors: []
symbols_used: []
sources:
- path: TheoryOfChange_main/01_Statements/Clarification/S-CL-environment-vector-anchor-stability.md:1
- path: TheoryOfChange_main/01_Statements/Clarification/S-CL-problem-to-environment-placement-protocol.md:1
flags: []
tags:
- clarification
- environment
- vector
- measurement
- type/CL
- status/stable
---

# Anchor Stability should be measured as a shared intervention-response invariant
## Content
Anchor Stability should not be assigned by family intuition or retrospective fitting. It should be measured by a shared intervention-response rule that applies across all admitted problems.

The shared question is:

> How stable the direction-of-better or target criterion itself remains over time.

## Why this form is needed
If anchor stability is left as an impressionistic label, then cross-problem placement remains handwavy. The same number on the vector would not mean the same thing across maze, bandit, renewal, games, search, or control.

## Shared measurement idea
A lawful placement should expose whether what counts as better remains stable under unfolding. The score should therefore come from anchor drift probes.

## Dimensionless readout
A suitable dimensionless readout is: normalized stability of the target/direction signal over time.

What must remain invariant is not the raw unit but the logic:

> stronger expression of the same intervention-response pattern means a more extreme value on the vector.

## Directional law
If a problem deformation changes the task so that the same probe exhibits stronger expression of this pattern, then the vector should move monotonically in the corresponding direction.

## Placement consequence
Lower values should delay hard target-lock and preserve broader anchor-sensitive unfolding.

## Misuse warning
It is invalid to assign anchor stability by family label or by whichever environment later performs best. The score must come from the shared intervention-response rule itself.
