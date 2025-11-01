# SpecCard — CO.K5.Logic.ThreeValued @ v0.2.0

**Scope.** 3-valued base (⊤, ⊥, ?) with Gödel t-norm; Kripke-style ◇/□/↻ on Q; collapse → classical.

## Truth tables
- Neg: ¬⊤=⊥, ¬⊥=⊤, ¬?=?.
- And: ⊤∧⊤=⊤; ⊥∧x=⊥; ?∧⊤=?; ?∧?=?.
- Or:  ⊥∨⊥=⊥; ⊤∨x=⊤; ?∨⊥=?; ?∨?=?.
- Imp: φ→ψ := (¬φ)∨ψ.

## Modalities on Q
- ◇φ at [v]: sup over reachable witness-consistent paths (discount optional).
- □φ at [v]: inf over reachable classes.
- ↻φ at [v]: holds on nodes of min-mean witness-consistent cycles through [v].

## Tests required
- test_logic: table enumerations; small Kripke model sanity; collapse case equals classical.
