<!-- docs/stoa_bandit.md -->
# STOA: Multi-armed Bandits (Bernoulli)

**Primary references**
- Auer, Cesa-Bianchi, Fischer (2002). *Finite-time Analysis of the Multiarmed Bandit Problem*. UCB1 index:
  \[
    \text{UCB1}_a(t)=\hat{\mu}_a + \sqrt{\frac{2\ln t}{n_a(t)}}
  \]
  (Play each arm once; then argmax of index.)
- Garivier & Cappé (2011). *KL-UCB*. For Bernoulli arms, dominates UCB1 regrets in practice.
- Lai & Robbins (1985). Asymptotic lower bound: regret ≥ \(\sum_{a\ne a^\*}\frac{\ln T}{\mathrm{KL}(p_a\Vert p^\*)}\).

**Instances & expectations**
- Bernoulli probs `[0.1, 0.2, 0.8]`, horizon 2000.
- UCB1 regret grows ≈ \(C \sum_{a\ne a^\*} \frac{\ln T}{\Delta_a}\) with moderate C; best-arm pull fraction → 1.

**Acceptance**
- Regret monotone nondecreasing.
- Best-arm pull fraction ≥ 0.95 by end.
- (If KL-UCB is present) cumulative regret ≤ UCB1 for ≥ 90% of checkpoints.

**Pitfalls**
- Failing to pull each arm once.
- Using t=rounds per arm rather than global t in \(\ln t\).
- Logging cumulative regret incorrectly (must use means from config, not observed rewards).
