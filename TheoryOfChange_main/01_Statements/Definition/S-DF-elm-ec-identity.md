---
id: stmt.elm-ec-identity
type: DF
aliases: ["ELM.EC.Identity"]
title: Element — EC — Identity (closure and tracking)
concepts: ["[[02_Concepts/C-identity-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-prm-reid-kernel]]", "[[01_Statements/Definition/S-DF-prm-closure-quotient]]", "[[01_Statements/Definition/S-DF-identity-through-change]]"]
parents: ["[[01_Statements/Definition/S-DF-identity-through-change]]"]
successors: ["[[01_Statements/Definition/S-DF-ops-j4a-reid-closure]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Gamma]]", "[[01_Statements/SYMBOLS/Epsilon]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5616
flags: []
tags: [layer/operators, domain/operational, element, identity, closure, "type/DF", "concept/identity-change", "symbol/Gamma", "symbol/Epsilon"]
---
# Element — EC — Identity (closure and tracking)
## Claim (formal)
Maintain identity_ok by applying ReID kernel under ε‑closure; emit last_distance and eps_used to support stable class operations.

## Philosophical Translation (of formal claim)
Keep track of what stays the same, even when it changes a bit.

## Philosophical Justification
Identity is an auditable claim under declared similarity and closure. ReID kernels evaluate cross‑time sameness under gauge transport; ε‑closure collapses near‑duplicates into classes, ensuring operations act on kinds rather than fragile instances. This makes identity persistence explicit and inspectable across gaps, aligning with identity‑through‑change.

## Derivation (Formal/Operational)
```text
identity_ok := K_reid(x_t, x_s; Γ, ε) ≥ θ over window K
class := [x]_≈ε      # quotient under ε-identity
```
Outputs include last_distance and eps_used to explain decisions.

## Clarifications / Further Context
- Identity criteria and ε must be declared per domain and tracked over time.
- Couples to closure/OPS for stable manipulation of identity classes.

## Next Steps in Chain
- suggest: [[S-DF-ops-j4a-reid-closure]]

## Tags
#type/DF #layer/operators #domain/operational #element #identity #closure #concept/identity-change #symbol/Gamma #symbol/Epsilon

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-prm-closure-quotient]]
- [[01_Statements/Definition/S-DF-prm-reid-kernel]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Definition/S-DF-identity-through-change]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-reid-kernel]]; [[01_Statements/Definition/S-DF-prm-closure-quotient]]; [[01_Statements/Definition/S-DF-identity-through-change]]
- Successors: [[01_Statements/Definition/S-DF-ops-j4a-reid-closure]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

