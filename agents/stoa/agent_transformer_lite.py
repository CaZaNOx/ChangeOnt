from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional


@dataclass
class TransformerLite:
    """
    Zero-dependency, toy 'transformer-like' memory: an n-gram table with decay.
    Not a real transformer; good enough for a cheap baseline stub.
    """
    order: int = 2
    decay: float = 0.98
    table: Dict[Tuple[int, ...], float] = field(default_factory=dict)

    def update(self, context: Tuple[int, ...], reward: float) -> None:
        if not context:
            return
        self.table[context] = self.table.get(context, 0.0) * self.decay + reward

    def score(self, context: Tuple[int, ...]) -> float:
        return self.table.get(context, 0.0)


@dataclass
class TransformerLiteAgent:
    """
    Very small context model that prefers arms with best n-gram score.
    """
    order: int = 2
    memory: TransformerLite = field(init=False)
    last_arm: Optional[int] = None
    n_arms: int = 0
    ctx: Tuple[int, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self.memory = TransformerLite(order=self.order)

    def reset(self, env_or_n: int | object) -> None:
        if isinstance(env_or_n, int):
            self.n_arms = env_or_n
        else:
            self.n_arms = int(getattr(env_or_n, "n_arms", 0))
        self.memory = TransformerLite(order=self.order)
        self.ctx = tuple()
        self.last_arm = None

    def act(self) -> int:
        # Score each arm given current context and pick the best
        best, best_s = 0, float("-inf")
        for i in range(max(1, self.n_arms)):
            s = self.memory.score(self._next_ctx(i))
            if s > best_s:
                best_s = s
                best = i
        self.last_arm = best
        self.ctx = self._next_ctx(best)
        return best

    def observe(self, reward: float) -> None:
        self.memory.update(self.ctx, float(reward))

    def _next_ctx(self, new_arm: int) -> Tuple[int, ...]:
        ctx = self.ctx + (new_arm,)
        if len(ctx) > self.order:
            ctx = ctx[-self.order:]
        return ctx
