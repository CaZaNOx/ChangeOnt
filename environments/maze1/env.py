from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, List
import yaml  # type: ignore

from environments.maze1.grid_maze import GridMaze  # assumes you already have this


@dataclass
class MazeSpec:
    width: int
    height: int
    seed: int = 0


class GridMazeEnv:
    """
    Deterministic grid maze. Rewards:
      -1 per step, 0 at goal. Episode ends upon reaching goal.
    Actions: 'UP','DOWN','LEFT','RIGHT'
    """
    ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT")
    DELTA = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

    def __init__(self, spec_path: Optional[str] = None, spec: Optional[MazeSpec] = None):
        if spec_path:
            data = yaml.safe_load(Path(spec_path).read_text(encoding="utf-8")) or {}
            p = data.get("params", {})
            self.spec = MazeSpec(width=int(p.get("width", 5)),
                                 height=int(p.get("height", 5)),
                                 seed=int(p.get("seed", 0)))
        elif spec:
            self.spec = spec
        else:
            self.spec = MazeSpec(width=5, height=5, seed=0)
        self.maze = GridMaze(self.spec.width, self.spec.height, seed=self.spec.seed)
        self.start = self.maze.start
        self.goal = self.maze.goal
        self.pos = self.start
        self._done = False

    def reset(self, seed: Optional[int] = None):
        if seed is not None:
            self.maze = GridMaze(self.spec.width, self.spec.height, seed=seed)
        else:
            self.maze = GridMaze(self.spec.width, self.spec.height, seed=self.spec.seed)
        self.start = self.maze.start
        self.goal = self.maze.goal
        self.pos = self.start
        self._done = False
        return self.pos

    # used by BFS in runner
    def passable(self, r: int, c: int) -> bool:
        return self.maze.in_bounds(r, c) and not self.maze.is_wall(r, c)

    def step(self, action: str):
        if self._done:
            return self.pos, 0.0, True, {}
        if action not in self.ACTIONS:
            raise ValueError(f"invalid action {action}")

        dr, dc = self.DELTA[action]
        nr, nc = self.pos[0] + dr, self.pos[1] + dc

        # illegal moves: stay in place but still pay step cost (so BFS optimality maps to minimal steps)
        if not self.passable(nr, nc):
            nr, nc = self.pos

        self.pos = (nr, nc)
        done = (self.pos == self.goal)
        reward = 0.0 if done else -1.0
        self._done = done
        return self.pos, reward, done, {}
