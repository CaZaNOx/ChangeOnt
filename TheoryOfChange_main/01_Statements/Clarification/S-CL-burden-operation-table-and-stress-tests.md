---
id: stmt.burden-operation-table-and-stress-tests
type: CL
aliases:
- S-CL-burden-operation-table-and-stress-tests
- BurdenOperationTable
- BurdenStressTests
- BurdenCounterexamples
title: Burden operation table and stress tests
concepts:
- '[[02_Concepts/C-change-trace-invariants]]'
dependencies:
- '[[01_Statements/Derivation/S-DR-burden-as-anchored-operative-tension.md]]'
- '[[01_Statements/Clarification/S-CL-public-facts-vs-policy-advice.md]]'
parents:
- '[[01_Statements/Derivation/S-DR-burden-as-anchored-operative-tension.md]]'
successors:
- '[[../ChangeOntCode/docs/kernel_spec/84_BURDEN_OPERATION_ALGEBRA.md]]'
symbols_used: []
flags:
- requires-toy-invariant-tests-before-code-claim
tags:
- layer/foundations
- domain/operational
- type/CL
- concept/burden
- concept/kernel-bridge
- status/canonical-scaffold
status: canonical-scaffold
---
# Burden operation table and stress tests

## Purpose
This file turns the concept of burden as anchored operative tension into an operation table with examples and counterexamples. It is meant to prevent burden from collapsing into generic cost, uncertainty, or domain labels.

It incorporates the field-asymmetry clarification:

```text
burden = continuation-relevant de-centering in a changing relational field
```

So the table now tracks not only magnitude, but also direction, coupling, barrier, basin, visibility, and threshold status.

## Operation table

| Operation | What changes? | What is preserved? | Burden type? | Visibility? | Branch identity effect | Relation effect |
|---|---|---|---|---|---|---|
| carry | Burden remains active | Continuation condition remains live | persists | unchanged or slowly worsens | branch may persist as debt-carrying | can create proximity/dependency |
| amplify | Magnitude, urgency, gradient, or criticality increases | Type and pressured condition persist | persists | may become more visible | branch may become less collapse-ready | increases relief/recursion pressure |
| expose | Hidden/latent burden becomes field-visible | Underlying burden may persist | persists or splits | increases | can split a branch or alter signature | creates evidence/hiddenness relation |
| mask/postpone | Apparent urgency lowers while residual remains | Underlying burden remains | persists | decreases or lags | branch may falsely appear stable | dangerous false-collapse risk |
| relieve | Residual requirement reduces | Continuation condition preserved | persists but lower | often clearer | preserves branch while reducing debt | relief relation |
| cancel | Condition making burden active is removed/reset | May preserve higher-level task, not local branch | terminated or replaced | usually explicit | may end one branch and start/reset another | cancellation relation |
| transfer | Carrier/scope changes | Type persists | persists | may shift | branch relation changes | dependency/proximity shifts |
| transform | Residual requirement changes form | Higher-level continuity may persist | changes | often increases temporarily | pressure signature changes | can generate new relations |
| absorb/buffer | Incoming tension is routed/averaged without becoming operative burden | Continuation condition remains centered | none or bounded | often low | stabilizes branch identity | shielding / stability relation |
| threshold/phase-shift | Small change reorganizes burden regime after boundary crossing | Higher-level process may persist | may persist or transform | often jumps | may split/terminate/rebase branch | critical proximity / regime-shift relation |

## Burden modifiers
A burden token should not be treated as a scalar alone. The following modifiers clarify why the same amount of change can behave differently in different contexts.

| Modifier | Meaning | Failure if omitted |
|---|---|---|
| scale | level at which tension is evaluated | every micro-change falsely becomes burden |
| coupling | whether tension affects the active anchor | remote/nonoperative changes pollute the field |
| direction | what transformation would reduce/express/escape burden | burden becomes undirected badness |
| gradient | how strongly pressure changes across nearby configurations | weak drift and strong pull are confused |
| barrier | difficulty of reaching relief/cancellation | burden relief is mistaken for accessible relief |
| basin/curvature | stability, metastability, overclosure, underclosure | stable and stuck states are conflated |
| history/momentum | retained direction from prior unfolding | branch identity loses path dependence |
| threshold status | below-threshold, accumulating, critical, phase-shifted | gradual and discontinuous burden changes are conflated |

## Stress-test examples by family

### Maintenance

