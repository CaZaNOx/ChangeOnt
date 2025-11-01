# CO_LOGIC — Kernel v0.2.0

Purpose
Define the basic 3-valued logic used in CO over the quotient graph Q.
Classical logic appears as the collapse (frozen identity) case.

Truth Values
⊤ (true), ⊥ (false), ? (unknown).

Strong Kleene Truth Tables
Negation
• ¬⊤ = ⊥
• ¬⊥ = ⊤
• ¬? = ?

Conjunction (∧)
• ⊤ ∧ ⊤ = ⊤
• ⊥ ∧ x = ⊥ for any x
• ? ∧ ⊤ = ?
• ? ∧ ? = ?

Disjunction (∨)
• ⊥ ∨ ⊥ = ⊥
• ⊤ ∨ x = ⊤ for any x
• ? ∨ ⊥ = ?
• ? ∨ ? = ?

Implication (→)
A → B is defined as (¬A) ∨ B under the above tables.

Modal Semantics over Q
Worlds are quotient classes [v].
Accessibility [u] R [v] holds iff a lifted edge exists from [u] to [v].
Valuation is interval-truth from observed frequencies on Q (unknown maps to ?).

Modalities
• ◇φ holds at [u] iff ∃[v] with [u] R [v] and φ holds at [v].
• □φ holds at [u] iff ∀[v] with [u] R [v], φ holds at [v].
• ↻φ (recurrence) holds on all nodes of a min-mean cycle through [u] with respect to perceived cost.

Collapse Case
When headers freeze identity and empirical variance is low,
? vanishes for stabilized propositions and the logic collapses to classical.

Tests
See tests/test_logic.py for table sanity checks.
