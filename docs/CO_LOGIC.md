# CO_LOGIC — Logic under Change

CO-logic assigns truth to *paths/classes under tolerance τ*, not to timeless propositions.

## 1. Valuation

Let `⟦φ⟧( [π], τ ) ∈ [0,1]` be the degree that formula `φ` holds on class `[π]` at tolerance `τ`.

- **Atomic** `p`: `⟦p⟧([π],τ)` is the empirical frequency that `p` holds on traversals of `[π]` within τ.
- **Negation**: `⟦¬φ⟧ = 1 − ⟦φ⟧` (default; interval semantics in uncertain regimes).
- **Conjunction**: `⟦φ∧ψ⟧ = min(⟦φ⟧, ⟦ψ⟧)` (Gödel t-norm; aligns with monotone costs).

## 2. Modalities over Q

- **Reachability** `◇φ`: `⟦◇φ⟧([π],τ) = sup_{[π]→…→[π']}( decay·⟦φ⟧([π'],τ) )` with decay from cumulative cost.
- **Invariance** `□φ`: `⟦□φ⟧ = inf_{reachable} ⟦φ⟧`.
- **Recurrence** `↻φ`: truth is the asymptotic visitation frequency of states satisfying `φ` on minimal-cost loops.

## 3. Classical Collapse

**Proposition.** If (i) drift-guard holds and LLN stabilizes empirical frequencies, and (ii) `τ→0` so bend-equivalence collapses to identity, then `⟦φ⟧∈{0,1}` and CO-logic reduces to classical propositional logic on `Q`.  
*Sketch:* Frequences stabilize; tolerance vanishes; reachability/invariance become crisp over a fixed graph.

## 4. Inference (sequent sketch)

- From `φ` and `φ→ψ` (interpreted as `⟦φ⟧≤⟦ψ⟧`), infer `ψ`.  
- Under collapse, this reproduces classical modus ponens.

**Note:** We prefer **interval truth** in practice; collapse is used only in demonstrably classical regimes.


# CO-LOGIC (v1)

CO-logic reasons about statements whose truth depends on **change** and on the **quotient** `Q` derived from bend-equivalence.

---

## 1) Valuations over paths/classes

Let `W` be the set of **worlds** = quotient nodes `V_Q`. An **accessibility** relation `R_τ ⊆ W×W` is given by the observed edges in `Q` whose perceived cost `c_G(u→v)` is finite (edge exists).

A **valuation** at time `t` is a map `ν_t: Prop → 𝕋`, where `𝕋 = {⊥, ⊤, 𝕌}` (false, true, undecided) or interval-truth `[l,u] ⊆ [0,1]` for quantitative forms. Valuations are **empirical**: they are computed from observed transitions only (no plant oracles).

**Collapse:** When the header triggers (H ≤ 0.10 bits and var ≤ 5% with LLN), `𝕋` collapses to `{⊥, ⊤}` (no undecided) and probability intervals collapse to scalars.

---

## 2) Syntax

Formulas:

- Atomic `p` (about present class / local predicates).
    
- Boolean: `¬φ`, `φ ∧ ψ`, `φ ∨ ψ`, `φ → ψ`.
    
- Modal: `◇φ` (“reachable within τ-bends”), `□φ` (“all τ-consistent unfoldings”), `↻φ` (“recurs on the loop”).
    

---

## 3) Semantics (Kripke-style on Q)

At a world `w ∈ W` and time `t`:

- `w ⊨_t p` iff `ν_t(p)` evaluates to **⊤** at `w`. (Data-driven.)
    
- `w ⊨_t ¬φ` iff not(`w ⊨_t φ`) with three-valued De Morgan rules.
    
- `w ⊨_t φ ∧ ψ` iff min-truth of both; `∨` via max-truth; `→` via `¬φ ∨ ψ`.
    
- `w ⊨_t ◇φ` iff ∃ `v` with `(w,v) ∈ R_τ` and `v ⊨_t φ`.
    
- `w ⊨_t □φ` iff ∀ `v` with `(w,v) ∈ R_τ`, `v ⊨_t φ`.
    
- `w ⊨_t ↻φ` iff along the current min-mean cycle through `w`, `φ` holds at every node in the cycle.
    

**Note.** `R_τ` is empirical: only observed quotient edges are allowed. No hidden step indices, lap counts, or renewal flags.

---

## 4) Inference rules and collapse-to-classical

We use sequent-style rules sound for three-valued Kleene logic with modalities:

- **Kleene-MP:** from `φ` and `φ→ψ`, infer `ψ` **only if** both premises are ⊤ (not 𝕌).
    
- **K-axiom (□):** `□(φ→ψ) → (□φ → □ψ)`.
    
- **Duality:** `◇φ ≡ ¬□¬φ`.
    

**Collapse theorem (prooflet).** If τ→0 and LLN stability holds (edge set & valuations no longer drift), then valuations become classical (`𝕌` disappears) and standard modal logic K is recovered.  
_Reason:_ τ→0 kills bend-induced merges; with LLN stability, empirical frequencies converge, so undecideds vanish under the sample floor/CI thresholds.

---

## 5) Practical reading

- Use `◇` when you want “possibly reachable given what’s been observed” (no oracles).
    
- Use `↻` to assert properties of current stable loops (e.g., “if we flip, we will return to class `c`”).
    
- When the collapse header is on, treat all formulas classically (CO just defers to the stabilized special case).
