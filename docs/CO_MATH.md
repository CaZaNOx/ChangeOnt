# CO_MATH — Mathematical Core

This document fixes the **operators, structures, and lemmas** used throughout CO.

## 1. Eventlets, Paths, and Base Cost δ

- Eventlets form a set `E` with composition `∘ : E* × E → E*` (free monoid with unit `ε`).
- Base cost `δ : E → ℝ_≥0`, extended additively to paths: `δ(ε)=0`, `δ(π∘e)=δ(π)+δ(e)`.

**Lemma 1 (Pseudo-metric on paths).**  
Define `d_δ(π,π') = |δ(π) − δ(π')|`. Then `d_δ` is a pseudo-metric (non-negativity, symmetry, triangle).  
*Sketch:* Triangle: `|δ(π)−δ(π'')| ≤ |δ(π)−δ(π')| + |δ(π')−δ(π'')|`.

## 2. Bends and τ-Equivalence

- Let `B` be a finite set of *bend moves* (local rewrites) with costs `κ: B → ℝ_≥0`.
- A bend derivation `π ⇒_B π'` has cumulative cost `≤ τ` iff sum of constituent `κ` ≤ τ.

**Definition (τ-equivalence).** `π ~_τ π'` iff `π` can be transformed to `π'` by finitely many bend moves with total cost ≤ τ.  
**Lemma 2 (Equivalence closure).** The reflexive, symmetric, transitive closure of `⇒_B^τ` yields an equivalence relation `~_τ`.  
*Sketch:* Finite-cost concatenations preserve ≤ τ budget; symmetry via reverse bends; transitivity by concatenation and subadditivity.

## 3. Quotient Q and Infimum-Lift of Edge Costs

Let `Q = Paths / ~_τ`. We only keep edges `u→v` when the transition is **observed**. For class costs:

c_Q([u]→[v]) = inf_{u'∈[u], v'∈[v]} c(u'→v')

markdown
Copy code

**Lemma 3 (Well-definedness).** If `c` is bend-congruent (local rewrites do not *increase* edge costs), then `c_Q` does not depend on class representatives.  
*Sketch:* For `u~u1` and `v~v1`, there exist zig-zags with total cost ≤ τ; by monotonicity, infima coincide.

## 4. Gauge G (Robbins–Monro) and Two-Time-Scale

Update:

G_{t+1}(u) = clip( G_t(u) + α_t ( λ·PE_t(u) − β·EU_t(u) − ρ·G_t(u) ) )

markdown
Copy code

Assumptions:
- `α_t > 0`, `∑ α_t = ∞`, `∑ α_t^2 < ∞` (e.g., `α_t=(t+c)^−γ`, `γ∈(0.5,1)`).
- `PE_t`, `EU_t` are bounded, Lipschitz in empirical frequencies, and change slower than `1/α_t` (*two-time-scale*).

**Lemma 4 (RM convergence under drift-guard).**  
If the quotient’s empirical transition operator is mixing and **drift-guard** enforces `Jaccard(Q_{t−W}, Q_t) ≤ 0.10` and sample floor `≥50`, the RM iterate tracks a stable ODE with bounded error.  
*Sketch:* Standard SA with slowly varying targets; see Robbins–Monro & Borkar two-time-scale results.

## 5. CO-Numbers (Intervals) and Operators

Let a **CO-number** be a closed interval `x = [x⁻, x⁺] ⊆ ℝ` with `x⁻ ≤ x⁺`. Define:

- Addition: `x ⊕ y = [x⁻+y⁻, x⁺+y⁺]`
- Scalar mult (s≥0): `s ⊙ x = [s·x⁻, s·x⁺]`
- Order (⊑): `x ⊑ y` iff `x⁻ ≥ y⁻` and `x⁺ ≤ y⁺` (reverse inclusion ⇒ “more precise”).
- Collapse to ℝ when `width(x)=x⁺−x⁻ ≤ ε_collapse`.

**Lemma 5 (Distributivity conditions).**  
`⊙` distributes over `⊕` when scalar signs are fixed; interval widening breaks exact ring laws (expected). Classical arithmetic is recovered in the collapse limit `width→0`.

## 6. CO-Quantale (Sketch)

We use a **cost quantale** `(V, ⊕, ⊤, ⊗, ⊥)`:
- `⊕` = infimum-like combine (min or interval-min); unit `⊤` as ∞-like top.
- `⊗` = path composition (additive in classical case; interval-sum here); unit `⊥` as 0-like.
- Monotone residuation holds under bounded noise and bend-congruence.

