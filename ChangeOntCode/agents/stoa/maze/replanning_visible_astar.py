from __future__ import annotations

import heapq
from typing import Dict, Any, List, Tuple, Optional

DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]
DELTA = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


def _heur(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _passable(grid: List[List[int]], h: int, w: int, r: int, c: int, optimistic_unknown: bool) -> bool:
    if not (0 <= r < h and 0 <= c < w):
        return False
    try:
        v = int(grid[r][c])
    except Exception:
        return bool(optimistic_unknown)
    if v == 0:
        return True
    if v == 1:
        return False
    return bool(optimistic_unknown)


def visible_replanning_astar_action(
    observation: Dict[str, Any],
    optimistic_unknown: bool = True,
    unknown_penalty: float = 0.0,
) -> Optional[str]:
    grid = observation.get("grid")
    pos = observation.get("pos")
    goal = observation.get("goal")
    h = int(observation.get("height", len(grid) if isinstance(grid, list) else 0) or 0)
    w = int(observation.get("width", len(grid[0]) if isinstance(grid, list) and grid else 0) or 0)
    if not (isinstance(grid, list) and isinstance(pos, (list, tuple)) and isinstance(goal, (list, tuple))):
        return None
    start = (int(pos[0]), int(pos[1]))
    target = (int(goal[0]), int(goal[1]))
    if start == target:
        return None

    openq: List[Tuple[float, float, Tuple[int, int], Any, Optional[str]]] = []
    heapq.heappush(openq, (_heur(start, target), 0.0, start, None, None))
    best_g: Dict[Tuple[int, int], float] = {start: 0.0}

    while openq:
        _f, g, cur, prev, move = heapq.heappop(openq)
        if cur == target:
            node = (_f, g, cur, prev, move)
            path: List[str] = []
            while node[3] is not None:
                path.append(node[4])
                node = node[3]
            path.reverse()
            return path[0] if path else None
        r, c = cur
        for act in DIRS:
            dr, dc = DELTA[act]
            nr, nc = r + dr, c + dc
            if not _passable(grid, h, w, nr, nc, optimistic_unknown):
                continue
            cell = int(grid[nr][nc]) if 0 <= nr < h and 0 <= nc < w else 1
            step_cost = 1.0 + (float(unknown_penalty) if cell < 0 else 0.0)
            ng = g + step_cost
            nxt = (nr, nc)
            if nxt not in best_g or ng < best_g[nxt]:
                best_g[nxt] = ng
                heapq.heappush(openq, (ng + _heur(nxt, target), ng, nxt, (_f, g, cur, prev, move), act))

    # Fallback: greedy local move over observed grid only.
    best_act: Optional[str] = None
    best_score: Optional[float] = None
    for act in DIRS:
        dr, dc = DELTA[act]
        nr, nc = start[0] + dr, start[1] + dc
        if not _passable(grid, h, w, nr, nc, optimistic_unknown):
            continue
        score = float(_heur((nr, nc), target))
        if best_score is None or score < best_score:
            best_score = score
            best_act = act
    return best_act
