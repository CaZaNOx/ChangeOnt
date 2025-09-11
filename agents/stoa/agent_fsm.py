from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import math
import collections


# -----------------------------
# A) BFS agent for grid mazes
# -----------------------------

Move = Tuple[int, int]
DIRS: Dict[str, Move] = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
DIR_LIST: List[str] = ["UP", "DOWN", "LEFT", "RIGHT"]


def _neighbors(pos: Tuple[int, int], passable) -> List[Tuple[int, int]]:
    r, c = pos
    out: List[Tuple[int, int]] = []
    for dr, dc in DIRS.values():
        nr, nc = r + dr, c + dc
        if passable(nr, nc):
            out.append((nr, nc))
    return out


def _reconstruct_path(prev: Dict[Tuple[int, int], Tuple[int, int]],
                      start: Tuple[int, int],
                      goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    if goal not in prev and goal != start:
        return []
    path = [goal]
    cur = goal
    while cur != start:
        cur = prev[cur]
        path.append(cur)
    path.reverse()
    return path


@dataclass
class BFSAgent:
    """
    Deterministic shortest-path agent for unweighted grid mazes.

    Expected env adapter provides:
      - .start: (r, c)
      - .goal: (r, c)
      - .passable(r, c): bool
      - .is_done(): bool
      - .pos (current position)
      - .step(action: str) -> (obs, reward, done, info)
    """
    planned: List[Tuple[int, int]] = field(default_factory=list)

    def reset(self, env) -> None:
        self.planned.clear()
        # Pre-compute shortest path from start to goal
        start = tuple(env.start)  # type: ignore[arg-type]
        goal = tuple(env.goal)    # type: ignore[arg-type]
        q: collections.deque[Tuple[int, int]] = collections.deque([start])
        prev: Dict[Tuple[int, int], Tuple[int, int]] = {}
        seen = {start}
        while q:
            u = q.popleft()
            if u == goal:
                break
            for v in _neighbors(u, env.passable):
                if v not in seen:
                    seen.add(v)
                    prev[v] = u
                    q.append(v)
        path = _reconstruct_path(prev, start, goal)
        self.planned = path

    def act(self, env) -> str:
        if getattr(env, "is_done", lambda: False)():
            return "UP"  # won't be used
        cur = tuple(env.pos)  # type: ignore[arg-type]
        # Find next waypoint on path
        if not self.planned:
            return "UP"  # fallback noop
        # If current position equals planned[0], step to planned[1]
        try:
            idx = self.planned.index(cur)
        except ValueError:
            # If we got off-path, re-plan
            self.reset(env)
            idx = 0
        nxt_idx = min(idx + 1, len(self.planned) - 1)
        nxt = self.planned[nxt_idx]
        dr = nxt[0] - cur[0]
        dc = nxt[1] - cur[1]
        for name, d in DIRS.items():
            if d == (dr, dc):
                return name
        # Should not happen on grid; fallback:
        return "UP"

    def observe(self, reward: float, info: Optional[dict] = None) -> None:
        # BFS is deterministic; no learning.
        pass


# -----------------------------
# B) UCB1 agent for K-armed bandits
# -----------------------------

@dataclass
class UCB1Agent:
    """
    Textbook UCB1 for stationary Bernoulli bandits.
    API expected by bandit runner:
      - reset(n_arms: int) or reset(env) with env.n_arms
      - act() -> arm index
      - observe(reward: float)  # reward for last pulled arm
    """
    counts: List[int] = field(default_factory=list)
    means: List[float] = field(default_factory=list)
    t: int = 0
    last_arm: Optional[int] = None

    def reset(self, env_or_n: int | object) -> None:
        if isinstance(env_or_n, int):
            n = env_or_n
        else:
            n = int(getattr(env_or_n, "n_arms", 0))
            if n <= 0:
                raise ValueError("UCB1Agent.reset: could not infer number of arms")
        self.counts = [0] * n
        self.means = [0.0] * n
        self.t = 0
        self.last_arm = None

    def _ucb_score(self, i: int) -> float:
        if self.counts[i] == 0:
            return math.inf
        # Auer et al. (2002) style: mu + sqrt(2 ln t / n_i)
        return self.means[i] + math.sqrt(2.0 * math.log(max(1, self.t))) / math.sqrt(self.counts[i])

    def act(self) -> int:
        self.t += 1
        # Pull each arm at least once
        for i, c in enumerate(self.counts):
            if c == 0:
                self.last_arm = i
                return i
        # Otherwise pick argmax UCB
        best = 0
        best_score = -1.0
        for i in range(len(self.counts)):
            s = self._ucb_score(i)
            if s > best_score:
                best = i
                best_score = s
        self.last_arm = best
        return best

    def observe(self, reward: float) -> None:
        if self.last_arm is None:
            return
        i = self.last_arm
        self.counts[i] += 1
        # online mean update
        n = self.counts[i]
        self.means[i] += (reward - self.means[i]) / n