**Axioms block (operational):**
1. `(V, ⊕)` is commutative idempotent monoid.
2. `(V, ⊗)` is monoid; `⊗` distributes over arbitrary `⊕`.
3. Monotone: `a⊑b ⇒ a⊕c ⊑ b⊕c` and `a⊗c ⊑ b⊗c`.

## 7. CO-Metrics

- Bend-distance on classes: `D([u],[v]) = inf_{u'∈[u], v'∈[v]} δ_path(u'↝v')` subject to τ-congruence.
- Gauge-warped edge: `c_G(u→v) = max(0, δ(u→v) − ½(G(u)+G(v)))`.

**Lemma 6 (Metric conditions).**  
If bends satisfy triangle-like subadditivity and the quotient graph is strongly connected, `D` is a pseudo-metric on `Q`.

**Takeaway:** Classical ℝ-operators appear as **collapse limits** when interval widths shrink and drift is negligible.


# CO-MATH (v1)

This document fixes the math primitives and operators used across the CO core. Every definition cites its ancestor in the CO chain:

Immediate Datum → **eventlets** → **paths** → base cost **δ** → **bends (τ)** → **equivalence closure** → **quotient** **Q** → **gauge** **G** → **perceived cost** **c_G** → decisions.

---

## 0) Symbols (quick table)

- 𝟙D: Immediate Datum (the “something appears” stance).
    
- 𝔈: set of **eventlets**; an eventlet `e` is a minimal contrast outcome from 𝟙D.
    
- `x, y, …`: observable tokens labeling eventlets.
    
- `Π`: set of **paths**; a path `π = (e₁,…,e_k)` over eventlets.
    
- `δ(e→e') ∈ [0,∞)`: **base edge cost** on the pre-quotient graph `G₀ = (𝔈,E)`.
    
- `τ ≥ 0`: **bend tolerance** parameter (how much deformation we allow when re-identifying).
    
- `~_τ`: **bend-equivalence** relation on 𝔈 induced by τ (reflexive, symmetric, transitive).
    
- `[e]`: the **equivalence class** of eventlet `e` under `~_τ`.
    
- `Q = (V_Q, E_Q)`: **quotient graph**, `V_Q = 𝔈 / ~_τ`.
    
- `c_G`: **perceived (gauge-warped) cost** on edges of `Q`.
    
- `G(v) ∈ [0,1]`: **gauge** value attached to quotient node `v`.
    
- `α_t`: Robbins–Monro stepsize; `α_t = (t + c)^{-p}`, with `p ∈ (1/2, 1)`.
    
- `Jaccard(A,B)`: Jaccard similarity between edge-sets; used for **drift guard**.
    
- `ℝ̄ = ℝ ∪ {+∞}`.
    

---

## 1) Eventlets (from 𝟙D)

**Definition 1 (eventlet).** Fix an observer thresholding rule on contrasts. An **eventlet** is the outcome of a single thresholded contrast. The set 𝔈 is finite at any finite time (finitude), but extensible (spawnable) across experience.

- No global time is required; only _order_ on observed contrasts, given by their appearance.
    
- Practical representation: tokens `x ∈ Σ` emitted by the plant; the particular encoding is inessential.
    

---

## 2) Paths and base edge cost δ

**Definition 2 (path).** A **path** is a finite sequence `π = (e₁,…,e_k)` with `e_i ∈ 𝔈`. Path concatenation is `π ∘ π' = (e₁,…,e_k, e'₁,…,e'_m)`.

**Definition 3 (base edge cost).** For any ordered pair `(e,e')` observed at least once, define a nonnegative **base cost** `δ(e→e')`. Unobserved edges are absent (treated as `+∞` where an algorithm expects a number).

- **No time dependence** in `δ` itself. All adaptation happens through the gauge `G` (Sec. 5).
    

**Lemma 1 (pseudo-metric on paths).** Let `c(π)` be the sum of base costs along `π`. Then  
`d(π,π') = |c(π) − c(π')|` is a pseudo-metric on the set of same-length paths (non-negativity, symmetry, triangle inequality hold; identity-of-indiscernibles can fail).  
_Sketch:_ Follows from absolute value properties and additivity of `c(·)` along concatenations.

---

## 3) Bends and tolerance τ

