---
id: stmt.generic-problem-contract
type: DF
aliases:
- GenericProblemContract
- PlugAndPlayProblemBoundary
title: Generic problem contract — new problems may provide declarative structure, not strategy
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-recursive-truth]]'
dependencies:
- '[[01_Statements/Definition/S-DF-stabilization-target-scope]]'
- '[[01_Statements/Definition/S-DF-descriptor-guided-predictive-deformation]]'
- '[[01_Statements/Definition/S-DF-hdr-meta]]'
- '[[01_Statements/Definition/S-DF-hdr-common]]'
parents:
- '[[01_Statements/Definition/S-DF-stabilization-target-scope]]'
successors:
- '[[01_Statements/Definition/S-DF-elm-ec-identity]]'
- '[[01_Statements/Definition/S-DF-candidate-surface]]'
- '[[01_Statements/Definition/S-DF-change-benchmark-protocol]]'
symbols_used: []
sources:
- path: chat/2026-04-08 clarification that new problems must be pluggable by declaring their regime/observability/task/constraint structure, not by adding family-shaped behavioral logic
- path: ChangeOntCode/docs/kernel_spec/16_TRANSLATOR_BOUNDARY_CONTRACT.md
- path: ChangeOntCode/docs/kernel_spec/77_PUBLIC_BURDEN_EFFECT_SCHEMA.md
flags: []
tags:
- layer/operators
- domain/operational
- type/DF
- status/stable
- bridge
- boundary
- plug-and-play
chain_status_band: bridge-provisional
chain_status_note: The need for a generic declarative problem boundary follows from the anti-finetuning doctrine and stabilization-scope distinction, but the exact runtime schema remains a bridge-level formalization.
---
# Generic problem contract — new problems may provide declarative structure, not strategy
## Claim (formal)
A new problem may enter the kernel only by declaring parity-honest problem structure in a generic contract. That contract may describe admissible actions, observation channels, task anchor, hard constraints, soft costs, regime anchors, mutable factors, and horizon-relative profiles such as observability, reversibility, and rate of change. It must not provide benchmark-specific policy, near-solution semantics, or strategic role labels.

## Philosophical Translation (of formal claim)
A kernel that needs a new inner doctrine every time a new task appears is not yet general. But a kernel also cannot act in a void. So the problem may tell the kernel what kind of field it is acting in, as long as it only declares structure and not strategy.

## Philosophical Justification
[[01_Statements/Definition/S-DF-stabilization-target-scope]] already establishes that what is being stabilized differs in kind. [[01_Statements/Definition/S-DF-descriptor-guided-predictive-deformation]] then requires that regime claims predict configuration advantage under controlled deformation. [[01_Statements/Definition/S-DF-hdr-meta]] and [[01_Statements/Definition/S-DF-hdr-common]] together already assume that local action unfolds inside inherited structural conditions. These commitments jointly require a disciplined boundary. A new problem must be allowed to declare what is fixed, what is mutable, what is visible, and what counts as success or constraint; otherwise no honest action is possible. But if the boundary also declares who the incumbent is, what support mode is appropriate, or how rivalry should be solved, then the family has effectively smuggled in policy and the kernel has failed the plug-and-play criterion.

## Explanation (informal)
Chess may tell the kernel that legal moves are fixed, piece identities are horizon-fixed, and the task anchor is checkmate under tournament rules. A bandit may tell the kernel that there are discrete admissible actions, reward feedback is visible only through outcomes, and the action identities are fixed while latent value relations remain uncertain. Both are legitimate problem descriptions. Neither may tell the kernel which line is strategically mature or which support law already won.

## Derivation (Philosophical)
- Any actionable problem supplies some structural conditions: what can be done, what can be seen, and what is forbidden.
- A general kernel must therefore accept declarative problem structure.
- But a problem-specific strategy is not the same thing as a problem-specific structure.
- If the boundary provides strategic or near-solution semantics, the family is solving the problem under the name of translation.
- Therefore the boundary must be limited to a generic declarative problem contract and forbid policy leakage.

## Derivation (Formal/Logical/Mathematical)
```text
Allowed contract kinds:
  actions
  observation_channels
  task_anchor
  hard_constraints
  soft_costs
  regime_anchors
  mutable_factors
  timescale_profile
  observability_profile
  reversibility_profile

Forbidden boundary content:
  incumbent/challenger labels
  promotion scores
  support-stage labels
  family-specific strategy hints
  near-final action rankings disguised as contract fields
```

## Clarifications / Further Context
- This file does **not** claim that the current repository already satisfies the contract fully.
- It states the anti-finetuning boundary condition that a serious plug-and-play kernel must satisfy.
- The vocabulary inside a contract field may still vary across families, but the field *types* must remain generic and declarative.
- This file therefore licenses adapter-level problem description while forbidding adapter-level policy.

## Next Steps in Chain
- suggest: [[01_Statements/Definition/S-DF-change-benchmark-protocol]]
- suggest: [[01_Statements/Definition/S-DF-elm-ec-identity]]
- suggest: [[01_Statements/Definition/S-DF-candidate-surface]]

## Active-chain status
Band: bridge-provisional.
The anti-finetuning doctrine strongly supports a declarative problem boundary, but the exact runtime schema and enforcement remain bridge-level work rather than a closed first-layer theorem.

## Tags
#type/DF #layer/operators #domain/operational #bridge #boundary #plug-and-play #status/stable
