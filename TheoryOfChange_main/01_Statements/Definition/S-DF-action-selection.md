---
id: stmt.action-selection
type: DF
aliases: ["FND_22.ActionSelection"]
title: Action selection / decision dynamics
concepts: ["[[02_Concepts/C-recursive-truth]]"]
dependencies: ["[[01_Statements/Definition/S-DF-attention-focus]]", "[[01_Statements/Definition/S-DF-evaluation-surface]]", "[[01_Statements/Definition/S-DF-actor]]"]
parents: ["[[01_Statements/Definition/S-DF-attention-focus]]", "[[01_Statements/Definition/S-DF-actor]]"]
successors: ["[[01_Statements/Corollary/S-CR-action-influences-expectation]]", "[[01_Statements/Corollary/S-CR-recursive-expectation]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:1760
flags: []
tags: [layer/validation, domain/operational, stable, recursion, "type/DF", "concept/recursive-truth"]
---
# Action selection / decision dynamics
## Claim (formal)
Actions are chosen by descending evaluation surfaces under breath‑modulated attention, subject to identity invariants and SE budgets; selections are written to memory traces to update future choices.

## Philosophical Translation (of formal claim)
We act by following what continues to work under repeated checking, given what we can currently pay attention to and still remain ourselves.

## Philosophical Justification
- [[S-DF-attention-focus]] narrows the space of options; [[S-DF-evaluation-surface]] scores them.
- [[S-DF-actor]] provides the reflexive locus that can commit to a choice and remember it.
- Identity/SE constraints prune options that would destabilize the subject; thus feasible actions are constrained descents, not arbitrary jumps.

## Explanation (informal)
Action selection is “hill‑walking” on a landscape of viability. Focus shines a light on a patch, the actor picks a step that lowers cost without breaking itself, and the memory of the step updates the landscape for the next move.

## Derivation (Philosophical)
- Limited RTV + invariants ⇒ must prioritize; attention provides weights.
- Weighted options + evaluation algebra ⇒ pick minimal cost move.
- Memory writes ⇒ recursive expectation adjustments (corollaries).

## Derivation (Formal/Logical/Mathematical)
```text
Choose a ∈ LocalReach s.t.
  a = argmin_x w(x) ⊗ Eval(x)
  subject to SE(x) ≥ 0 and Invariants(x) respected.
Record(a) updates Eval for next breath.
```

## Proofs/Corollaries References
- corollary: [[S-CR-action-influences-expectation]]
- corollary: [[S-CR-recursive-expectation]]

## Clarifications / Further Context
- Breath coupling sets step size; exploration/exploitation trade-off encoded via attention weights.
- Failures (SE < 0) trigger reweighting or broadened attention windows.

## Next Steps in Chain
- suggest: [[S-CR-action-influences-expectation]]
- suggest: [[S-CR-recursive-expectation]]

## Tags
#type/DF #layer/validation #domain/operational #concept/recursive-truth #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Corollary/S-CR-action-influences-expectation]]
- [[01_Statements/Definition/S-DF-actor]]
- [[01_Statements/Definition/S-DF-attention-focus]]
- [[01_Statements/Definition/S-DF-evaluation-surface]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-recursive-truth]]
- Parents: [[01_Statements/Definition/S-DF-attention-focus]]; [[01_Statements/Definition/S-DF-actor]]
- Dependencies: [[01_Statements/Definition/S-DF-attention-focus]]; [[01_Statements/Definition/S-DF-evaluation-surface]]; [[01_Statements/Definition/S-DF-actor]]
- Successors: [[01_Statements/Corollary/S-CR-action-influences-expectation]]; [[01_Statements/Corollary/S-CR-recursive-expectation]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

