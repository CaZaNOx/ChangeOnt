from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple

@dataclass
class MergeWitness:
    pair: Tuple[int, int]
    dist: float
    tau: float
    hdr_hash: str
    kept: int
    dropped: int

class UnionFind:
    def __init__(self, n: int):
        self.par = list(range(n))
        self.sz = [1] * n
    def find(self, x: int) -> int:
        while self.par[x] != x:
            self.par[x] = self.par[self.par[x]]
            x = self.par[x]
        return x
    def union(self, a: int, b: int) -> int:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return ra
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.par[rb] = ra
        self.sz[ra] += self.sz[rb]
        return ra

def equivalence_closure(
    items: List[Dict[str, Any]],
    *,
    tau: float,
    distance: Callable[[list[int], list[int]], float],
    header_ok: Callable[[dict, dict], bool],
    hdr_hash: Callable[[dict], str],
    congruence_ok: Callable[[int, int, List[int]], bool],
) -> Tuple[List[int], List[MergeWitness]]:
    """
    Deterministic union-find closure with header agreement & congruence guard.
    Returns (roots array, witness log).
    """
    n = len(items)
    uf = UnionFind(n)
    # Enumerate all candidate pairs with in-threshold distance
    candidates: List[Tuple[float, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            if not header_ok(items[i].get("header", {}), items[j].get("header", {})):
                continue
            d = distance(items[i].get("trace", []), items[j].get("trace", []))
            if d <= tau:
                candidates.append((d, i, j))
    # Deterministic order: by distance then by indices
    candidates.sort(key=lambda t: (t[0], t[1], t[2]))

    witnesses: List[MergeWitness] = []
    for d, i, j in candidates:
        ri, rj = uf.find(i), uf.find(j)
        if ri == rj:
            continue
        # Congruence check takes roots and proposed partition after union
        par_snapshot = [uf.find(k) for k in range(n)]
        # simulate union
        sim_par = par_snapshot[:]
        # choose deterministic "kept" root (smaller index)
        keep, drop = (ri, rj) if ri < rj else (rj, ri)
        sim_par = [keep if x == drop else x for x in sim_par]
        if not congruence_ok(keep, drop, sim_par):
            continue
        new_root = uf.union(keep, drop)
        w = MergeWitness(
            pair=(i, j),
            dist=d,
            tau=tau,
            hdr_hash=hdr_hash(items[i].get("header", {})) + "|" + hdr_hash(items[j].get("header", {})),
            kept=new_root,
            dropped=drop,
        )
        witnesses.append(w)

    roots = [uf.find(k) for k in range(n)]
    return roots, witnesses
