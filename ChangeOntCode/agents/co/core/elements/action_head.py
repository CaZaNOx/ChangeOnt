from __future__ import annotations
from typing import Any, Dict, Optional, List, Tuple
import random
from collections import deque, defaultdict

Coord = Tuple[int, int]
_DIRS = ("UP", "DOWN", "LEFT", "RIGHT")
_DELTA = {"UP": (-1,0), "DOWN": (1,0), "LEFT": (0,-1), "RIGHT": (0,1)}
_OPPOSITE = {"UP":"DOWN","DOWN":"UP","LEFT":"RIGHT","RIGHT":"LEFT"}

class ActionHead:
    """
    Family-aware final head. Must run last.
    - Bandit: ε-greedy on online means (prefers primitive bandit_stats; safe fallback)
    - Renewal: predict-last OR internal n-gram (k >= 1)
    - Maze: greedy-to-goal with wall checks + small ε exploration (uses eps_on_cycle)
    """

    def __init__(
        self,
        seed: int = 0,
        eps_on_cycle: float = 0.10,     # used for bandit AND maze exploration
        ngram_order: int = 0,
    ) -> None:
        self.rng = random.Random(int(seed))
        self.eps = max(0.0, min(1.0, float(eps_on_cycle)))

        # bandit fallback stats
        self._counts: List[int] = []
        self._means:  List[float] = []

        # renewal n-gram
        self.k = max(0, int(ngram_order))
        self._hist = deque(maxlen=max(1, self.k))
        self._ng_counts: defaultdict[Tuple[int, ...], defaultdict[int, int]] = defaultdict(lambda: defaultdict(int))

        # maze episode-local memory to reduce oscillations
        self._ep: Optional[int] = None
        self._last_dir: Optional[str] = None
        self._last_pos: Optional[Tuple[int,int]] = None

    # ---------------- utilities ----------------

    def _ensure_arms(self, n: int) -> None:
        while len(self._counts) < n:
            self._counts.append(0)
            self._means.append(0.0)

    @staticmethod
    def _in_bounds(r: int, c: int, H: int, W: int) -> bool:
        return 0 <= r < H and 0 <= c < W

    @staticmethod
    def _manhattan(a: Coord, b: Coord) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # ---------------- hooks ----------------

    def update(
        self,
        observation: Dict[str, Any],
        primitives: Dict[str, Any],
        header: Any,
        feedback: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        fam = observation.get("family")

        # bandit: update means from last feedback (prefer primitive)
        if fam == "bandit" and isinstance(feedback, dict):
            a = feedback.get("action", None)
            r = feedback.get("reward", None)
            n_arms = int(observation.get("n_arms", 2))
            bs = primitives.get("bandit_stats")
            if isinstance(a, int) and isinstance(r, (int, float)):
                if bs is not None and hasattr(bs, "update"):
                    try:
                        bs.update(int(a), float(r), n_arms=n_arms)
                    except Exception:
                        self._bandit_update_fallback(int(a), float(r), n_arms)
                else:
                    self._bandit_update_fallback(int(a), float(r), n_arms)

        # renewal: learn n-gram on the post-step observation
        if fam == "renewal" and isinstance(feedback, dict) and self.k >= 1:
            obs_next = feedback.get("observation", None)
            if isinstance(obs_next, int):
                ctx = tuple(self._hist)
                if len(ctx) == self.k:
                    self._ng_counts[ctx][obs_next] += 1
                self._hist.append(obs_next)

        # maze: reset anti-oscillation per episode
        if fam == "maze":
            ep = observation.get("episode")
            if ep is not None and ep != self._ep:
                self._ep = ep
                self._last_dir = None
                self._last_pos = None

        return {}

    def step(
        self,
        observation: Dict[str, Any],
        primitives: Dict[str, Any],
        header: Any,
        feedback: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        fam = observation.get("family")

        # ---------------- BANDIT ----------------
        if fam == "bandit":
            n_arms = int(observation.get("n_arms", 2))
            bs = primitives.get("bandit_stats")
            if bs is not None and all(hasattr(bs, k) for k in ("means", "counts", "ensure")):
                try:
                    bs.ensure(n_arms)
                    means = list(bs.means[:n_arms])
                    counts = list(bs.counts[:n_arms])
                except Exception:
                    means, counts = self._fallback_stats(n_arms)
            else:
                means, counts = self._fallback_stats(n_arms)

            # pull each arm once
            for i in range(n_arms):
                if i >= len(counts) or counts[i] == 0:
                    return {"action": i, "co_policy": f"bandit:egreedy(eps={self.eps:.3f})"}

            # ε-greedy
            if self.rng.random() < self.eps:
                a = self.rng.randrange(n_arms)
            else:
                a = max(range(n_arms), key=lambda i: means[i])
            return {"action": a, "co_policy": f"bandit:egreedy(eps={self.eps:.3f})"}

        # ---------------- RENEWAL ---------------
        if fam == "renewal":
            a_default = int(observation.get("obs", 0))
            if self.k >= 1:
                ctx = tuple(self._hist)
                if len(ctx) == self.k and ctx in self._ng_counts and self._ng_counts[ctx]:
                    nxt = max(self._ng_counts[ctx].keys(), key=lambda s: self._ng_counts[ctx][s])
                    return {"action": int(nxt), "co_policy": f"renewal:ngram(k={self.k})"}
            if self.k > 0 and len(self._hist) < self.k:
                self._hist.append(a_default)
            return {"action": a_default, "co_policy": "renewal:predict_last"}

        # ---------------- MAZE ------------------
        if fam == "maze":
            pos  = observation.get("pos")
            goal = observation.get("goal")
            H    = observation.get("height")
            W    = observation.get("width")
            grid = observation.get("grid")

            if not (isinstance(pos, (list, tuple)) and isinstance(goal, (list, tuple))):
                # fall back to legal cycle (will be masked by runner guard anyway)
                t = int(observation.get("t", 0) or 0)
                return {"action": _DIRS[t % 4], "co_policy": "maze:cycle"}

            pr, pc = int(pos[0]), int(pos[1])
            gr, gc = int(goal[0]), int(goal[1])

            def free(nr: int, nc: int) -> bool:
                if isinstance(H, int) and isinstance(W, int):
                    if not self._in_bounds(nr, nc, H, W): return False
                if isinstance(grid, list):
                    try:
                        if grid[nr][nc] == 1: return False
                    except Exception:
                        pass
                return True

            base = self._manhattan((pr, pc), (gr, gc))
            cands: List[Tuple[int,str]] = []
            for d in _DIRS:
                dr, dc = _DELTA[d]
                nr, nc = pr + dr, pc + dc
                if not free(nr, nc): continue
                new = self._manhattan((nr, nc), (gr, gc))
                if new <= base:
                    # prefer non-backtrack if possible
                    if self._last_dir is not None and d == _OPPOSITE.get(self._last_dir):
                        cands.append((new + 1, d))  # slight penalty to immediate backtrack
                    else:
                        cands.append((new, d))

            if cands:
                cands.sort(key=lambda x: x[0])
                best_dist, best_dir = cands[0]
                # small exploration (uses eps_on_cycle) if multiple candidates
                if len(cands) > 1 and self.rng.random() < self.eps:
                    best_dir = cands[1][1]
                self._last_dir = best_dir
                self._last_pos = (pr, pc)
                return {"action": best_dir, "co_policy": "maze:greedy"}

            # no improving move: try any legal
            for d in _DIRS:
                dr, dc = _DELTA[d]
                nr, nc = pr + dr, pc + dc
                if free(nr, nc):
                    self._last_dir = d
                    self._last_pos = (pr, pc)
                    return {"action": d, "co_policy": "maze:explore"}

            # give up => cycle
            t = int(observation.get("t", 0) or 0)
            return {"action": _DIRS[t % 4], "co_policy": "maze:cycle"}

        # unknown family
        return {}

    # --------------- helpers -----------------

    def _fallback_stats(self, n_arms: int) -> Tuple[List[float], List[int]]:
        self._ensure_arms(n_arms)
        return list(self._means[:n_arms]), list(self._counts[:n_arms])

    def _bandit_update_fallback(self, a: int, r: float, n_arms: int) -> None:
        self._ensure_arms(n_arms)
        if 0 <= a < n_arms:
            self._counts[a] += 1
            n = self._counts[a]
            self._means[a] += (float(r) - self._means[a]) / float(max(1, n))

    def metrics(self) -> Dict[str, Any]:
        return {
            "head_eps": float(self.eps),
            "head_ngram_order": int(self.k),
            "head_bandit_counts": list(self._counts),
            "head_bandit_means":  list(self._means),
        }