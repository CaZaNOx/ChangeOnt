# core/quotient/equivalence.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
import hashlib
import json

Hash = str
NodeId = Any  # hashable
ClassId = Any  # hashable

def _stable_hash_bytes(obj: Any) -> bytes:
    """Deterministic content hash independent of Python id()."""
    # Use a canonical JSON representation
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).digest()

def stable_hash(obj: Any) -> Hash:
    return hashlib.sha256(_stable_hash_bytes(obj)).hexdigest()

@dataclass(frozen=True)
class CandidatePair:
    u: NodeId
    v: NodeId
    dist: float
    header_hash: Hash

class UnionFind:
    """
    Name-free union-find with deterministic tie-break based on content hashes.
    Tracks 'witness' edges chosen for merges.
    """
    def __init__(self, items: Iterable[NodeId], signature_fn: Callable[[NodeId], Any]):
        self.parent: Dict[NodeId, NodeId] = {}
        self.rank: Dict[NodeId, int] = {}
        self.sig_fn = signature_fn
        self.sig_hash: Dict[NodeId, Hash] = {}
        self.witness_log: List[Dict[str, Any]] = []

        for x in items:
            self.parent[x] = x
            self.rank[x] = 0
            self.sig_hash[x] = stable_hash(self.sig_fn(x))

    def find(self, x: NodeId) -> NodeId:
        # path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def _tie_break(self, a: NodeId, b: NodeId) -> NodeId:
        """Return the preferred representative (deterministic)."""
        ha, hb = self.sig_hash[a], self.sig_hash[b]
        if ha < hb:
            return a
        if hb < ha:
            return b
        # absolute tie (extremely rare) -> fall back to lex order of repr()
        return a if repr(a) <= repr(b) else b

    def union(self, a: NodeId, b: NodeId, witness: Optional[Dict[str, Any]] = None) -> NodeId:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return ra
        # union by rank, but keep deterministic chosen representative
        keep = self._tie_break(ra, rb)
        drop = rb if keep == ra else ra

        # rank update
        if self.rank[ra] == self.rank[rb]:
            if keep == ra:
                self.rank[ra] += 1
            else:
                self.rank[rb] += 1

        # attach 'drop' under 'keep'
        self.parent[drop] = keep

        if witness is not None:
            self.witness_log.append({
                "chosen": True,
                "keep": keep,
                "drop": drop,
                **witness,
            })
        return keep

    def classes(self) -> Dict[NodeId, List[NodeId]]:
        out: Dict[NodeId, List[NodeId]] = {}
        for x in self.parent.keys():
            r = self.find(x)
            out.setdefault(r, []).append(x)
        return out

def deterministic_merge_pass(
    items: Iterable[NodeId],
    distance_fn: Callable[[NodeId, NodeId], float],
    header_agree_fn: Callable[[NodeId, NodeId], bool],
    signature_fn: Callable[[NodeId], Any],
    tau: float,
    seed: int = 1729,
) -> Tuple[UnionFind, List[CandidatePair]]:
    """
    Compute a deterministic set of merges under (distance <= tau) and header agreement.
    Returns the union-find and the ordered candidate list we considered (for audit).
    """
    items_list = list(items)
    # Build candidate list
    cands: List[CandidatePair] = []
    for i in range(len(items_list)):
        for j in range(i + 1, len(items_list)):
            u, v = items_list[i], items_list[j]
            if not header_agree_fn(u, v):
                continue
            d = distance_fn(u, v)
            if d <= tau:
                hdr_obj = {"hdr_u": signature_fn(u), "hdr_v": signature_fn(v)}
                cands.append(CandidatePair(u=u, v=v, dist=d, header_hash=stable_hash(hdr_obj)))

    # Deterministic order: (dist ↑, freshness? we don't have timestamps here, then tie on stable hashes)
    cands.sort(key=lambda cp: (cp.dist, stable_hash(cp.u), stable_hash(cp.v)))

    uf = UnionFind(items_list, signature_fn)
    # Merge in order; we do NOT split during a pass
    for cp in cands:
        ru, rv = uf.find(cp.u), uf.find(cp.v)
        if ru == rv:
            continue
        # Optionally, a "congruence check" hook could go here; keep simple for kernel
        uf.union(ru, rv, witness={
            "seed": seed,
            "pair": [cp.u, cp.v],
            "dist": cp.dist,
            "tau": tau,
            "header_hash": cp.header_hash,
        })
    return uf, cands
