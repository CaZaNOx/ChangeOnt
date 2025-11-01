from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from environments.maze1.env import GridMazeEnv



DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]
DELTA = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


def bfs_path(env: GridMazeEnv) -> List[str]:
    """Return a shortest action sequence from start to goal using BFS on the grid graph."""
    start = env.start
    goal = env.goal
    from collections import deque
    q = deque([start])
    prev: Dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}
    prev_act: Dict[Tuple[int, int], str | None] = {start: None}

    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            break
        for act in DIRS:
            dr, dc = DELTA[act]
            nr, nc = r + dr, c + dc
            if not env.passable(nr, nc):
                continue
            if (nr, nc) in prev:
                continue
            prev[(nr, nc)] = (r, c)
            prev_act[(nr, nc)] = act
            q.append((nr, nc))

    # reconstruct
    if goal not in prev:
        return []  # no path
    path_actions: List[str] = []
    cur = goal
    while cur != start:
        act = prev_act[cur]
        assert act is not None
        path_actions.append(act)
        cur = prev[cur]  # type: ignore
        assert cur is not None
    path_actions.reverse()
    return path_actions