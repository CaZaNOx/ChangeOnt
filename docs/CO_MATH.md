# CO_MATH — Kernel v0.2.0

This file defines the mathematical core required by the CO Kernel:
(K-1) detectability and closure on observations,
(K-2) infimum-lift with witness consistency,
(K-5) logic pointer (tables live in CO_LOGIC.md).
Everything is name-free and assumes effective finiteness.

Effective Finiteness (EF)
• Class cap N ≤ N_max (e.g., 64).
• Per-class window length W (bounded).
• Observed edge set E is finite.
• Header signals are computed on finite windows.
• No splits during a closure pass; splits happen between passes.

––––––––––––––––––––––––––––––––––––––––

SpecCard CO.K1.Identity.Rtau@v0.2 — Detectability & Bend Relation

Universe
Recent traces of representatives u, v are sequences x_{1:L}(u), x_{1:L}(v) with L ≤ W.
When lengths differ, pad with a special symbol ⌀.

Gauge Weights
A bounded sequence {w_t} ⊂ [0,1] comes from the gauge (see core/gauge/haq.py).
Let w_pad ∈ [0,1] weight padding-comparisons.

Warped Bend Distance
d^g_τ(u, v) := (1/L) * Σ_{t=1..L} ω_t * Δ(x_t(u), x_t(v)),
with ω_t = w_t when both tokens present, else w_pad,
and Δ(a, b) = 1 if a≠b else 0 (Hamming; any monotone symbol metric may be substituted).

Header Agreement
HeaderAgree(u, v) is true iff binding headers match over aligned windows:
• same collapse state,
• same density mode (if used),
• same window alignment (start/end indices).

Relation and Tolerance
R_τ(u, v) :⇔ d^g_τ(u, v) ≤ τ  and  HeaderAgree(u, v).

Notes
R_τ is reflexive and symmetric but not necessarily transitive (local weights may break triangle inequality).
We therefore take equivalence closure.

Code Reference
core/quotient/equivalence.py uses distance_fn and header_agree_fn consistent with this definition.

––––––––––––––––––––––––––––––––––––––––

SpecCard CO.K1.Identity.Closure@v0.2 — Equivalence & Deterministic Closure

Equivalence
≈ is the reflexive–symmetric–transitive closure of R_τ.

Deterministic Union-Find
Each representative’s content signature s(x) is hashed to a stable content hash h(x).
On merge, the retained root is the lexicographically smallest content hash (tie on repr),
making closure order-deterministic within a pass.

Witness Log (Mandatory)
Each accepted merge logs a line such as:
    {"pair":[u,v],"dist":0.1875,"tau":0.20,"header_hash":"...","keep":u,"drop":v,"seed":1729}

Termination (EF)
With k classes at pass start, at most k−1 unions occur.
No splits inside a pass ⇒ closure halts.

Name-Free Invariance
Evaluation metrics must not depend on class IDs.
See evaluation/invariance_test.py.

Code Reference
core/quotient/equivalence.py (UnionFind and deterministic_merge_pass).

––––––––––––––––––––––––––––––––––––––––

SpecCard CO.K2.Lift.Witness@v0.2 — Infimum-Lift on the Quotient

Perceived Base Cost
Observed edges u→v carry nonnegative perceived costs c(u→v)
(plant δ warped by gauge; clipped at 0). Kernel does not fix δ or warp; only c ≥ 0.

Lifted Edge Cost (Attained under EF)
c_Q([x]→[y]) := inf_{u∈[x], v∈[y]} c(u→v).
Under EF the infimum is a minimum attained by a witness pair (u*, v*).
We store the witness.

Witness-Consistent Path/Cycle (Guard)
A lifted cycle [C0, C1, …, Ck−1, C0] has a defined cost only if the stored witnesses chain:
v_i* = u_{i+1}* for all i modulo k.
If chaining fails, the cycle cost is undefined (rejected).
This forbids “Frankenstein” minima stitched from incompatible representatives.

Monotonicity under Merges
Enlarging [x] or [y] cannot increase c_Q([x]→[y]) (minimum over a superset weakly decreases).

Reach Preservation
Any realized base path x0→x1→…→xm induces a lifted path [x0]→…→[xm], with
Σ_i c_Q([x_i]→[x_{i+1}]) ≤ Σ_i c(x_i→x_{i+1}).

Why the Guard is Needed (Counterexample)
Without witness chaining, picking per-edge minima from different representatives
can fabricate a spurious low-cost cycle not realizable in the base graph.

Code Reference
core/quotient/infimum_lift.py (LiftedGraph with lifted_edge_cost and witness_consistent_cycle_cost).

Micro-Example
See tests/test_lift.py for a 3-class cycle where chaining fails until an additional base edge is added.

––––––––––––––––––––––––––––––––––––––––

Appendix: Logic Pointer (K-5)
CO uses strong Kleene 3-valued logic (⊤, ⊥, ?) on the quotient.
Truth tables and modal clauses live in docs/CO_LOGIC.md and are tested in tests/test_logic.py.
Classical logic is the collapse case when headers freeze identity.
