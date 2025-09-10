from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import hashlib
import json

@dataclass
class Rep:
    rid: str
    tokens: List[Any]  # last W tokens, right-aligned, ⌀-padded
    header: Dict[str, Any]  # {'collapse': bool, 'density_mode': str, ...}
    freshness: int  # smaller = fresher

def content_hash(rep: Rep) -> str:
    m = hashlib.sha256()
    hdr = json.dumps(rep.header, sort_keys=True)
    toks = json.dumps(rep.tokens, default=str)
    m.update(hdr.encode()); m.update(b"|"); m.update(toks.encode())
    return m.hexdigest()

class UnionFind:
    def __init__(self, reps: List[Rep]):
        self.parent = {r.rid: r.rid for r in reps}
        self.size = {r.rid: 1 for r in reps}

    def find(self, x: str) -> str:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> str:
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return ra
        if self.size[ra] < self.size[rb]: ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return ra

def header_agree(a: Rep, b: Rep) -> bool:
    return (a.header.get("collapse") == b.header.get("collapse")
            and a.header.get("density_mode") == b.header.get("density_mode"))

def warped_bend_distance(a: Rep, b: Rep, gauge: Dict[Any,float], pad_weight: float=0.25) -> float:
    assert len(a.tokens) == len(b.tokens)
    W = len(a.tokens); acc = 0.0
    for x,y in zip(a.tokens, b.tokens):
        if x == y: continue
        gx = gauge.get(x, 0.0) if x != "⌀" else pad_weight
        gy = gauge.get(y, 0.0) if y != "⌀" else pad_weight
        w = 1.0 - 0.5*(gx+gy)
        acc += w
    return acc / max(1, W)

def rtau(a: Rep, b: Rep, tau: float, gauge: Dict[Any,float]) -> bool:
    return header_agree(a,b) and warped_bend_distance(a,b,gauge) <= tau

def closure(reps: List[Rep], tau: float, gauge: Dict[Any,float], seed: int,
            witness_log_path: str) -> Dict[str, str]:
    """Deterministic name-free closure with witness logging."""
    uf = UnionFind(reps)
    # build candidates
    cands: List[Tuple[float,int,int,str,str]] = []
    for i, u in enumerate(reps):
        for j in range(i+1, len(reps)):
            v = reps[j]
            if not header_agree(u,v): continue
            d = warped_bend_distance(u,v,gauge)
            if d <= tau:
                # sort key: (d, freshness, seed, hash xor)
                hx = int(content_hash(u), 16) ^ int(content_hash(v), 16)
                key = (d, min(u.freshness, v.freshness), seed, hx)
                cands.append((d, min(u.freshness, v.freshness), seed, u.rid, v.rid))
    # deterministic sort
    cands.sort(key=lambda t: (t[0], t[1], t[2], int(hashlib.sha256(f"{t[3]}|{t[4]}".encode()).hexdigest(),16)))
    # log
    logf = open(witness_log_path, "a", encoding="utf-8")
    for _, _, _, u_id, v_id in cands:
        ru, rv = uf.find(u_id), uf.find(v_id)
        if ru == rv: continue
        # congruence residual placeholder (set via downstream oracle later)
        record = {
            "seed": seed, "pair": [u_id, v_id], "dist": None, "tau": tau,
            "hdr_hash": None, "congruence_resid": None,
            "chosen": True, "kept_root": ru, "other_root": rv
        }
        uf.union(ru, rv)
        logf.write(json.dumps(record)+"\n")
    logf.close()
    return uf.parent
