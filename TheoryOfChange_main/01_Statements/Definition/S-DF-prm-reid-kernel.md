---
id: stmt.prm-reid-kernel
type: DF
aliases: ["PRM_4.ReID"]
title: Primitive — ReID kernel (cross-time same-ness under gauge)
concepts: ["[[02_Concepts/C-identity-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-similarity-operator]]", "[[01_Statements/Definition/S-DF-gauge-alignment-field]]"]
parents: ["[[01_Statements/Definition/S-DF-similarity-operator]]"]
successors: ["[[01_Statements/Definition/S-DF-prm-closure-quotient]]", "[[01_Statements/Definition/S-DF-elm-ec-identity]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Gamma]]", "[[01_Statements/SYMBOLS/Epsilon]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2544
  - path: TheoryOfChange/02_Foundations/DerChain.md:5488
flags: []
tags: [layer/formal, domain/operational, primitive, similarity, tracking, "type/DF", "concept/identity-change", "symbol/Gamma", "symbol/Epsilon", status/stable]
---
# Primitive — ReID kernel (cross-time same-ness under gauge)
## Claim (formal)
Define a kernel K_reid(x_t, x_s; Γ, ε) measuring identity across time under gauge transport and tolerance ε; supports stable tracking and closure.

## Philosophical Translation (of formal claim)
To follow a thing through change, we need a way to recognize it when it’s not exactly the same.

## Philosophical Justification
- [[S-DF-similarity-operator]] gives ≈; [[S-DF-gauge-alignment-field]] transports features so comparisons are meaningful across frames.
- Kernelizing identity with explicit Γ, ε makes tracking auditable and prevents ad-hoc sameness claims.

## Clarifications / Further Context
- Used by identity element (EC) and OPS/J4a (ReID closure).
- ε should be declared per context; Γ updates should be tracked to interpret changes in scores.

## Derivation (Formal/Logical/Mathematical)
```text
K_reid(x_t, x_s) := Sim(Transport_Γ(x_t), x_s) with threshold ε for acceptance.
```

## Next Steps in Chain
- suggest: [[S-DF-prm-closure-quotient]]
- suggest: [[S-DF-elm-ec-identity]]

## Tags
#type/DF #layer/formal #domain/operational #primitive #similarity #tracking #concept/identity-change #symbol/Gamma #symbol/Epsilon #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-ec-identity]]
- [[01_Statements/Definition/S-DF-ops-j4a-reid-closure]]
- [[01_Statements/Definition/S-DF-prm-closure-quotient]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Definition/S-DF-similarity-operator]]
- Dependencies: [[01_Statements/Definition/S-DF-similarity-operator]]; [[01_Statements/Definition/S-DF-gauge-alignment-field]]
- Successors: [[01_Statements/Definition/S-DF-prm-closure-quotient]]; [[01_Statements/Definition/S-DF-elm-ec-identity]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

