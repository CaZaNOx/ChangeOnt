# agents/co/logic/spread_numbers.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Spread:
    """Spread number (mu, breadth, depth)."""
    mu: float
    b: float = 0.0
    d: float = 0.0

    def __add__(self, other: "Spread") -> "Spread":
        return Spread(self.mu + other.mu, self.b + other.b, self.d + other.d)

    def mul(self, other: "Spread") -> "Spread":
        """First-order safe propagation (interval-like)."""
        mu = self.mu * other.mu
        b = abs(self.mu)*other.b + abs(other.mu)*self.b + self.b*other.b
        d = abs(self.mu)*other.d + abs(other.mu)*self.d + self.d*other.d
        return Spread(mu, b, d)

    @staticmethod
    def zero() -> "Spread": return Spread(0.0, 0.0, 0.0)
    @staticmethod
    def one() -> "Spread": return Spread(1.0, 0.0, 0.0)
