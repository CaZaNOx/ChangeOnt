# FILE: core/gauge.py
import numpy as np
from .rm import alpha_t

class Gauge:
    """Gauge G per class (float32 in [0,1])."""

    def __init__(self, n_classes: int, lam: float = 1.0, beta: float = 0.8, leak: float = 0.001):
        self.G = np.zeros((n_classes,), dtype=np.float32)
        self.lam = np.float32(lam)
        self.beta = np.float32(beta)
        self.leak = np.float32(leak)
        self.t = 0

    def update(self, idx: int, PE: float, EU: float) -> np.float32:
        """Update G[idx] using RM schedule."""
        a = alpha_t(self.t)
        g = self.G[idx] + a * (self.lam * np.float32(PE) - self.beta * np.float32(EU) - self.leak * self.G[idx])
        self.G[idx] = np.clip(g, 0.0, 1.0)
        self.t += 1
        return self.G[idx]

    @staticmethod
    def perceived_cost(delta_edge: float, g_u: float, g_v: float) -> np.float32:
        """c_G(u→v) = max(0, δ - 0.5(G(u)+G(v)))."""
        return np.float32(max(0.0, np.float32(delta_edge) - 0.5 * (np.float32(g_u) + np.float32(g_v))))
