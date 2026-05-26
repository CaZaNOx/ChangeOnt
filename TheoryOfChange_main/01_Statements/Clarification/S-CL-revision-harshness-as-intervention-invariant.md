---
id: stmt.cl-revision-harshness-as-intervention-invariant
type: CL
title: Revision harshness should be measured as a shared intervention-response invariant
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-kernel]]'
dependencies:
- '[[01_Statements/Clarification/S-CL-environment-vector-revision-harshness]]'
- '[[01_Statements/Clarification/S-CL-problem-to-environment-placement-protocol]]'
parents:
- '[[01_Statements/Clarification/S-CL-environment-vector-revision-harshness]]'
successors: []
symbols_used: []
sources:
- path: TheoryOfChange_main/01_Statements/Clarification/S-CL-environment-vector-revision-harshness.md:1
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

# Revision harshness should be measured as a shared intervention-response invariant
## Content
Revision harshness should not be assigned by family intuition, verbal analogy, or retrospective fitting to whichever environment later performs best. It should be measured by a shared intervention-response rule that applies across all admitted problems.

The shared question is:

> Once currently active support is wrong or inadequate, how costly is delayed correction?

The relevant quantity is not whether revision is allowed, but how much excess burden accumulates when revision is postponed.

## Why this form is needed
If revision harshness is left as an impressionistic label, then placement across different problem classes remains handwavy. The same number on the vector would not mean the same thing in maze, bandit, renewal, search, or control. To make the vector global, the score must be tied to one family-unspecific operation.

The right operation is a lawful delayed-revision intervention.

## Shared measurement idea
For a given problem state or local regime:
1. identify or induce a state in which current support is inadequate or contradicted,
2. compare immediate revision against revision delayed by k steps,
3. measure the excess burden accumulated during that delay,
4. normalize that excess burden into a bounded dimensionless value.

The vector value is therefore not “how hard the problem feels,” but the normalized response of the problem to delayed correction.

## Dimensionless readout
A suitable dimensionless readout is a normalized delayed-revision penalty, for example:

- excess regret per delayed step,
- excess path burden per delayed step,
- excess loss of objective per delayed step,
- normalized detour ratio,
- or another burden quantity that is already lawful for the problem through the translator.

What must remain invariant is not the raw unit but the logic:

> more sharply compounding harm under lawful revision delay means higher revision harshness.

## Why this remains global
Maze, bandit, renewal, search, and control all admit the same question even though the burden units differ. The vector therefore remains global because the intervention and normalized response are global, even if the concrete burden semantics are translator-specific.

## Directional law
If a problem is modified in a way that makes stale continuation more punishing, then revision harshness should increase. If delayed correction becomes cheaper or more reversible, then revision harshness should decrease.

This means that along controlled deformations, the vector should move monotonically enough that updated placement becomes more accurate than stale placement.

## Placement consequence
Low revision harshness should lawfully permit stronger carry-forward and earlier hardening. High revision harshness should lawfully weaken stale support authority, keep revision channels open, and delay premature collapse.

## Misuse warning
It is invalid to assign revision harshness by family label (“maze is medium”, “renewal is high”) without the shared delayed-revision logic. It is also invalid to define the vector by whichever environment later scores best. The vector must be assigned before the environment comparison, by the measurement rule itself.
