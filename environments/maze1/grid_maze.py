from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

Grid = List[List[str]]  # 'S','G','.' (free), '#'(wall)

@dataclass
class GridSpec:
    grid: Grid
    start: Tuple[int, int]
    goal: Tuple[int, int]

    @classmethod
    def from_grid(cls, grid: Grid) -> "GridSpec":
        sr = sc = gr = gc = -1
        for r, row in enumerate(grid):
            for c, ch in enumerate(row):
                if ch == "S":
                    sr, sc = r, c
                elif ch == "G":
                    gr, gc = r, c
        if sr < 0 or gr < 0:
            raise ValueError("GridSpec: grid must contain 'S' and 'G'")
        return cls(grid=grid, start=(sr, sc), goal=(gr, gc))

    @classmethod
    def tiny_default(cls) -> "GridSpec":
        # 5x7 toy
        rows = [
            list("S..#..."),
            list("..##..G"),
            list("..#...."),
            list("..#...."),
            list("......."),
        ]
        return cls.from_grid(rows)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])

    def passable(self, r: int, c: int) -> bool:
        return self.in_bounds(r, c) and self.grid[r][c] != "#"
