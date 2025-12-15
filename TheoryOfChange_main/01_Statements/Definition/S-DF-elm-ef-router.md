---
id: stmt.elm-ef-router
type: DF
aliases: ["ELM.EF.Router"]
title: Element — EF — Router (dynamic + math policy)
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-prm-bend-metric]]", "[[01_Statements/Definition/S-DF-prm-mdl-compressibility]]", "[[01_Statements/Definition/S-DF-prm-temporal-ops]]", "[[01_Statements/Definition/S-DF-quantale-logic]]", "[[01_Statements/Definition/S-DF-elm-ee-compressibility]]"]
parents: ["[[01_Statements/Definition/S-DF-prm-bend-metric]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5628
flags: []
tags: [layer/operators, domain/operational, element, routing, policy, "type/DF", "concept/math-structures"]
---
# Element — EF — Router (dynamic + math policy)
## Claim (formal)
Route between dynamic regimes and math contexts using bend/volatility, compressibility, and EMA history; emit dyn and math_context.

## Philosophical Translation (of formal claim)
Choose how to think — and how to move — based on what the world is doing now.

## Philosophical Justification
Different regimes demand different tools: high volatility favors robust dynamics; high compressibility supports aggressive consolidation; breath phase informs pacing. A router makes these choices explicit and auditable rather than implicit in ad‑hoc heuristics.

## Derivation (Formal/Operational)
```text
dyn := f(volatility_proxy, loopiness, phase)
math_context := g(compressibility, quantale_ready)
```
Emits dyn and math_context as explicit downstream inputs.

## Clarifications / Further Context
- Keep routing simple and explainable; avoid oscillations between regimes.
- Incorporate robustness_pred from compressibility ([[S-DF-elm-ee-compressibility]]) to bias toward stable modes.

## Next Steps in Chain
- Evaluate regime switches with hysteresis; log decisions for audit.

## Tags
#type/DF #layer/operators #domain/operational #element #routing #policy #concept/math-structures

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-ee-compressibility]]
- [[01_Statements/Definition/S-DF-prm-temporal-ops]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-prm-bend-metric]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-bend-metric]]; [[01_Statements/Definition/S-DF-prm-mdl-compressibility]]; [[01_Statements/Definition/S-DF-prm-temporal-ops]]; [[01_Statements/Definition/S-DF-quantale-logic]]; [[01_Statements/Definition/S-DF-elm-ee-compressibility]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

