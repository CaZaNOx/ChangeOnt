# Immediate Datum → eventlets → paths

**Immediate Datum (ID).** What is minimally given to an observer is *contrast*: something-not-like-something. No global time or labels are assumed; only locally detectable differences.

## Eventlets
An **eventlet** is a minimal, observer-fixed contrast:
- $e := \langle \Delta^+, \Delta^- \rangle$ with thresholds from the observer’s own discrimination.
- No absolute time index is smuggled; order is induced by arrival of contrasts.

## Paths
A **path** is a finite sequence of eventlets $(e_0,\dots,e_n)$ with **base cost** $\delta(e_i\!\to e_{i+1}) \in \mathbb{R}_{\ge 0}$. $\delta$ encodes local prediction/effort or mismatch (e.g., Hamming on tokens, or negative log-likelihood from a simple local predictor). $\delta$ is **time-invariant**; non-stationarity enters only via gauge warping (later).

We define path concatenation $\pi\cdot\pi'$ and additive base cost
$$
\delta(\pi\cdot\pi') = \delta(\pi) + \delta(\pi') \quad\text{(monoid law)}.
$$

## Bends and tolerance
A **bend** $B_\tau$ deforms a path within tolerance $\tau$ (bounded edits, permutations, small insert/delete) while preserving re-identification at the observer’s scale. “Same identity” is the **reflexive, symmetric, transitive closure** of “within τ-bend”.

Denote $u \sim_\tau v$ if $v$ is reachable from $u$ by finitely many τ-bends; this is an equivalence relation.

## Quotient
The **quotient graph** $Q=\mathcal{E}/\sim_\tau$ maps eventlets to equivalence classes $[u]$. An edge $[u]\!\to\![v]$ exists iff the underlying representatives have been observed in succession (no topology edits are ever added by the agent). The **edge cost** on $Q$ is the **infimum-lift** of the perceived cost (see `CO_MATH.md`):
$$
c_Q([u]\!\to\![v]) = \inf_{u'\in[u],\, v'\in[v]}\; c_G(u'\!\to\! v').
$$

## Gauge (intuition)
The **gauge** $G_t(\cdot)\in[0,1]$ is an observer potential that **warps perceived costs** based on local surprise and loop value, without changing topology. It evolves by a Robbins–Monro schedule on a slower time-scale than mixing.
