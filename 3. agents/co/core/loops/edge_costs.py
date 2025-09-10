from collections import defaultdict


class TransitionModel:
    """
    Empirical token→token transition model with symmetric Dirichlet smoothing.
    Provides:
      - update(u, v): increment count for u→v
      - probs_row(u): dict v -> P(v|u)
      - prob(u, v): scalar P(v|u)
      - stay_leave_costs(u, gauge): perceived costs (c_stay, c_leave) under current gauge
    """
    def __init__(self, A: int, alpha: float = 0.3):
        self.A = int(A)
        self.alpha = float(alpha)
        # counts[from][to] -> int
        self.counts = defaultdict(lambda: defaultdict(int))

    # --- learning ---

    def update(self, u: int, v: int):
        self.counts[u][v] += 1

    # --- probabilities ---

    def probs_row(self, u: int):
        """
        Dirichlet posterior with symmetric alpha over the A outcomes.
        Returns a dict: v -> P(v|u)
        """
        row = self.counts[u]
        tot = sum(row.values())
        denom = tot + self.A * self.alpha
        p = {}
        for v in range(self.A):
            p[v] = (row.get(v, 0) + self.alpha) / denom
        return p

    def prob(self, u: int, v: int) -> float:
        """Convenience: return P(v|u) with Dirichlet smoothing."""
        return self.probs_row(u).get(v, 0.0)

    # --- perceived costs under gauge ---

    def stay_leave_costs(self, u: int, gauge: dict):
        """
        Base cost δ(u→v) = 1 − P(v|u).
        Perceived cost c_G(u→v) = δ(u→v) − 0.5*(G[u] + G[v]).
        Return (c_stay, c_leave) where 'leave' is the MIN over v != u.
        """
        G_u = float(gauge.get(u, 0.0))
        p = self.probs_row(u)

        # Stay on u -> u
        base_stay = 1.0 - p.get(u, 0.0)
        c_stay = base_stay - 0.5 * (G_u + float(gauge.get(u, 0.0)))  # = base_stay - G_u

        # Best leave over v != u
        best = None
        for v in range(self.A):
            if v == u:
                continue
            base = 1.0 - p.get(v, 0.0)
            c = base - 0.5 * (G_u + float(gauge.get(v, 0.0)))
            if (best is None) or (c < best):
                best = c

        # If u has never been seen, best could be None; fall back to uniform expectation
        if best is None:
            base = 1.0 - (1.0 / self.A)
            best = base - 0.5 * (G_u + 0.0)

        return float(c_stay), float(best)