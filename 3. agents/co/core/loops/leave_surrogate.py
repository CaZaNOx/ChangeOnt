from **future** import annotations  
from typing import Dict, Hashable, List, Tuple, Optional

from core.loops.cycle_search import find_min_mean_cycle, MinMeanCycleResult

Node = Hashable  
Adj = Dict[Node, List[Tuple[Node, float]]]

def _successor_on_cycle(cycle: List[Node], x: Node) -> Optional[Node]:  
if x not in cycle: return None  
i = cycle.index(x)  
return cycle[(i + 1) % len(cycle)]

def _edge_cost(adj: Adj, u: Node, v: Node) -> Optional[float]:  
for (w, c) in adj.get(u, []):  
if w == v:  
return float(c)  
return None

def _advance_cost_on_cycle(adj: Adj, cycle: List[Node], start: Node, target: Node) -> Optional[float]:  
"""  
Sum perceived costs along the cycle from 'start' to 'target' (inclusive of edges traversed).  
"""  
if start not in cycle or target not in cycle:  
return None  
cost = 0.0  
i = cycle.index(start)  
# walk until we land on target  
while True:  
u = cycle[i]  
v = cycle[(i + 1) % len(cycle)]  
c = _edge_cost(adj, u, v)  
if c is None:  
return None  
cost += c  
i = (i + 1) % len(cycle)  
if v == target:  
break  
return float(cost)

def best_leave_cost(adj: Adj, current: Node,  
leave_cutoff: Optional[float] = None) -> Tuple[Optional[float], Optional[List[Node]], Optional[float]]:  
"""  
CO-compliant 'leave' surrogate:  
1) Find min-mean cycle L that _includes_ current if possible; otherwise the global min-mean cycle.  
2) For every x in L:  
d_L(current→x) = accumulated perceived cost to reach x by following L  
out(x) = min perceived cost of any edge x→y with y not the successor on L  
Define C_leave = min_x d_L(current→x) + out(x).  
If no outward edge exists from any x, return (None, cycle, C_stay).  
Returns (C_leave, cycle_nodes, C_stay=mean_cost_of_L).  
"""  
mmc = find_min_mean_cycle(adj)  
if mmc is None or not mmc.cycle:  
return (None, None, None)

```
cycle = mmc.cycle[:]
C_stay = float(mmc.mean_cost)

# If 'current' not on cycle, we still use this L but distances d_L start from the nearest entry by cycling
if current not in cycle:
    # choose a deterministic proxy: use cycle[0] as start
    current = cycle[0]

best = None
for x in cycle:
    succ = _successor_on_cycle(cycle, x)
    # outward edge: any edge not equal to the successor on L
    out_costs = [c for (y, c) in adj.get(x, []) if succ is None or y != succ]
    if not out_costs:
        continue
    out_x = min(out_costs)
    d_curr_x = _advance_cost_on_cycle(adj, cycle, current, x)
    if d_curr_x is None:
        continue
    total = float(d_curr_x + out_x)
    if best is None or total < best:
        best = total

if leave_cutoff is not None and best is not None and best > float(leave_cutoff):
    # reject if exceeds cutoff
    return (None, cycle, C_stay)
return (best, cycle, C_stay)
