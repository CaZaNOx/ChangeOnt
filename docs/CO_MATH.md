# CO Math (formal core)

This file fixes the symbols, equations, and minimal lemmas needed by the code. See `SYMBOLS.md` for a glossary.

## 1. Base objects
- Eventlets set $\mathcal{E}$; paths are finite sequences in $\mathcal{E}^*$.
- Base edge cost $\delta:\mathcal{E}\times\mathcal{E}\to\mathbb{R}_{\ge 0}$, *time-invariant*.
- Path cost: $\delta(\pi=e_0\!\to\!\dots\!\to\!e_n) := \sum_{i=0}^{n-1}\delta(e_i\!\to\!e_{i+1})$ (monoid).

## 2. Bends and equivalence
For tolerance $\tau\ge 0$, define a primitive relation $R_\tau$ (“within τ-bend”) on $\mathcal{E}$. Let $\sim_\tau$ be the **equivalence closure** of $R_\tau$ (reflexive, symmetric, transitive). We write $[u]$ for the class of $u$.

**Lemma 2.1 (Equivalence).** $\sim_\tau$ is an equivalence relation (by closure construction).  
**Lemma 2.2 (Congruence gate).** If for all edges $u\!\to\!v$ and representatives $u'\!\in\![u], v'\!\in\![v]$ the perceived costs differ by at most $\tau$ (τ-congruence), then infimum-lift below is well-defined and monotone.

## 3. Quotient graph and infimum-lift
Quotient $Q=(V,E)$ with $V=\mathcal{E}/\sim_\tau$ and 
$$
([u],[v])\in E \;\;\text{iff}\;\; \exists u'\in[u], v'\in[v] : (u'\!\to\!v') \text{ observed}.
$$

Let $G_t:\mathcal{E}\to[0,1]$ be a gauge. Define **perceived** edge cost on representatives:
$$
c_G(u\!\to\!v) := \max\!\Big(0,\;\delta(u\!\to\!v) - \tfrac{1}{2}\big(G_t(u)+G_t(v)\big)\Big).
$$

Define the **infimum-lift** on the quotient:
$$
c_Q([u]\!\to\![v]) := \inf_{u'\in[u],\, v'\in[v]} c_G(u'\!\to\!v').
$$

**Lemma 3.1 (Well-defined).** If τ-congruence holds (Lemma 2.2), the infimum exists and is independent of representative choice; $c_Q$ is lower-semicontinuous under merges.

## 4. Gauge update (Robbins–Monro)
For each class (or node) $x$ at step $t$:
$$
G_{t+1}(x) \;=\; \mathrm{clip}_{[0,1]}\!\left(G_t(x) \;+\; \alpha_t\big(\lambda\,\mathrm{PE}_t(x) \;-\; \beta\,\mathrm{EU}_t(x)\big) \;-\; \rho\,G_t(x)\right)
$$
with step size $\alpha_t = (t+50)^{-0.6}$, leak $\rho=10^{-3}$, weights $\lambda=1.0,\beta=0.8$, where:
- $\mathrm{PE}_t(x)$: 1 − predictive confidence for current observation under $x$ (Dirichlet-smoothed counts).
- $\mathrm{EU}_t(x)$: normalized “loop advantage” proxy (see §6).

**Lemma 4.1 (Two-time-scale).** If $\sum_t \alpha_t = \infty$, $\sum_t \alpha_t^2 < \infty$, and mixing on $Q$ is faster than the RM schedule (drift guard below), then empirical frequencies on $Q$ converge (weak LLN on quotients).

## 5. Collapse-to-classical header
Over a rolling window $W=200$, compute:
- conditional entropy $H(y\mid [x]) \le 0.10$ bits,
- variance ratio $\mathrm{var}(c_G)/(\lvert \mathbb{E}[c_G]\rvert+10^{-6}) \le 0.05$.

If both hold, **freeze** the gauge/merges (no topology edits anyway) and use a simple classical solver; auto **un-freeze** when either bound is breached twice consecutively.

## 6. Loop score, flips, and debt
Let $C_{\text{stay}}$ = min-mean cycle cost through current class (Karp≤24; fallback Johnson≤32/256; early-stop after 64 non-improving).  
Let $C_{\text{leave}}$ = cheapest outward hop after within-loop travel (myopic surrogate defined on $Q$ only).  
Define loop score:
$$
s_t \;=\; \frac{C_{\text{leave}} - C_{\text{stay}}}{\lvert C_{\text{leave}}\rvert + \lvert C_{\text{stay}}\rvert + 10^{-6}},
\quad s^{(\mathrm{EMA})} \leftarrow 0.9\, s^{(\mathrm{EMA})} + 0.1\, s_t.
$$
Flip thresholds $\theta_{\text{on}}=0.25$, $\theta_{\text{off}}=0.15$ with cooldown 10. Execute a flip only if Monte-Carlo flip-debt (H=40, n=8 paired) predicts $\Delta\mathrm{Reg}\ge 0.05$.

## 7. Drift guard and LLN-stability
Let $Q_t$ be quotient snapshots; define volatility $V_t = 1 - \mathrm{Jaccard}(Q_{t-W}, Q_t)$ with $W=200$.  
**LLN-stable** when $V_t \le 0.10$ for 3 consecutive windows **and** per-class visit count ≥ 50.

## 8. CO numbers (interval/range)
A CO number is an interval $[a,b]$ with $a\le b$; collapse map $\kappa([a,b])=\frac{a+b}{2}$ when header deems the regime classical. Addition/multiplication are Minkowski-style; uncertainty propagates. This generalizes classical $\mathbb{R}$ as the degenerate case $a=b$.