| Situation | Burden reading | Operation |
|---|---|---|
| RUN while healthy | ordinary tensions are buffered by current operating regime | absorb/buffer or carry minimal burden |
| RUN while degraded | degradation pressure remains while local reward may continue | carry / amplify |
| INSPECT under hidden health | hiddenness becomes visible; may reveal degradation | expose |
| high reward despite degradation | local support masks degradation debt | mask/postpone |
| REPAIR | degradation burden is reduced while machine-continuation is preserved | relieve |
| REPLACE | previous state-class burden is reset/canceled; may create resource/restart burden | cancel + possible transform |
| sudden failure threshold | accumulated burden crosses phase boundary | threshold/phase-shift |

### Maze

| Situation | Burden reading | Operation |
|---|---|---|
| open flat corridor | local route tensions are low/buffered | carry minimal burden |
| blocked corridor discovered | hidden topology burden becomes visible obstruction burden | expose / transform |
| continue toward blocked route | topological obstruction burden is carried/amplified | carry / amplify |
| detour | route burden shifts into path-length or commitment burden | transfer |
| wall opened or route bypassed | obstruction condition ceases to matter | cancel or relieve depending on preservation |
| many equivalent routes | differences lose continuation relevance | quotient |
| many non-equivalent chokepoints | unresolved topology remains operative | grey / recursion pressure |

### Bandit

| Situation | Burden reading | Operation |
|---|---|---|
| exploit current supported option with unsampled alternatives | uncertainty/coverage burden remains | carry / mask |
| sample an arm | uncertainty burden for that arm/class reduces | relieve/expose |
| sampling reveals poor arm | hiddenness transforms into exclusion/rivalry relation | expose / transform |
| all arms sufficiently equivalent under task tolerance | uncertainty differences become nonoperative | quotient / collapse |
| high immediate reward with unknown alternatives | local success may buffer or mask uncertainty depending on regime | absorb/buffer or mask |

### Renewal

| Situation | Burden reading | Operation |
|---|---|---|
| run through stable phase | phase burden low | carry bounded burden |
| run past degradation point | cycle/degradation burden amplifies | amplify |
| wait until favorable phase | phase burden may relieve if alignment improves | relieve |
| reset/renew | accumulated cycle-state burden cancels/reset-transforms | cancel / transform |
| phase hidden or ambiguous | hiddenness burden controls collapse-readiness | expose / preserve grey |
| threshold crossing | one step moves regime from stable to failing | threshold/phase-shift |

## Adversarial counterexamples

### Low cost, high burden
A locally cheap action may postpone hidden degradation. If burden equals immediate cost, this case is misread. Correct reading: cost is low while continuation burden increases.

### High cost, low burden
An expensive reset may cancel accumulated burden. If burden equals immediate cost, this case is misread. Correct reading: local cost is high while residual burden may drop sharply.

### Same source, different burden
A blocked door can create topological obstruction, hiddenness, and revision burden. Source identity is not burden identity.

### Different sources, same burden
Wear, shock, and overuse can all create degradation burden if the same repair/reset operation class addresses the pressured condition.

### Relief vs cancellation
Repair relieves degradation while preserving the machine-continuation. Replacement cancels or resets the prior degradation-bearing condition. Treating both as generic improvement loses relation structure.

### Masking vs relief
High immediate support can mask burden. Relief reduces the residual requirement. Masking lowers apparent pressure without reducing the real residual.

### Buffering vs masking
Buffering prevents ordinary tension from becoming operative burden while preserving the continuation. Masking hides or delays burden that remains operative. Confusing these would falsely call stable absorption a hidden debt or falsely call debt-carrying stability safe.

### Threshold change vs smooth increase
A small input may matter little below threshold and dominate after threshold crossing. If burden is treated as smooth magnitude only, phase-shift cases are misread.

### Same amount, different field position
The same increment can relieve, destabilize, or do nothing depending on closure position, coupling, barrier, and basin. Burden is relational-position dependent, not quantity dependent.

## Diagnostic rule
A burden operation is meaningful only if changing it while holding scalar candidate score fixed can change relation topology, grey preservation, quotient, recursion demand, or collapse-readiness.

If burden operations never change field behavior independently of action score, then they are not doing kernel work.

## What remains to test
Before runtime claims, create toy invariants for:

1. low-cost high-burden branch should not collapse merely because score is high;
2. relief branch should gain relation status only when it reduces same-type burden;
3. cancellation should differ from relief;
4. exposure can increase short-term burden while improving collapse legitimacy;
5. masking must not count as relief;
6. buffering must not count as masking/postponement;
7. threshold/phase-shift must be distinguishable from smooth amplification;
8. same source can produce multiple burden types;
9. different sources can produce same burden type;
10. same scalar burden magnitude but different direction/barrier/relation topology should permit different collapse outcomes.

## Tags
#type/CL #layer/foundations #domain/operational #concept/burden #concept/kernel-bridge #status/canonical-scaffold
