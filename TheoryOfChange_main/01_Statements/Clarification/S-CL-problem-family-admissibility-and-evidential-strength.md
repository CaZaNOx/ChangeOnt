---
id: stmt.problem-family-admissibility-and-evidential-strength
type: CL
aliases:
- S-CL-problem-family-admissibility-and-evidential-strength
- ProblemFamilyAdmissibility
- COTestValidity
title: Problem-family admissibility and evidential strength
concepts:
- '[[02_Concepts/C-boundary]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
- '[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]'
parents:
- '[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]'
successors:
- '[[../ChangeOntCode/docs/kernel_spec/83_PROBLEM_FAMILY_ADMISSIBILITY_AND_TEST_VALIDITY.md]]'
symbols_used: []
flags:
- benchmark-validity
tags:
- layer/foundations
- domain/operational
- type/CL
- concept/problem-family
- concept/evidence
- concept/kernel-bridge
status: canonical-scaffold
---
# Problem-family admissibility and evidential strength

## Claim
In principle, any bounded problem family is admissible for CO if it can be expressed as a bounded local unfolding with public boundary, legal transformations, task anchor, observation channels, admissible/prohibited transitions, and fair baselines.

Admissibility is not the same as evidential strength.

## Admissibility conditions
A family is admissible when it can specify:

- local boundary;
- legal transition grammar;
- public / hidden distinction where relevant;
- task anchor;
- observation channels;
- admissible and prohibited transformations;
- public effect facts or raw facts from which effects can be derived;
- parity-honest baselines.

A classical-looking family is not excluded. A static family is not excluded. A simple family is not excluded.

## Evidential strength
A family gives stronger evidence when it stresses a claimed CO mechanism:

- branch identity across actions;
- relation topology;
- quotient/equivalence;
- relief/cancellation;
- grey preservation;
- earned collapse;
- shape-regime modulation;
- public-boundary discipline;
- cross-family mechanism reuse.

A family gives weaker evidence if it can be solved by one-step scoring and does not force the kernel to use its claimed continuation-field mechanisms.

## Anti-cherry-picking rule
The paper must say what each family tests before using results. “It performs well on several tasks” is weaker than “this task stresses quotienting, this task stresses grey preservation, this task stresses public hiddenness, and this task stresses branch identity.”

## Tags
#type/CL #layer/foundations #domain/operational #concept/problem-family #concept/evidence #concept/kernel-bridge #status/canonical-scaffold
