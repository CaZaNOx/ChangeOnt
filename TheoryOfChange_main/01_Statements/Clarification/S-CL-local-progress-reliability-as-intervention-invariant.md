---
id: stmt.cl-local-progress-reliability-as-intervention-invariant
type: CL
title: Local-Progress Reliability should be measured as a shared intervention-response invariant
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-kernel]]'
dependencies:
- '[[01_Statements/Clarification/S-CL-environment-vector-local-progress-reliability]]'
- '[[01_Statements/Clarification/S-CL-problem-to-environment-placement-protocol]]'
parents:
- '[[01_Statements/Clarification/S-CL-environment-vector-local-progress-reliability]]'
successors: []
symbols_used: []
sources:
- path: TheoryOfChange_main/01_Statements/Clarification/S-CL-environment-vector-local-progress-reliability.md:1
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

# Local-Progress Reliability should be measured as a shared intervention-response invariant
## Content
Local-Progress Reliability should not be assigned by family intuition or retrospective fitting. It should be measured by a shared intervention-response rule that applies across all admitted problems.

The shared question is:

> How trustworthy local progress cues are as guides to true longer-horizon improvement.

## Why this form is needed
If local-progress reliability is left as an impressionistic label, then cross-problem placement remains handwavy. The same number on the vector would not mean the same thing across maze, bandit, renewal, games, search, or control.

## Shared measurement idea
A lawful placement should expose whether locally good-looking moves continue to reduce burden under lawful rollout. The score should therefore come from short rollout progress probes.

## Dimensionless readout
A suitable dimensionless readout is: normalized agreement between local progress signal and realized improvement.

What must remain invariant is not the raw unit but the logic:

> stronger expression of the same intervention-response pattern means a more extreme value on the vector.

## Directional law
If a problem deformation changes the task so that the same probe exhibits stronger expression of this pattern, then the vector should move monotonically in the corresponding direction.

## Placement consequence
Lower values should reduce greedy closure and permit broader nonlocal unfolding.

## Misuse warning
It is invalid to assign local-progress reliability by family label or by whichever environment later performs best. The score must come from the shared intervention-response rule itself.
