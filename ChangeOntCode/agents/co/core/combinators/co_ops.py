# agents/co/core/combinators/co_ops.py
from __future__ import annotations
from typing import Dict, Iterable, Tuple

def min_plus_sum(vals: Iterable[float]) -> float:
    return sum(vals)  # '+' is the monoid in Lawvere metric

def inf_convolution(f: Dict, g: Dict) -> Dict:
    """
    (f ⊗ g)(u->v) = min_w f(u->w) + g(w->v)
    f,g: dict of (u,w)->cost
    returns dict of (u,v)->cost
    """
    out = {}
    keys_f = list(f.keys())
    keys_g = list(g.keys())
    nodes_w = set(k[1] for k in keys_f).union(set(k[0] for k in keys_g))
    nodes_u = set(k[0] for k in keys_f)
    nodes_v = set(k[1] for k in keys_g)
    for u in nodes_u:
        for v in nodes_v:
            best = None
            for w in nodes_w:
                cf = f.get((u, w))
                cg = g.get((w, v))
                if cf is None or cg is None: continue
                cand = cf + cg
                if (best is None) or (cand < best):
                    best = cand
            if best is not None:
                out[(u, v)] = float(best)
    return out

def residuation(a: float, b: float) -> float:
    """a ⇒ b in (min,+) is truncated subtraction."""
    return max(0.0, b - a)
