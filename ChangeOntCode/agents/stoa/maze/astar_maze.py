# FILE: agents/stoa/astar_maze.py
from __future__ import annotations
import heapq

def astar_path(env) -> list[str]:
    start = env.start
    goal = env.goal
    moves = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    openq = [(h(start, goal), 0, start, None, None)]  # (f, g, pos, prev_node, move)
    best_g = {start: 0}

    while openq:
        f, g, pos, prev, move = heapq.heappop(openq)
        if pos == goal:
            path = []
            node = (f, g, pos, prev, move)
            while node[3] is not None:
                path.append(node[4])
                node = node[3]
            return list(reversed(path))

        r, c = pos
        for m, (dr, dc) in moves.items():
            nr, nc = r + dr, c + dc
            if not env.passable(nr, nc):
                continue
            ng = g + 1
            if (nr, nc) not in best_g or ng < best_g[(nr, nc)]:
                best_g[(nr, nc)] = ng
                heapq.heappush(openq, (ng + h((nr, nc), goal), ng, (nr, nc), (f, g, pos, prev, move), m))
    return []
