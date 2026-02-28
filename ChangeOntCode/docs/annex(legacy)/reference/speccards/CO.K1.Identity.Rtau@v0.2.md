Non-binding reference (see docs/03_BINDING_SPEC.md for binding contracts).

# SpecCard — CO.K1.Identity.Rtau @ v0.2.0

**Scope.** Detectability relation R_τ, HeaderAgree, equivalence closure ≈, deterministic (name-free) tie-break.

## Definitions
- Window length: W ∈ ℕ (default 128). Token alphabet Σ; pad symbol ⌀.
- Gauge weights g_t: Σ → [0,1]. Padding weight w_⌀ = 0.25.
- Warped bend distance on two length-W traces U, V (right-aligned, ⌀-padded):
  d^g_τ(U,V) := (1/W) * Σ_{i=1..W} ω_i · 𝟙[U_i ≠ V_i],  where ω_i = 1 − ½(g_t(U_i)+g_t(V_i)).
- HeaderAgree(u,v): same collapse state AND same density mode over their last W steps (windowed counters).
- Pre-relation: R_τ(u,v) ⇔ d^g_τ(trace_W(u), trace_W(v)) ≤ τ ∧ HeaderAgree(u,v).
- Equivalence: ≈ is the reflexive–symmetric–transitive closure of R_τ.

## Deterministic, name-free closure
- Candidate pairs: all (u,v) with R_τ true.
- Tie-break (total order): sort by ( d^g_τ ↑ , freshness ↓ , seed ↑ , content_hash(u) ⊕ content_hash(v) ↑ ).
- content_hash(x): SHA256 of (header_snapshot(x), multiset(tokens_W(x))). No class IDs.

## Invariants
- Finite working set (class cap K; window W) ⇒ closure terminates ≤ K−1 merges.
- Name-free invariance: partition depends only on traces/headers + seed, not IDs.

## Proof obligations
- Termination (finite merges).  
- Name-free determinism under the total order.

## Tests required
- test_closure: termination; order-effect counterexample without tie-break; determinism with tie-break; invariance under ID permutation.

## Constants (prereg)
W=128; K=64; τ_merge=0.20; w_⌀=0.25.
