from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Tuple

@dataclass
class State:
    x: int
    y: int

class Maze1Env:
    def __init__(self, width: int = 5, height: int = 5, seed: int = 0):
        self.width = width
        self.height = height
        self.rng = __import__("random").Random(seed)
        self.reset()

    def reset(self) -> State:
        self.state = State(0, 0)
        return self.state

    def step(self, action: str) -> Tuple[State, float, bool, Dict[str, Any]]:
        x, y = self.state.x, self.state.y
        if action == "up":    y = max(0, y - 1)
        if action == "down":  y = min(self.height - 1, y + 1)
        if action == "left":  x = max(0, x - 1)
        if action == "right": x = min(self.width - 1, x + 1)
        self.state = State(x, y)
        done = (x == self.width - 1 and y == self.height - 1)
        reward = 1.0 if done else -0.01
        info: Dict[str, Any] = {}
        return self.state, reward, done, info
