# FND0 — Immediate Datum (ID)

**Claim (ID):** What is immediately given is **change**: a *felt contrast*, not a static object nor an external clock.
We formalize the minimal observation as an **eventlet**.

## Eventlets

- An **eventlet** `e` is the smallest contrast detectable by an observer `A` under a sensitivity threshold `θ_A`.
- Notation: `e = ⟦Δ⟧_A`, where `Δ` is a just-noticeable difference (JND) in the observer’s channel.
- **No global time**: eventlets are not time-stamped; they are *ordered only by composition*.

### Observer dependence
- Sensitivity `θ_A` and resolution define which contrasts exist for `A`. Different observers induce different eventlet algebras.
- Invariance under **coarsening**: increasing `θ_A` can only merge eventlets; it cannot create finer ones.

## Paths

A **path** `π = e₁ ∘ e₂ ∘ … ∘ e_k` is a composable sequence of eventlets.
Composition `∘` is associative; the empty path `ε` is the neutral element.

### Base cost δ

We assign a **base cost** `δ(e)` to each eventlet (e.g., predictive effort or local discrepancy), and extend to paths by:

- `δ(ε) = 0`
- `δ(π ∘ e) = δ(π) + δ(e)`  (additivity over composition)

`δ` is a pseudo-length: distinct eventlets may share cost; different paths may have equal accumulated cost.

## Bends and tolerance τ

Two paths `π, π'` are **τ-bend equivalent** if one can be deformed into the other via a finite sequence of *local rewrites* (“bends”)
whose cumulative cost does not exceed `τ`. This induces a **tolerance relation**.

- Generate a relation `~_τ` from bend moves and declare the **equivalence closure** (reflexive, symmetric, transitive).
- **Identity = re-identifiability under τ**: the “same” arises as a class under tolerated bends.

## Quotient Q

Let `Q = Paths / ~_τ`. Elements `[π] ∈ Q` are *equivalence classes* of paths. Edges in `Q` are **observed transitions** between classes.
The **infimum-lift** defines edge costs on classes:

c_Q([u]→[v]) = inf_{u'∈[u], v'∈[v]} c(u'→v')


(See CO_MATH for well-definedness conditions.)

## Gauge G (Robbins–Monro)

A **gauge** `G` is an attention-like potential updated via Robbins–Monro SA with two signals:
- `PE` = prediction error (misfit on recent class-conditional emission)
- `EU` = advantage of staying in current loop vs leaving

Update (clipped to [0,1]):

G_{t+1}(u) = clip( G_t(u) + α_t ( λ·PE_t(u) − β·EU_t(u) − ρ·G_t(u) ) )


with step-size `α_t = (t+c)^−γ`, `γ ∈ (0.5, 1)`, leak `ρ>0`.

## Headers (collapse, density, meta-flip, complex turn)

Headers *schedule* behavior but **never change topology** nor base cost `δ`. Collapse recognizes classical regimes (low entropy/variance).
Density measures branching vs revisitation to choose exploration mode; meta-flip flips depth↔breadth; complex turn makes smooth policy rotations.

**Bottom line:** From ID alone we derive eventlets→paths→bends→quotient→gauge. Classical behavior is a **limit** (not the base).

