# agents/co/core/elements/action_head.py
from __future__ import annotations
from typing import Any, Dict, Optional, List, Tuple
from collections import defaultdict
import random

try:
    from agents.co.integration.translators import get_translator_for_family
except Exception:
    def get_translator_for_family(_fam: str):
        return None

try:
    from agents.co.core.combinators.C_fuse import C_Fuse
except Exception:
    class C_Fuse:  # type: ignore
        def __init__(self, method: str = "add", tau: float = 1.0): pass
        def fuse(self, scores_list):
            out: Dict[Any, float] = {}
            try:
                for item in scores_list:
                    if isinstance(item, tuple) and len(item) == 2:
                        d, w = item
                        for k, v in d.items():
                            out[k] = out.get(k, 0.0) + float(v) * float(w)
                    else:
                        for k, v in item.items():
                            out[k] = out.get(k, 0.0) + float(v)
                return out
            except Exception:
                return out

try:
    from agents.co.core.contracts.signals import normalize_scores
except Exception:
    def normalize_scores(scores: Dict[Any, float]) -> Dict[Any, float]:
        if not scores:
            return {}
        m = max(abs(float(v)) for v in scores.values())
        if m <= 1e-12:
            return dict(scores)
        return {k: float(v) / m for k, v in scores.items()}

Coord = Tuple[int, int]
OPPOSITE = {"UP":"DOWN","DOWN":"UP","LEFT":"RIGHT","RIGHT":"LEFT"}

