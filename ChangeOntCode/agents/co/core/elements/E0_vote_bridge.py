# agents/co/core/elements/E0_vote_bridge.py
from __future__ import annotations
from typing import Any, Dict, List, Optional

def _bandit_votes(obs: Dict[str, Any], prims: Dict[str, Any]) -> List[Dict[str, Any]]:
    n = int(obs.get("n_arms", 2))
    means = [0.0]*n
    bs = prims.get("bandit_stats")
    if bs is not None and all(hasattr(bs, k) for k in ("ensure","means")):
        try:
            bs.ensure(n)
            means = list(bs.means[:n])
        except Exception:
            pass
    mmin = min(means) if means else 0.0
    wts = [max(0.0, m - mmin) for m in means]
    if sum(wts) <= 1e-12:
        wts = [1.0]*n
    return [{"action": i, "weight": float(w), "source": "vote_bridge/bandit"} for i, w in enumerate(wts)]

def _renewal_votes(obs: Dict[str, Any], prims: Dict[str, Any]) -> List[Dict[str, Any]]:
    a = int(obs.get("obs", 0))
    return [{"action": a, "weight": 1.0, "source": "vote_bridge/renewal"}]

def _maze_votes(obs: Dict[str, Any]) -> List[Dict[str, Any]]:
    pos = obs.get("pos"); goal = obs.get("goal")
    H = obs.get("height"); W = obs.get("width"); grid = obs.get("grid")
    if not (isinstance(pos,(list,tuple)) and isinstance(goal,(list,tuple))):
        return []
    pr,pc = int(pos[0]), int(pos[1]); gr,gc = int(goal[0]), int(goal[1])
    dirs = ("UP","DOWN","LEFT","RIGHT")
    deltas = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}
    def inb(r,c): 
        if H is None or W is None: return True
        try: return 0 <= r < int(H) and 0 <= c < int(W)
        except Exception: return True
    def free(r,c):
        if not inb(r,c): return False
        if grid is None: return True
        try: return int(grid[r][c]) == 0
        except Exception: return True
    d0 = abs(pr-gr)+abs(pc-gc)
    votes: List[Dict[str, Any]] = []
    for d in dirs:
        dr,dc = deltas[d]; nr,nc = pr+dr, pc+dc
        if not free(nr,nc): continue
        d1 = abs(nr-gr)+abs(nc-gc)
        improve = float(d0 - d1)  # >0 is better
        w = improve if improve > 0.0 else 0.1
        votes.append({"action": d, "weight": w, "source": "vote_bridge/maze"})
    return votes

class E0_VoteBridge:
    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any],
               header: Any, feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        return {}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any],
             header: Any, feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        fam = str(observation.get("family","")).lower()
        bus = primitives.get("co_bus")
        if bus is None or not hasattr(bus, "push"):
            return {}
        try:
            votes: List[Dict[str, Any]] = []
            if fam == "bandit":
                votes = _bandit_votes(observation, primitives)
                for v in votes: bus.push("bandit", v["action"], weight=v["weight"], source=v.get("source"))
            elif fam == "renewal":
                votes = _renewal_votes(observation, primitives)
                for v in votes: bus.push("renewal", v["action"], weight=v["weight"], source=v.get("source"))
            elif fam == "maze":
                votes = _maze_votes(observation)
                for v in votes: bus.push("maze", v["action"], weight=v["weight"], source=v.get("source"))
            # tiny metric to confirm publishing
            try:
                size = bus.size(fam)
            except Exception:
                size = 0

            return {"vote_bridge_published": int(len(votes)), "vote_bridge_bus_size": int(size)}
        except Exception:
            return {}

    def metrics(self) -> Dict[str, Any]:
        return {}