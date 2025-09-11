from __future__ import annotations
from typing import List, Tuple, Dict, Callable
import collections

Move = Tuple[int, int]
DIRS: Dict[str, Move] = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

def bfs_path(start: Tuple[int, int], goal: Tuple[int, int], passable: Callable[[int, int], bool]) -> List[Tuple[int, int]]:
    """
    Pure BFS shortest path on a grid-like domain with passable(r,c) predicate.
    Returns list of coordinates from start to goal (inclusive). Empty if no path.
    """
    q = collections.deque([start])
    prev: Dict[Tuple[int, int], Tuple[int, int]] = {}
    seen = {start}
    while q:
        u = q.popleft()
        if u == goal:
            break
        r, c = u
        for dr, dc in DIRS.values():
            v = (r + dr, c + dc)
            if v not in seen and passable(*v):
                seen.add(v)
                prev[v] = u
                q.append(v)
    path: List[Tuple[int, int]] = []
    if goal in prev or goal == start:
        cur = goal
        path = [cur]
        while cur != start:
            cur = prev[cur]
            path.append(cur)
        path.reverse()
    return path