**Definition 4 (bend).** A **bend** is a local rewrite of a path that replaces a contiguous block with another block whose base cost differs by at most `τ` per step (w.r.t. δ). Two eventlets `e, e'` are **bend-equivalent** (`e ~_τ e'`) if there exists a chain of bends taking a path ending in `e` to a path ending in `e'` without exceeding tolerance `τ`.

**Proposition 1 (equivalence closure).** The relation `~_τ` is an **equivalence relation** (reflexive, symmetric, transitive).  
_Sketch:_ Identity bend is reflexive; inverse bend gives symmetry; composing bend chains gives transitivity.

---

## 4) Quotient and infimum-lift

**Definition 5 (quotient graph).** Let `V_Q = 𝔈 / ~_τ`. For any observed edge `e→f`, add an edge `[e]→[f]` to `E_Q`.

**Definition 6 (infimum-lift).** Per-edge **base** cost on `Q` is the **infimum** of pre-quotient costs:

```
δ_Q([e]→[f]) = inf_{e'∈[e], f'∈[f]} δ(e'→f').
```

This is **well-defined** (independent of representative choice) and monotone under merges.

**Lemma 2 (well-definedness).** If `e₁ ~_τ e₂` and `f₁ ~_τ f₂`, then  
`inf_{u∈[e₁], v∈[f₁]} δ(u→v) = inf_{u∈[e₂], v∈[f₂]} δ(u→v)`.  
_Sketch:_ Classes `[e₁]=[e₂]`, `[f₁]=[f₂]` by Prop. 1; both sides range over the same sets.

---

## 5) Gauge and perceived cost

**Definition 7 (gauge update; Robbins–Monro).** Each quotient node `v ∈ V_Q` carries `G_t(v) ∈ [0,1]` updated by

```
G_{t+1}(v) = clip_{[0,1]}\Big(G_t(v) + α_t( λ·PE_t(v) − β·EU_t(v) ) − ρ·G_t(v)\Big),
```

with `α_t = (t+c)^{-p}, p∈(1/2,1)`, leak `ρ>0`, and weights `λ,β≥0`.

- `PE_t(v)` = (1 − Dirichlet-smoothed predictive prob of the last observation given v).
    
- `EU_t(v)` = normalized loop-advantage signal (Sec. loop/flip docs).
    
- **Two-time-scale**: choose `α_t` slower than the mixing of the quotient dynamics; include **drift guard** (Sec. 7).
    

**Definition 8 (perceived cost).** For a quotient edge `u→v`,

```
c_G(u→v) = max(0, δ_Q(u→v) − ½(G(u)+G(v))).
```

Gauge _warps_ costs; it does **not** alter topology.

---

## 6) CO-numbers and operators (collapse to ℝ)

We represent **values** as closed intervals `[a,b] ⊆ ℝ` plus an optional confidence tag `γ ∈ [0,1]`.

- Addition: `[a,b] ⊕ [c,d] = [a+c, b+d]`.
    
- Multiplication (nonnegative): `[a,b] ⊗ [c,d] = [min{ac,ad,bc,bd}, max{ac,ad,bc,bd}]`.
    
- Order: `[a,b] ≤ [c,d]` iff `b ≤ c` (strong order); overlaps are **undecided**.
    
- Collapse map: if width `b−a ≤ ε_num` and confidence `γ ≥ γ_min`, release scalar `≈ (a+b)/2`.
    

**Remark.** Classical arithmetic is recovered when interval widths shrink below thresholds; otherwise CO-ops preserve epistemic spread.

---

## 7) CO-metrics and stability

- **Bend distance** between classes: `d_τ([e],[f]) = inf cost of a τ-bend chain linking reps → reps`.
    
- **Volatility** of quotient: `V_t = 1 − Jaccard(E_Q(t−W), E_Q(t))`.
    
- **LLN stability condition:** declare stable when `V_t ≤ 0.10` for 3 consecutive windows and per-class visit count ≥ 50.
    

---

## 8) Collapse-to-classical header

When `(i)` conditional entropy `H(y|class) ≤ 0.10 bits` and `(ii)` cost variance fraction ≤ 5% over a window `W=200`, freeze quotient merges and set `G≡0` (turn off warping). Auto un-freeze if either bound is violated twice consecutively.

---

## 9) Why this is **not reducible** to classical axioms

All structure is built from **re-identification under bends** (τ), not a priori identity predicates. Classical identity appears only in the **limit** `τ→0` _and_ after LLN stabilization; prior to that, quotient + gauge induce dynamics that classical static graphs cannot capture without smuggling oracles.