from __future__ import annotations
from typing import List
from .grid_maze import GridSpec

def carve_simple_maze(width: int = 7, height: int = 5) -> GridSpec:
    """
    Very simple generator: empty grid with a few fixed walls and S/G.
    Deterministic; use only as a placeholder when no spec file is provided.
    """
    w, h = max(3, width), max(3, height)
    grid: List[List[str]] = [list("." * w) for _ in range(h)]
    grid[0][0] = "S"
    grid[min(1, h-1)][min(3, w-1)] = "#"
    grid[min(2, h-1)][min(2, w-1)] = "#"
    grid[min(1, h-1)][w-1] = "G"
    return GridSpec.from_grid(grid)
