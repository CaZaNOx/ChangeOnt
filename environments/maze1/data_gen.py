from __future__ import annotations
from typing import Iterator, Tuple

def random_walk_actions(steps: int, seed: int = 0) -> Iterator[str]:
    import random
    rng = random.Random(seed)
    actions = ["up","down","left","right"]
    for _ in range(steps):
        yield rng.choice(actions)
