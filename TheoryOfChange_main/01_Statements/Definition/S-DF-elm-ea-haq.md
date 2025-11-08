---
id: stmt.elm-ea-haq
type: DF
aliases: ["ELM.EA.HAQ"]
title: Element — EA — HAQ (History-Adaptive Gauge)
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-prm-bend-metric]]", "[[01_Statements/Definition/S-DF-prm-gauge]]", "[[01_Statements/Definition/S-DF-prm-temporal-ops]]"]
parents: ["[[01_Statements/Definition/S-DF-haq-core-family]]"]
successors: []
symbols_used: ["[[01_Statements/SYMBOLS/Alpha]]", "[[01_Statements/SYMBOLS/Gamma]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5580
flags: []
tags: [element, gauge, stabilization, "type/DF"]
---
# Element — EA — HAQ (History-Adaptive Gauge)
## Claim (formal)
Adjust local costs by history‑adapted gauge: warp(costs, α) with α tracked by EMA of holonomy defect; yields coherent aggregation and emergent curvature.

## Philosophical Translation (of formal claim)
Carry forward what you’ve learned about how things hold together, so costs reflect lived coherence.

## Philosophical Justification
Raw instantaneous costs are myopic when structures breathe and stabilize over cycles. The gauge connection Γ captures learned transport; when holonomy defect rises, it indicates loss of coherence. Updating a warp parameter α via EMA of the defect honors recency while protecting against noise (σ(ε)). Warping costs by α biases selection toward paths consistent with the learned gauge, which operationalizes “coherence has credit.” Breath cycles bound adaptation rate so HAQ neither freezes (rigidity) nor thrashes (instability).

## Derivation (Formal/Operational)
```text
α_{t+1} = (1 – β)·α_t + β·holonomy_error_t
warped_costs = costs + g(α_t, Γ)
```
where β is a forgetting/adaptation rate, and g encodes the gauge‑consistent penalty/bonus. Stability requires α within leak‑bounded ranges (see η in gauge alignment updates).

## Clarifications / Further Context
- Too large α hardens preferences and risks local minima; too small α underweights learned coherence.
- HAQ complements but does not replace principled model selection (e.g., MDL).

## Next Steps in Chain
- Jointly tune HAQ and Γ; report curvature K as a coherence diagnostic.

## Tags
#type/DF #element #gauge #stabilization #concept/math-structures



































































































<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->



































































































































































































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-haq-core-family]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-bend-metric]]; [[01_Statements/Definition/S-DF-prm-gauge]]; [[01_Statements/Definition/S-DF-prm-temporal-ops]]
<!-- END:AUTOGEN:RELATIONSHIPS -->































































































