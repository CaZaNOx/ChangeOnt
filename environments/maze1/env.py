from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any
import os

from .grid_maze import GridSpec
from .small_maze import small_spec

DIRS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
Action = str


@dataclass
class GridMazeEnv:
    """
    Deterministic grid maze.

    Exposed for agents:
      - .start: (r, c)
      - .goal: (r, c)
      - .pos:  (r, c)
      - .passable(r,c) -> bool
      - .is_done() -> bool
      - .reset(seed: Optional[int]) -> tuple[int,int]
      - .step(action: str) -> (obs=(r,c), reward: float, done: bool, info: dict)

    Notes:
      * No external dependencies; if a YAML spec is provided but PyYAML is missing,
        we fall back to a small built-in grid.
    """
    spec_path: Optional[str] = None
    step_cost: float = -1.0
    goal_reward: float = 10.0

    spec: GridSpec = field(init=False)
    start: Tuple[int, int] = field(init=False)
    goal: Tuple[int, int] = field(init=False)
    pos: Tuple[int, int] = field(init=False)
    _done: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.spec = self._load_spec(self.spec_path)
        self.start = self.spec.start
        self.goal = self.spec.goal
        self.pos = self.start
        self._done = False

    def _load_spec(self, path: Optional[str]) -> GridSpec:
        if path is None:
            return small_spec()
        if not os.path.exists(path):
            # File missing: fall back to default tiny grid
            return small_spec()
        # Try to parse a very small YAML subset if available
        try:
            import yaml  # type: ignore
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            grid = data.get("grid")
            if not grid:
                return small_spec()
            # Ensure rows are lists of single-char strings
            rows = [list(str(row)) if isinstance(row, str) else list(row) for row in grid]
            return GridSpec.from_grid(rows)
        except Exception:
            # Graceful fallback if PyYAML missing or parse fails
            return small_spec()

    # --- public API ---

    def passable(self, r: int, c: int) -> bool:
        return self.spec.passable(r, c)

    def is_done(self) -> bool:
        return self._done

    def reset(self, seed: Optional[int] = None) -> Tuple[int, int]:
        # deterministic; seed currently unused (no stochasticity)
        self.pos = self.start
        self._done = False
        return self.pos

    def step(self, action: Action) -> Tuple[Tuple[int, int], float, bool, Dict[str, Any]]:
        if self._done:
            # No-op once done; keep returning terminal state
            return self.pos, 0.0, True, {"terminal": True}

        dr, dc = DIRS.get(action, (0, 0))
        r, c = self.pos
        nr, nc = r + dr, c + dc
        if self.passable(nr, nc):
            self.pos = (nr, nc)
        reward = self.step_cost
        if self.pos == self.goal:
            self._done = True
            reward += self.goal_reward
        info: Dict[str, Any] = {}
        return self.pos, reward, self._done, info
