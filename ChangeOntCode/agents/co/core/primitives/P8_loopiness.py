# agents/co/core/primitives/P8_loopiness.py
from typing import Any, Iterable

def loopiness(frontier_graph_or_path: Any) -> float:
    """
    Minimal loopiness: if path is provided, fraction of revisits;
    if graph (adj list) provided, average clustering-ish proxy.
    """
    if isinstance(frontier_graph_or_path, (list, tuple)):
        seen = set()
        revisits = 0
        for x in frontier_graph_or_path:
            if x in seen: revisits += 1
            seen.add(x)
        return (revisits / max(1, len(frontier_graph_or_path)))
    # graph case: expect dict node->neighbors
    g = frontier_graph_or_path
    if isinstance(g, dict):
        degs = [len(v) for v in g.values()]
        if not degs: return 0.0
        return sum(1.0 if d >= 2 else 0.0 for d in degs) / len(degs)
    return 0.0

def suggest_p_breadth(L: float, depth_hint: int = 5) -> float:
    """Simple policy: more loops => more breadth (cap in [0.1, 0.9])."""
    return min(0.9, max(0.1, 0.1 + 0.8 * L))
