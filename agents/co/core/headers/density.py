from future import annotations
from dataclasses import dataclass
from typing import Dict, Hashable, Iterable, Tuple

@dataclass
class DensitySignals:
    breadth: float
    depth: float
    depth2_agrees: bool

    def _normalized_branching(outdeg: Dict[Hashable, int]) -> float:
        if not outdeg:
            return 0.0
        m = max(outdeg.values())
        if m <= 0:
            return 0.0
        return float(sum(outdeg.values()) / (len(outdeg) * m))

    def _revisit_ratio(visits: Dict[Hashable, int]) -> float:
        if not visits:
            return 0.0
        distinct = sum(1 for _, c in visits.items() if c > 0)
        total = sum(visits.values())
        if total == 0:
            return 0.0
        revisit = total - distinct
        return float(max(0.0, revisit / total))

    def _mean_return_time(visits: Dict[Hashable, int]) -> float:
        # proxy: inverse of visit frequency averaged over visited nodes
        if not visits:
            return 0.0
        visited = [c for c in visits.values() if c > 0]
        if not visited:
            return 0.0
        inv = [1.0 / c for c in visited]
        return float(sum(inv) / len(inv))

    def compute_density_signals(
    transitions: Iterable[Tuple[Hashable, Hashable]],
    ) -> DensitySignals:
        """
        Compute breadth (normalized branching) and depth (1 - revisit_ratio).
        Add a second depth proxy via (normalized) mean return time and require
        agreement within tolerance ±0.10 to set depth2_agrees True.
        """
        outdeg: Dict[Hashable, int] = {}
        visits: Dict[Hashable, int] = {}
        for u, v in transitions:
            outdeg[u] = outdeg.get(u, 0) + (0 if v in outdeg else 0) # outdeg counted below
            visits[u] = visits.get(u, 0) + 1
            visits[v] = visits.get(v, 0) + 1
            # recompute outdeg properly
            outdeg = {}
            for u, v in transitions:
                outdeg[u] = outdeg.get(u, 0) + 1

                b = _normalized_branching(outdeg)
                d = 1.0 - _revisit_ratio(visits)
                d2 = _mean_return_time(visits)
                # normalize d2 to [0,1] by heuristic clipping (robust for small windows)
                d2n = max(0.0, min(1.0, d2 / (d2 + 1.0)))
                agree = abs(d - d2n) <= 0.10
        return DensitySignals(breadth=float(b), depth=float(d), depth2_agrees=bool(agree))


    def density_header_decision(
        signals: DensitySignals,
        breadth_thresh: float = 0.60,
        ratio_thresh: float = 1.50,
        ) -> str:
        """
        Decide header mode: "breadth", "depth", or "mixed" based on:
        - breadth ≥ breadth_thresh and breadth ≥ ratio_thresh * depth -> breadth
        - depth ≥ breadth_thresh and depth ≥ ratio_thresh * breadth -> depth
        - else -> mixed
        """
        b, d = signals.breadth, signals.depth
        if b >= breadth_thresh and b >= ratio_thresh * d:
            return "breadth"
        if d >= breadth_thresh and d >= ratio_thresh * b and signals.depth2_agrees:
            return "depth"
        return "mixed"
    

    from **future** import annotations  
from typing import Dict, Hashable, List, Tuple

Node = Hashable  
Adj = Dict[Node, List[Tuple[Node, float]]]

def breadth_out_degree(adj: Adj) -> float:  
"""  
Normalized breadth = mean out-degree / max_out_degree (guard for zero).  
"""  
if not adj:  
return 0.0  
degrees = [len(adj.get(u, [])) for u in adj.keys()]  
max_deg = max(1, max(degrees))  
mean_deg = sum(degrees) / len(degrees)  
return float(mean_deg / max_deg)

def depth_revisitation_rate(class_visits: Dict[Node, int]) -> float:  
"""  
Revisitation rate over a window: fraction of visits that return to previously seen classes.  
Input: class_visits = counts over the window.  
"""  
total = sum(class_visits.values())  
if total <= 0:  
return 0.0  
distinct = sum(1 for k, v in class_visits.items() if v > 0)  
# naive proxy: more distinct => lower revisitation. Map to [0,1]  
revisitation = 1.0 - (distinct / max(1, total))  
return float(revisitation)

def depth_loop_occupancy(loop_nodes: List[Node], visit_counts: Dict[Node, int]) -> float:  
"""  
Secondary depth proxy: fraction of window visits that land on the current loop.  
"""  
tot = sum(visit_counts.values())  
if tot <= 0:  
return 0.0  
on_loop = sum(visit_counts.get(v, 0) for v in loop_nodes)  
return float(on_loop / tot)

def decide_density_schedule(adj: Adj,  
class_visits: Dict[Node, int],  
loop_nodes: List[Node],  
breadth_thresh: float = 0.60,  
ratio: float = 1.50,  
depth_agree_tol: float = 0.10) -> str:  
"""  
Decide header schedule per spec:  
- breadth b = normalized out-degree  
- depth d = 1 - revisitation_rate  
- safety: depth proxy 2 (loop occupancy) must agree with d within tolerance  
Returns 'breadth', 'depth', or 'mixed'.  
"""  
b = breadth_out_degree(adj)  
d1 = 1.0 - depth_revisitation_rate(class_visits)  
d2 = depth_loop_occupancy(loop_nodes, class_visits)  
agree = abs(d1 - d2) <= depth_agree_tol

```
if b >= breadth_thresh and b >= ratio * d1 and agree:
    return "breadth"
if d1 >= breadth_thresh and d1 >= ratio * b and agree:
    return "depth"
return "mixed"