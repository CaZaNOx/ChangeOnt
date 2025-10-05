# ---- simple STOA agents (inline, deterministic tie-breaks) ----

class UCB1Agent:
    def __init__(self, n_arms: int):
        self.n = n_arms
        self.counts = [0] * n_arms
        self.values = [0.0] * n_arms
        self.t = 0

    def select(self) -> int:
        # play each arm once first
        for a in range(self.n):
            if self.counts[a] == 0:
                return a
        import math
        self.t += 1
        ucb_vals = [
            self.values[a] + (2.0 * math.log(self.t) / self.counts[a]) ** 0.5
            for a in range(self.n)
        ]
        best = max(ucb_vals)
        for a in range(self.n):
            if ucb_vals[a] == best:
                return a
        return 0

    def update(self, a: int, r: float) -> None:
        self.counts[a] += 1
        n = self.counts[a]
        q = self.values[a]
        self.values[a] = q + (r - q) / n


class EpsilonGreedyAgent:
    def __init__(self, n_arms: int, epsilon: float = 0.1, seed: int = 0):
        from random import Random
        self.n = n_arms
        self.eps = float(epsilon)
        self.counts = [0] * n_arms
        self.values = [0.0] * n_arms
        self.rng = Random(seed)

    def select(self) -> int:
        if self.rng.random() < self.eps:
            return self.rng.randrange(self.n)
        best = max(self.values)
        for a in range(self.n):
            if self.values[a] == best:
                return a
        return 0

    def update(self, a: int, r: float) -> None:
        self.counts[a] += 1
        n = self.counts[a]
        q = self.values[a]
        self.values[a] = q + (r - q) / n