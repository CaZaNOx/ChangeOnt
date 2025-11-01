from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional
from collections import deque
import random


Coord = Tuple[int, int]


@dataclass
class GridMaze:
    """
    Deterministic 4-connected grid maze with a guaranteed path from start to goal.

    - 0 = free, 1 = wall
    - start = (0, 0)
    - goal  = (height-1, width-1)

    Generation strategy:
      1) start with an empty grid (all free)
      2) propose walls at random locations (seeded RNG), but only keep a wall
         if placing it DOES NOT disconnect start from goal (checked via BFS).
      3) wall_budget controls density; keep it modest to avoid narrow corridors.

    This is simple, reproducible, and avoids "no path" cases.
    """
    width: int
    height: int
    seed: int = 0
    wall_budget: Optional[int] = None  # if None, set to ~25% of cells (excluding start/goal)

    def __post_init__(self) -> None:
        self.start: Coord = (0, 0)
        self.goal: Coord = (self.height - 1, self.width - 1)
        self._rng = random.Random(self.seed)

        # grid[r][c] in {0,1}
        self.grid: List[List[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # choose how many walls to try to place (exclude start/goal)
        free_cells = [(r, c)
                      for r in range(self.height)
                      for c in range(self.width)
                      if (r, c) not in (self.start, self.goal)]
        self._rng.shuffle(free_cells)

        if self.wall_budget is None:
            # ~25% of all cells (rounded down), but never more than total free cells
            self.wall_budget = min(len(free_cells), max(0, (self.width * self.height) // 4))

        placed = 0
        for (r, c) in free_cells:
            if placed >= self.wall_budget:
                break
            # Tentatively place a wall and check connectivity
            if self.grid[r][c] == 0:
                self.grid[r][c] = 1
                if self._still_connected():
                    placed += 1
                else:
                    # revert; keep path alive
                    self.grid[r][c] = 0

    # ---------- basic API used by env/runner ----------

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.height and 0 <= c < self.width

    def is_wall(self, r: int, c: int) -> bool:
        return self.grid[r][c] == 1

    # ---------- helpers ----------

    def _neighbors4(self, r: int, c: int):
        yield r - 1, c
        yield r + 1, c
        yield r, c - 1
        yield r, c + 1

    def _still_connected(self) -> bool:
        """BFS from start to see if goal is reachable with current walls."""
        if self.is_wall(*self.start) or self.is_wall(*self.goal):
            return False
        q: deque[Coord] = deque([self.start])
        seen = {self.start}
        while q:
            r, c = q.popleft()
            if (r, c) == self.goal:
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

    # optional: human-readable preview
    def __str__(self) -> str:
        rows = []
        for r in range(self.height):
            line = []
            for c in range(self.width):
                if (r, c) == self.start:
                    ch = "S"
                elif (r, c) == self.goal:
                    ch = "G"
                else:
                    ch = "#" if self.grid[r][c] == 1 else "."
                line.append(ch)
            rows.append("".join(line))
        return "\n".join(rows)
