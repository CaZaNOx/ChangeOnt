---
id: stmt.cl-consequence-depth-as-intervention-invariant
type: CL
title: Consequence Depth should be measured as a shared intervention-response invariant
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-kernel]]'
dependencies:
- '[[01_Statements/Clarification/S-CL-environment-vector-consequence-depth]]'
- '[[01_Statements/Clarification/S-CL-problem-to-environment-placement-protocol]]'
parents:
- '[[01_Statements/Clarification/S-CL-environment-vector-consequence-depth]]'
successors: []
symbols_used: []
sources:
- path: TheoryOfChange_main/01_Statements/Clarification/S-CL-environment-vector-consequence-depth.md:1
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

# Consequence Depth should be measured as a shared intervention-response invariant
## Content
Consequence Depth should not be assigned by family intuition or retrospective fitting. It should be measured by a shared intervention-response rule that applies across all admitted problems.

The shared question is:

> How far beyond local evidence the true consequence of current choice lies.

## Why this form is needed
If consequence depth is left as an impressionistic label, then cross-problem placement remains handwavy. The same number on the vector would not mean the same thing across maze, bandit, renewal, games, search, or control.

## Shared measurement idea
A lawful placement should expose whether shallow local support fails to capture downstream burden or payoff change. The score should therefore come from delayed-consequence rollout probes.

## Dimensionless readout
A suitable dimensionless readout is: normalized depth at which local ranking stabilizes or flips.

What must remain invariant is not the raw unit but the logic:

> stronger expression of the same intervention-response pattern means a more extreme value on the vector.

## Directional law
If a problem deformation changes the task so that the same probe exhibits stronger expression of this pattern, then the vector should move monotonically in the corresponding direction.

## Placement consequence
Higher values should preserve longer-path unfolding before hard collapse.

## Misuse warning
It is invalid to assign consequence depth by family label or by whichever environment later performs best. The score must come from the shared intervention-response rule itself.
