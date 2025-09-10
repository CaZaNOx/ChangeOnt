from __future__ import annotations
from typing import Deque, Dict, Hashable, Iterable, List, Tuple
from collections import deque

def warped_hamming_distance(
    toks_u: Deque[Hashable],
    toks_v: Deque[Hashable],
    L: int = 12,
    pad_weight: float = 0.25,
    lambda_g: float = 0.5,
    gauge_lookup=lambda tok: 0.0,
    ) -> float:
    """
    Warped Hamming distance on the last L tokens of two classes.
    - pad with ⌀ (null) carrying pad_weight
    - local weights w_i = 1 - lambda_g * 0.5 * (g(tu)+g(tv))
    """
    dist = 0.0
    Lu, Lv = len(toks_u), len(toks_v)
    null = "⌀"
    for i in range(L):
        tu = toks_u[Lu - 1 - i] if i < Lu else null
        tv = toks_v[Lv - 1 - i] if i < Lv else null
        gu = 0.0 if tu == null else float(gauge_lookup(tu))
        gv = 0.0 if tv == null else float(gauge_lookup(tv))
        w = 1.0 - lambda_g * 0.5 * (gu + gv)
        if tu == null or tv == null:
            w *= pad_weight
        if tu != tv:
            dist += w
    return float(dist)

def merge_pass(
    class_tokens: Dict[int, Deque[Hashable]],
    L: int = 12,
    pad_weight: float = 0.25,
    lambda_g: float = 0.5,
    tau_merge: float = 0.20,
    gauge_lookup=lambda tok: 0.0,
    max_classes: int = 64,
    ) -> Dict[int, int]:
    """
    One O(n^2) merge pass (acceptable under class cap).
    Returns a mapping of old_cid -> new_cid for any merges performed.
    Uses warped_hamming_distance and merges if d <= tau_merge * L.
    """
    ids = list(class_tokens.keys())
    parent = {cid: cid for cid in ids}

def find(x: int) -> int:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a: int, b: int) -> None:
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

    changed = True
    while changed:
        changed = False
        ids = [i for i in ids if find(i) == i]
        # break if already under cap and nothing to compare
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                ci, cj = ids[i], ids[j]
                di = warped_hamming_distance(
                    class_tokens[ci], class_tokens[cj],
                    L=L, pad_weight=pad_weight, lambda_g=lambda_g, gauge_lookup=gauge_lookup
                )
                if di <= tau_merge * L:
                    union(ci, cj)
                    changed = True
                    if len({find(k) for k in parent}) <= max_classes:
                        # continue merging; cap is enforced elsewhere (LRU pruning)
                        pass

    # build map from each cid to its representative
    rep_map = {cid: find(cid) for cid in class_tokens.keys()}
    return rep_map