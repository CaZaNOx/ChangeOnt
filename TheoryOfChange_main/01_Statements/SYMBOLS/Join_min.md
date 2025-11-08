sym: "⊕"
name: Join (min)
scope: logic/quantale
status: stable
related: ["⊗", "≈"]
tags: ["symbol/Join", "status/stable", "scope/logic"]
---
# ⊕ — Join (min)

Definition (formal):
In CO quantale logic, ⊕ denotes the join operation implemented as pointwise minimum over evidence/cost functions: (e₁ ⊕ e₂)(x) = min(e₁(x), e₂(x)).

## Math
```math
(e_1 \oplus e_2)(x) = \min\{ e_1(x), e_2(x) \}
```

## Example
- Aggregating alternative explanations keeps the least costly one.

## Related
- [[01_Statements/SYMBOLS/Compose_tensor]] (⊗) — composition (inf‑convolution)
- [[01_Statements/SYMBOLS/Approx]] (≈)

## Philosophical Translation
“Or” keeps the easiest way.

## Clarifications / Further Context
- Used in: [[01_Statements/Definition/S-DF-quantale-logic]], [[01_Statements/Derivation/S-DR-quantale-evidence-composition]].



































































<!-- BEGIN:AUTOGEN:USED_IN -->
## Used In
- [[01_Statements/Definition/S-DF-quantale-logic]]
- [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]
- [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]
- [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:USED_IN -->

































































