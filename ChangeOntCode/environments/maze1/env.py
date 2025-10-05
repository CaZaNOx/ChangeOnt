# FILE: environments/maze1/env.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # only required when using spec_path

from environments.maze1.grid_maze import GridMaze  # must define in_bounds(), is_wall(), start, goal


@dataclass
class MazeSpec:
    width: int
    height: int
    seed: int = 0

    @staticmethod
    def from_params(
        p: Dict[str, Any] | None,
        default_w: int = 5,
        default_h: int = 5,
        default_seed: int = 0,
    ) -> "MazeSpec":
        p = p or {}
        return MazeSpec(
            width=int(p.get("width", default_w)),
            height=int(p.get("height", default_h)),
            seed=int(p.get("seed", default_seed)),
        )


class GridMazeEnv:
    """
    Deterministic grid maze. Rewards: -1 per step, 0 at goal.
    Episode ends upon reaching goal. Actions: 'UP','DOWN','LEFT','RIGHT'
    """
    ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT")
    DELTA = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

    def __init__(self, spec_path: Optional[str] = None, spec: Optional[MazeSpec] = None):
        if spec_path:
            if yaml is None:
                raise RuntimeError("PyYAML is required to load spec_path YAML (pip install pyyaml)")
            data = yaml.safe_load(Path(spec_path).read_text(encoding="utf-8")) or {}
            self.spec = MazeSpec.from_params(data.get("params"))
        elif spec is not None:
            self.spec = spec
        else:
            self.spec = MazeSpec(width=5, height=5, seed=0)

        self.maze = GridMaze(self.spec.width, self.spec.height, seed=self.spec.seed)
        self.start = self.maze.start
        self.goal = self.maze.goal
        self.pos: Tuple[int, int] = self.start
        self._done = False

    def reset(self, seed: Optional[int] = None) -> Tuple[int, int]:
        s = self.spec.seed if seed is None else int(seed)
        self.maze = GridMaze(self.spec.width, self.spec.height, seed=s)
        self.start = self.maze.start
        self.goal = self.maze.goal
        self.pos = self.start
        self._done = False
        return self.pos

    def passable(self, r: int, c: int) -> bool:
        return self.maze.in_bounds(r, c) and (not self.maze.is_wall(r, c))

    def step(self, action: str) -> tuple[Tuple[int, int], float, bool, dict]:
        if self._done:
            return self.pos, 0.0, True, {}

        if action not in self.ACTIONS:
            raise ValueError(f"invalid action {action}")

        dr, dc = self.DELTA[action]
        nr, nc = self.pos[0] + dr, self.pos[1] + dc

        if not self.passable(nr, nc):
            nr, nc = self.pos

        self.pos = (nr, nc)
        done = (self.pos == self.goal)
        reward = 0.0 if done else -1.0
        self._done = done
        return self.pos, reward, done, {}