class ActionHead:
    def __init__(
        self,
        seed: int = 0,
        eps_on_cycle: float = 0.10,
        ngram_order: int = 0,
        greedy_explore_bias: float = 0.05,
        fuse_method: str = "add",
        fuse_tau: float = 1.0,
        prefer_bus_if_present: bool = True,
        use_translator: bool = True,
        blend_mode: str = "mix",
        co_weight_override: Optional[float] = None,
        classic_planner: str = "greedy",
    ) -> None:
        self.rng = random.Random(int(seed))
        self.eps = float(eps_on_cycle)
        self.k = max(0, int(ngram_order))
        self._maze_explore = float(greedy_explore_bias)
        self._fuser = C_Fuse(method=fuse_method, tau=fuse_tau)
        self.prefer_bus = bool(prefer_bus_if_present)
        self.use_translator = bool(use_translator)
        self.blend_mode = str(blend_mode)
        self.co_weight_override = co_weight_override
        self.classic_planner = str(classic_planner).lower()

        self._counts: List[int] = []
        self._means: List[float] = []

        # new: minimal memory for oscillation breaking
        self._last_action: Optional[str] = None
        self._last_pos: Optional[Tuple[int,int]] = None
        self._prev_pos: Optional[Tuple[int,int]] = None  # pos at t-2

    def _ensure_arms(self, n: int) -> None:
        while len(self._counts) < n:
            self._counts.append(0); self._means.append(0.0)

    def _default_action_space(self, family: str, observation: Dict[str, Any]) -> List[Any]:
        if family == "bandit":
            return list(range(int(observation.get("n_arms", 2))))
        if family == "maze":
            return ["UP","DOWN","LEFT","RIGHT"]
        if family == "renewal":
            A = int(observation.get("A", 0))
            return list(range(A)) if A > 0 else []
        return []

    def _bus_scores(self, primitives: Dict[str, Any], family: str) -> tuple[Dict[Any, float], int]:
        bus = primitives.get("co_bus", None)
        if bus is None or not hasattr(bus, "drain"):
            return {}, 0
        try:
            votes = bus.drain(family)
        except Exception:
            votes = []
        agg: Dict[Any, float] = defaultdict(float)
        for v in votes:
            a = v.get("action", None)
            w = float(v.get("weight", 0.0) or 0.0)
            if a is not None and w > 0.0:
                agg[a] += w
        return dict(agg), len(votes)

    def _classical_scores(self, family: str, obs: Dict[str, Any], primitives: Dict[str, Any]) -> Dict[Any, float]:
        if family == "bandit":
            n = int(obs.get("n_arms", 2))
            bs = primitives.get("bandit_stats")
            if bs is not None and all(hasattr(bs, k) for k in ("ensure","means","counts")):
                try:
                    bs.ensure(n); means = list(bs.means[:n])
                except Exception:
                    self._ensure_arms(n); means = list(self._means[:n])
            else:
                self._ensure_arms(n); means = list(self._means[:n])
            if any(means):
                lo, hi = min(means), max(means); rng = (hi - lo) if (hi > lo) else 1.0
                return {i: (means[i]-lo)/rng for i in range(n)}
            return {i: 0.0 for i in range(n)}

    # --- renewal
        if family == "renewal":
            a = int(obs.get("obs", 0))
            return {a: 1.0}

    # --- maze
        if family == "maze":
            pos = obs.get("pos"); goal = obs.get("goal")
            H = obs.get("height"); W = obs.get("width"); grid = obs.get("grid")
            if not (isinstance(pos,(list,tuple)) and isinstance(goal,(list,tuple))):
                return {}
            pr,pc = int(pos[0]), int(pos[1]); gr,gc = int(goal[0]), int(goal[1])
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
            scores: Dict[str, float] = {}
            for d,(dr,dc) in deltas.items():
                nr, nc = pr+dr, pc+dc
                if not free(nr,nc): continue
                d1 = abs(nr-gr)+abs(nc-gc)
                improve = d0 - d1
                scores[d] = 1.0 if (improve > 0.0) else 0.2
            return scores
        return {}

    # --- helpers for maze lookahead and free check
    def _maze_free(self, r: int, c: int, grid, H, W) -> bool:
        if H is not None and W is not None:
            if not (0 <= r < int(H) and 0 <= c < int(W)):
                return False
        if grid is None: return True
        try: return int(grid[r][c]) == 0
        except Exception: return True

    def _maze_lookahead_degree(self, r: int, c: int, move: str, grid, H, W) -> int:
        deltas = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}
        opp = OPPOSITE.get(move)
        nr, nc = r + deltas[move][0], c + deltas[move][1]
        deg = 0
        for d,(dr,dc) in deltas.items():
            if d == opp: continue
            if self._maze_free(nr+dr, nc+dc, grid, H, W): deg += 1
        return deg

    def _fuse_safe(self, parts: List[Any]) -> Dict[Any, float]:
        form1 = []
        for p in parts:
            if isinstance(p, tuple) and len(p) == 2: form1.append(p)
            else: form1.append((p, 1.0))
        try:
            return self._fuser.fuse(form1) or {}
        except Exception:
            pass
        form2 = [p[0] if (isinstance(p, tuple) and len(p) == 2) else p for p in parts]
        try:
            return self._fuser.fuse(form2) or {}
        except Exception:
            out: Dict[Any, float] = {}
            for p in parts:
                d = p[0] if (isinstance(p, tuple) and len(p) == 2) else p
                try:
                    for k, v in d.items():
                        out[k] = out.get(k, 0.0) + float(v)
                except Exception:
                    pass
            return out

    # ----------------- hooks -----------------
    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        fam = str(observation.get("family", "")).lower()
        if fam == "bandit" and isinstance(feedback, dict):
            a = feedback.get("action", None); r = feedback.get("reward", None)
            n_arms = int(observation.get("n_arms", 2)); bs = primitives.get("bandit_stats")
            if isinstance(a, int) and isinstance(r, (int, float)):
                if bs is not None and hasattr(bs, "update"):
                    try: bs.update(int(a), float(r), n_arms=n_arms)
                    except Exception:
                        self._ensure_arms(n_arms); self._counts[a] += 1
                        n = max(1, self._counts[a]); self._means[a] += (float(r) - self._means[a]) / float(n)
                else:
                    self._ensure_arms(n_arms); self._counts[a] += 1
                    n = max(1, self._counts[a]); self._means[a] += (float(r) - self._means[a]) / float(n)
        return {}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            family = str(observation.get("family", "")).lower()
            actions = observation.get("action_space") or self._default_action_space(family, observation)

            # weights
            if self.co_weight_override is not None:
                co_w = float(max(0.0, min(1.0, self.co_weight_override)))
            else:
                try: co_w = float(getattr(header, "state", {}).get("co_weight", 1.0))
                except Exception: co_w = 1.0
            if self.blend_mode == "co_only": co_w = 1.0
            elif self.blend_mode == "classic_only": co_w = 0.0
            classic_w = 1.0 - co_w

            print(f"[HEAD] family={family} blend={self.blend_mode} co_w={co_w:.3f} classic_w={classic_w:.3f}")

            # CO path
            co_sources: List[str] = []
            bus_scores, n_votes = ({}, 0)
            if self.prefer_bus:
                bus_scores, n_votes = self._bus_scores(primitives, family)
                if bus_scores: co_sources.append("bus")
            print(f"[HEAD] bus_scores={bus_scores} n_votes={n_votes}")

            trans_scores: Dict[Any, float] = {}
            translator_mask: set = set()
            if self.use_translator:
                translator = get_translator_for_family(family)
                if translator is not None:
                    tcfg = {"eps": self.eps, "maze_explore": self._maze_explore, "k": self.k}
                    try:
                        trans_scores, translator_mask, _info = translator(observation, header, primitives, {}, tcfg)
                    except Exception:
                        trans_scores, translator_mask = {}, set()
                    if trans_scores: co_sources.append("translator")
            print(f"[HEAD] trans_scores={trans_scores} mask={translator_mask}")

            co_scores: Dict[Any, float] = {}
            parts: List[Any] = []
            if bus_scores:   parts.append((bus_scores, 1.0))
            if trans_scores: parts.append((trans_scores, 1.0))
            if parts:
                co_scores = self._fuse_safe(parts)
                co_scores = normalize_scores(co_scores)
            print(f"[HEAD] co_scores (pre-mask)={co_scores}")

            # apply translator mask
            if translator_mask:
                for a in list(co_scores.keys()):
                    if a in translator_mask:
                        co_scores.pop(a, None)
            print(f"[HEAD] co_scores (post-mask)={co_scores}")

            # classical
            classical = self._classical_scores(family, observation, primitives)
            if classical:
                classical = normalize_scores(classical)
                co_sources.append("classical")
            print(f"[HEAD] classical={classical}")

            # final scores
            domain = list(actions) if actions else list(set(list(co_scores.keys()) + list(classical.keys())))
            final_scores: Dict[Any, float] = {}
            if domain:
                for a in domain:
                    cs = co_scores.get(a, 0.0); ks = classical.get(a, 0.0)
                    final_scores[a] = co_w * cs + classic_w * ks
                    print(f"[HEAD] score[{a}] = co({cs:.3f})*{co_w:.3f} + klass({ks:.3f})*{classic_w:.3f} = {final_scores[a]:.3f}")

            # ------------- Maze anti-osc without ties -------------
            picked_override: Optional[str] = None
            if family == "maze":
                pos = observation.get("pos")
                grid = observation.get("grid"); H = observation.get("height"); W = observation.get("width")
                goal = observation.get("goal")
                if isinstance(pos,(list,tuple)): pr, pc = int(pos[0]), int(pos[1])
                else: pr = pc = None

                # (A) If mask left only one CO action and it's the inverse of last move,
                #     try to allow a lateral alternative that is free & promising.
                if co_scores and len(co_scores) == 1 and self._last_action in OPPOSITE:
                    only = next(iter(co_scores.keys()))
                    inv = OPPOSITE[self._last_action]
                    if only == inv and pr is not None:
                        # consider laterals
                        laterals = [a for a in ("UP","DOWN","LEFT","RIGHT")
                                    if a not in (only, OPPOSITE[only])]
                        # legal & free
                        cand = []
                        for a in laterals:
                            dr,dc = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}[a]
                            nr, nc = pr+dr, pc+dc
                            if self._maze_free(nr, nc, grid, H, W):
                                cand.append(a)
                        if cand:
                            # prefer improvement toward goal, then lookahead degree
                            best_a, best_key = None, (-1e9, -1)
                            for a in cand:
                                dr,dc = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}[a]
                                nr, nc = pr+dr, pc+dc
                                improve = 0
                                if isinstance(goal,(list,tuple)):
                                    gr,gc = int(goal[0]), int(goal[1])
                                    d0 = abs(pr-gr)+abs(pc-gc)
                                    d1 = abs(nr-gr)+abs(nc-gc)
                                    improve = d0 - d1
                                deg = self._maze_lookahead_degree(pr, pc, a, grid, H, W)
                                key = (improve, deg)
                                if key > best_key:
                                    best_key, best_a = key, a
                            if best_a is not None:
                                picked_override = best_a
                                print(f"[HEAD] mask-only inverse '{only}' -> override to lateral '{picked_override}'")

                # (B) Two-step 2-cycle detector: if we returned to pos_{t-2}, avoid inverse even without ties.
                if picked_override is None and self._prev_pos is not None and self._last_pos is not None and isinstance(pos,(list,tuple)):
                    cur = (int(pos[0]), int(pos[1]))
                    if cur == self._prev_pos and self._last_action in OPPOSITE:
                        inv = OPPOSITE[self._last_action]
                        # choose best legal non-inverse option
                        options = [a for a in ("UP","DOWN","LEFT","RIGHT") if a != inv]
                        best_a, best_key = None, (-1e9, -1)
                        for a in options:
                            dr,dc = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}[a]
                            nr, nc = cur[0]+dr, cur[1]+dc
                            if not self._maze_free(nr, nc, grid, H, W): continue
                            improve = 0
                            if isinstance(goal,(list,tuple)):
                                gr,gc = int(goal[0]), int(goal[1])
                                d0 = abs(cur[0]-gr)+abs(cur[1]-gc)
                                d1 = abs(nr-gr)+abs(nc-gc)
                                improve = d0 - d1
                            deg = self._maze_lookahead_degree(cur[0], cur[1], a, grid, H, W)
                            key = (improve, deg)
                            if key > best_key:
                                best_key, best_a = key, a
                        if best_a is not None:
                            picked_override = best_a
                            print(f"[HEAD] 2-cycle detected -> override inverse to '{picked_override}'")

            # choose action
            if final_scores or picked_override is not None:
                if picked_override is not None:
                    best = picked_override
                else:
                    best = max(final_scores, key=final_scores.get)

                # update 2-step position history
                pos = observation.get("pos")
                if isinstance(pos,(list,tuple)):
                    cur = (int(pos[0]), int(pos[1]))
                    self._prev_pos = self._last_pos
                    self._last_pos  = cur
                if family == "maze" and isinstance(best, str):
                    self._last_action = best

                print(f"[HEAD] choose action={best} sources={co_sources}")
                return {
                    "action": best,
                    "co_policy": f"{family}:blend(co={co_w:.2f})",
                    "co_bus_votes": int(n_votes),
                    "co_weight": float(co_w),
                    "classic_weight": float(classic_w),
                    "co_sources": co_sources,
                    "head_eps": float(self.eps),
                    "head_ngram_order": int(self.k),
                }

            # fallbacks (unchanged)
            if family == "bandit":
                n_arms = int(observation.get("n_arms", 2))
                self._ensure_arms(n_arms)
                for i in range(n_arms):
                    if self._counts[i] == 0:
                        return {"action": i, "co_policy": "bandit:fallback_roundrobin",
                                "co_bus_votes": 0, "co_weight": float(co_w), "classic_weight": float(classic_w),
                                "co_sources": ["fallback"], "head_eps": float(self.eps), "head_ngram_order": int(self.k)}
                a = self.rng.randrange(n_arms) if self.rng.random() < self.eps else max(range(n_arms), key=lambda j: self._means[j])
                return {"action": a, "co_policy": "bandit:fallback_egreedy",
                        "co_bus_votes": 0, "co_weight": float(co_w), "classic_weight": float(classic_w),
                        "co_sources": ["fallback"], "head_eps": float(self.eps), "head_ngram_order": int(self.k)}

            if family == "renewal":
                a = int(observation.get("obs", 0))
                return {"action": a, "co_policy": "renewal:fallback_predict_last",
                        "co_bus_votes": 0, "co_weight": float(co_w), "classic_weight": float(classic_w),
                        "co_sources": ["fallback"], "head_eps": float(self.eps), "head_ngram_order": int(self.k)}

            if family == "maze":
                pos = observation.get("pos"); goal = observation.get("goal")
                if isinstance(pos,(list,tuple)) and isinstance(goal,(list,tuple)):
                    pr, pc = int(pos[0]), int(pos[1])
                    gr, gc = int(goal[0]), int(goal[1])
                    deltas = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}
                    best = None; best_improve = -1e9
                    d0 = abs(pr-gr)+abs(pc-gc)
                    for d,(dr,dc) in deltas.items():
                        d1 = abs(pr+dr-gr)+abs(pc+dc-gc)
                        imp = d0 - d1
                        if imp > best_improve:
                            best_improve, best = imp, d
                    self._last_action = best
                    return {"action": best or "RIGHT", "co_policy": "maze:fallback_greedy",
                            "co_bus_votes": 0, "co_weight": float(co_w), "classic_weight": float(classic_w),
                            "co_sources": ["fallback"], "head_eps": float(self.eps), "head_ngram_order": int(self.k)}
            if actions:
                return {"action": actions[0], "co_policy": "fallback:any",
                        "co_bus_votes": 0, "co_weight": float(co_w), "classic_weight": float(classic_w),
                        "co_sources": ["fallback"], "head_eps": float(self.eps), "head_ngram_order": int(self.k)}
            return {}
        except Exception as ex:
            print(f"[HEAD.step] exception: {ex!r}")
            fam = str(observation.get("family","")).lower()
            if fam == "maze":
                pos = observation.get("pos"); goal = observation.get("goal")
                if isinstance(pos,(list,tuple)) and isinstance(goal,(list,tuple)):
                    pr, pc = int(pos[0]), int(pos[1]); gr, gc = int(goal[0]), int(goal[1])
                    deltas = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}
                    best = None; best_improve = -1e9
                    d0 = abs(pr-gr)+abs(pc-gc)
                    for d,(dr,dc) in deltas.items():
                        d1 = abs(pr+dr-gr)+abs(pc+dc-gc); imp = d0 - d1
                        if imp > best_improve: best_improve, best = imp, d
                    self._last_action = best
                    return {"action": best or "RIGHT", "co_policy": "maze:fallback_greedy", "co_bus_votes": 0,
                            "co_sources": ["fallback"]}
            actions = observation.get("action_space") or []
            return {"action": (actions[0] if actions else None), "co_policy": "fallback:any",
                    "co_bus_votes": 0, "co_sources": ["fallback"]}

    def run_update(self, elements: list, primitives: dict, header: any, observation: dict, feedback: dict | None) -> dict:
        out: dict = {}
        try:
            hrec = header.update(observation)
            if isinstance(hrec, dict): out.update(hrec)
        except Exception:
            pass
        for e in elements:
            if e.__class__.__name__.lower().endswith("actionhead"): continue
            if hasattr(e, "update"):
                try:
                    u = e.update(observation, primitives, header, feedback)
                    if isinstance(u, dict) and u: out.update(u)
                except Exception: pass
            if hasattr(e, "step"):
                try:
                    s = e.step(observation, primitives, header, feedback)
                    if isinstance(s, dict) and s: out.update(s)
                except Exception: pass
            if hasattr(e, "metrics"):
                try:
                    m = e.metrics()
                    if isinstance(m, dict) and m: out.update(m)
                except Exception: pass
        return out

    def metrics(self) -> Dict[str, Any]:
        return {"head_eps": float(self.eps), "head_ngram_order": int(self.k)}