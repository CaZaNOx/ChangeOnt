from __future__ import annotations
from typing import Dict, Iterable, Tuple, DefaultDict
from collections import defaultdict

def build_adjacency(edges: Iterable[Tuple[int, int]]) -> Dict[int, Dict[int, int]]:
    """
    Build an adjacency map with simple integer counts from an iterable of (u, v) edges.
    Returns: {u: {v: count}}
    """
    adj: DefaultDict[int, DefaultDict[int, int]] = defaultdict(lambda: defaultdict(int))
    for u, v in edges:
        adj[u][v] += 1
    return {u: dict(d) for u, d in adj.items()}
