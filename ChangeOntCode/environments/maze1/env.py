from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
from collections import deque
import random

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
    partial_observability: bool = False
    view_radius: int = 1
    dynamic_walls: bool = False
    wall_flip_prob: float = 0.0
    max_flips_per_step: int = 1

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
            partial_observability=bool(p.get("partial_observability", False)),
            view_radius=max(0, int(p.get("view_radius", 1))),
            dynamic_walls=bool(p.get("dynamic_walls", False)),
            wall_flip_prob=float(p.get("wall_flip_prob", 0.0) or 0.0),
            max_flips_per_step=max(0, int(p.get("max_flips_per_step", 1))),
        )


class GridMazeEnv:
    """
    Grid maze with optional partial observability and optional dynamic wall flips.

    Public fairness boundary:
    - env.grid remains the *true* grid for environment transition logic.
    - get_observation() returns only the visible/discovered grid; unknown cells are -1.
    - dynamic flips are accepted only when they preserve a path from current position to goal.

    Rewards: -1 per step, 0 at goal.
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

        self._rng = random.Random(self.spec.seed)
        self.maze = GridMaze(self.spec.width, self.spec.height, seed=self.spec.seed)
        self.start = self.maze.start
        self.goal = self.maze.goal
        self.width = self.spec.width
        self.height = self.spec.height
        self.H = self.height
        self.W = self.width
        self.pos: Tuple[int, int] = self.start
        self._done = False
        self._step_count = 0
        self.grid: List[List[int]] = []
        self.observed_grid: List[List[int]] = []
        self.reset(seed=self.spec.seed)

    def reset(self, seed: Optional[int] = None) -> Tuple[int, int]:
        s = self.spec.seed if seed is None else int(seed)
        self._rng = random.Random(s)
        self.maze = GridMaze(self.spec.width, self.spec.height, seed=s)
        self.start = self.maze.start
        self.goal = self.maze.goal
        self.width = self.spec.width
        self.height = self.spec.height
        self.H = self.height
        self.W = self.width
        self.pos = self.start
        self._done = False
        self._step_count = 0
        self.grid = [[int(v) for v in row] for row in self.maze.grid]
        self.observed_grid = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        self._refresh_observation(force_full=not self.spec.partial_observability)
        return self.pos

    def passable(self, r: int, c: int) -> bool:
        return self.in_bounds(r, c) and (not self.is_wall(r, c))

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.height and 0 <= c < self.width

    def is_wall(self, r: int, c: int) -> bool:
        return bool(self.grid[r][c] == 1)

    def observed_cell(self, r: int, c: int) -> int:
        if not self.in_bounds(r, c):
            return 1
        return int(self.observed_grid[r][c])

    def get_observation_grid(self) -> List[List[int]]:
        return [[int(v) for v in row] for row in self.observed_grid]

    def get_observation(self) -> Dict[str, Any]:
        return {
            "pos": tuple(self.pos),
            "goal": tuple(self.goal),
            "grid": self.get_observation_grid(),
            "width": int(self.width),
            "height": int(self.height),
            "partial_observability": bool(self.spec.partial_observability),
            "view_radius": int(self.spec.view_radius),
            "dynamic_walls": bool(self.spec.dynamic_walls),
            "wall_flip_prob": float(self.spec.wall_flip_prob),
            "step_count": int(self._step_count),
        }

    def step(self, action: str) -> tuple[Tuple[int, int], float, bool, dict]:
        if self._done:
            return self.pos, 0.0, True, {"observation": self.get_observation(), "dynamic_events": []}

        if action not in self.ACTIONS:
            raise ValueError(f"invalid action {action}")

        dr, dc = self.DELTA[action]
        nr, nc = self.pos[0] + dr, self.pos[1] + dc

        if not self.passable(nr, nc):
            nr, nc = self.pos

        self.pos = (nr, nc)
        self._step_count += 1
        dynamic_events = self._apply_dynamic_flips() if self.spec.dynamic_walls else []
        self._refresh_observation(force_full=not self.spec.partial_observability)

        done = self.pos == self.goal
        reward = 0.0 if done else -1.0
        self._done = done
        info = {
            "observation": self.get_observation(),
            "dynamic_events": dynamic_events,
            "visible_changed": bool(dynamic_events),
        }
        return self.pos, reward, done, info

    def _refresh_observation(self, force_full: bool = False) -> None:
        if force_full:
            self.observed_grid = [[int(v) for v in row] for row in self.grid]
            return
        radius = int(max(0, self.spec.view_radius))
        pr, pc = self.pos
        for r in range(max(0, pr - radius), min(self.height, pr + radius + 1)):
            for c in range(max(0, pc - radius), min(self.width, pc + radius + 1)):
                self.observed_grid[r][c] = int(self.grid[r][c])
        self.observed_grid[self.pos[0]][self.pos[1]] = 0
        self.observed_grid[self.goal[0]][self.goal[1]] = 0

    def _neighbors4(self, r: int, c: int):
        yield r - 1, c
        yield r + 1, c
        yield r, c - 1
        yield r, c + 1

    def _path_exists_from(self, start: Tuple[int, int], goal: Tuple[int, int]) -> bool:
        if not self.in_bounds(*start) or not self.in_bounds(*goal):
            return False
        if self.is_wall(*start) or self.is_wall(*goal):
            return False
        q = deque([start])
        seen = {start}
        while q:
            r, c = q.popleft()
            if (r, c) == goal:
                return True
            for nr, nc in self._neighbors4(r, c):
                if not self.in_bounds(nr, nc):
                    continue
                if self.is_wall(nr, nc):
                    continue
                if (nr, nc) in seen:
                    continue
                seen.add((nr, nc))
                q.append((nr, nc))
        return False

    def _flip_admissible(self, r: int, c: int) -> bool:
        if (r, c) in (self.start, self.goal, self.pos):
            return False
        old = int(self.grid[r][c])
        self.grid[r][c] = 0 if old == 1 else 1
        ok = self._path_exists_from(self.pos, self.goal)
        if not ok:
            self.grid[r][c] = old
            return False
        return True

    def _apply_dynamic_flips(self) -> List[Dict[str, Any]]:
        if self.spec.wall_flip_prob <= 0.0 or self.spec.max_flips_per_step <= 0:
            return []
        events: List[Dict[str, Any]] = []
        for _ in range(int(self.spec.max_flips_per_step)):
            if self._rng.random() >= float(self.spec.wall_flip_prob):
                continue
            cells = [
                (r, c)
                for r in range(self.height)
                for c in range(self.width)
                if (r, c) not in (self.start, self.goal, self.pos)
            ]
            self._rng.shuffle(cells)
            for r, c in cells:
                before = int(self.grid[r][c])
                if not self._flip_admissible(r, c):
                    continue
                after = int(self.grid[r][c])
                if not self.spec.partial_observability:
                    self.observed_grid[r][c] = after
                else:
                    pr, pc = self.pos
                    if abs(r - pr) <= self.spec.view_radius and abs(c - pc) <= self.spec.view_radius:
                        self.observed_grid[r][c] = after
                events.append({"cell": (int(r), int(c)), "before": before, "after": after})
                break
        return events
