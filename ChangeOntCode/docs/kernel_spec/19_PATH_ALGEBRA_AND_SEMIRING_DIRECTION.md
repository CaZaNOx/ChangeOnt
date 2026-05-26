# Path Algebra and Semiring Direction

**Status: exploratory / directional, not a current implementation override.**

This file may guide later formalization only after the active docs/code chain and diagnostics justify promotion.

## Status
- **Directional adoption**: yes
- **Binding constraint**: algebraic composition may guide implementation, but it must not introduce additive proxy or score rescue in the canonical CO path
- **Open design space**: exact carrier spaces, exact typed operations, and exact role-to-law mapping

## 1. Why this direction is being adopted

The continuation space handled by the CO kernel should not be reasoned about as an ordinary ring-like linear score space. The main reasons are:

- actions and realized continuations are generally not trivially invertible;
- path order matters;
- continuity, fracture, and branch creation are not the same kind of object;
- a realized path can prune or weaken unrealized alternatives;
- additive fusion has repeatedly proven stable but semantically shallow.

## 2. What is being adopted now

The project adopts the following directional doctrine:

- **choice** and **sequence** are distinct operations;
- exact additive inverses should not be assumed by default;
- residuation-like reasoning is often more appropriate than true inversion;
- typed local laws are preferred to one flat global vote law whenever experiments show additive washout.

This is compatible with semiring, quantale, and path-algebra language, but the project is not freezing one final universal algebra yet.

## 3. Practical current reading

For current implementation work, read the space this way:

- additive fusion = safe baseline for local score aggregation
- multiplicative or gated laws = candidate ways to express persistence-fracture interaction
- order-sensitive laws = candidate ways to preserve sequential asymmetry
- translator feedback = realized path event returning to kernel space

## 4. Typed roles

The first typed roles to preserve explicitly are:

- persistence / attractor
- fracture / rupture
- branching / birth
- gradient / salience
- ordering / asymmetry
- transport / gauge
- attention / precision
- constraint / mask

These roles should not be assumed commensurable in one flat linear space.

## 5. Expected result if this direction is right

The first expected win is **not** universal benchmark dominance. The first expected win is:

- less collapse of a second element when combined with a strong first element;
- clearer difference between easy stabilized regimes and harder contested regimes;
- more interpretable continuation logic for persistence, fracture, and branching.

## 6. What is not being claimed yet

The project is not yet claiming:

- that one final algebra already covers every primitive and element;
- that every role should share the same carrier and the same two operations;
- that semiring language alone guarantees better performance.

## 7. Adoption rule

Promote semiring-style behavior incrementally:

1. document the typed role;
2. verify the role is live;
3. test at least one non-additive local law;
4. keep algebraic claims separate from implementation rescue paths;
5. only then treat the typed law as candidate default.
