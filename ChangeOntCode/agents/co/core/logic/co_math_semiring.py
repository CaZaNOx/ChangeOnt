# agents/co/core/logic/co_math_semiring.py
from __future__ import annotations
from dataclasses import dataclass

# ---- Truth algebra (Lawvere quantale, (R>=0, >=, +, 0)) ----

def q_and(a: float, b: float) -> float:   # conjunction = max
    return max(a, b)

def q_or(a: float, b: float) -> float:    # disjunction = min
    return min(a, b)

def q_then(a: float, b: float) -> float:  # sequential = +
    return a + b

def q_imp(a: float, b: float) -> float:   # residuation
    return max(0.0, b - a)

# ---- Spread numbers (mu, breadth, depth) ----

@dataclass(frozen=True)
class Spread:
    mu: float
    b: float = 0.0
    d: float = 0.0

    def boxplus(self, other: "Spread") -> "Spread":
        return Spread(self.mu + other.mu, self.b + other.b, self.d + other.d)

    def boxtimes(self, other: "Spread") -> "Spread":
        b = abs(self.mu)*other.b + abs(other.mu)*self.b + self.b*other.b
        d = abs(self.mu)*other.d + abs(other.mu)*self.d + self.d*other.d
        return Spread(self.mu * other.mu, b, d)

    @staticmethod
    def from_scalar(x: float) -> "Spread":
        return Spread(x, 0.0, 0.0)
