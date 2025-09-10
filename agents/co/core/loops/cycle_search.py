from __future__ import annotations
from typing import Dict, Hashable, Iterable, List, Tuple, Optional

def karp_min_mean_cycle(
    nodes: Iterable[Hashable],
    edges: Dict[Tuple[Hashable, Hashable], float],
    include_node: Optional[Hashable] = None,
    max_len: int = 24,
    ) -> Tuple[Optional[List[Hashable]], Optional[float]]:
    """
    Karp's algorithm for minimum mean-weight cycle (on perceived costs).
    - nodes: iterable of class ids
    - edges: dict (u,v)->cost (must be non-negative here; if absent, not considered)
    - include_node: if set, restrict to cycles that include this node (filter afterwards)
    - max_len: cap path length considered (small graphs only)
    Returns (cycle_nodes_in_order, mean_cost) or (None, None) if none found.
    """
    V = list(nodes)
    n = len(V)
    if n == 0:
        return None, None
    idx = {v: i for i, v in enumerate(V)}

    # DP table: dp[k][v] = min cost of path of length k ending at v
    INF = 1e18
    dp = [[INF] * n for _ in range(max_len + 1)]
    for i in range(n):
        dp[0][i] = 0.0

    # predecessor for reconstruction
    pred: List[List[Optional[int]]] = [[None] * n for _ in range(max_len + 1)]

    for k in range(1, max_len + 1):
        for v in range(n):
            best = INF
            best_u = None
            for (u_node, v_node), c in edges.items():
                if idx[v_node] != v:
                    continue
                u = idx[u_node]
                cand = dp[k - 1][u] + c
                if cand < best:
                    best = cand
                    best_u = u
            dp[k][v] = best
            pred[k][v] = best_u

    # compute minimum mean weight over cycles using Karp's formula
    best_mean = INF
    best_v = None
    for v in range(n):
        max_diff = -INF
        for k in range(0, max_len):
            diff = (dp[max_len][v] - dp[k][v]) / max(1, (max_len - k))
            if diff > max_diff:
                max_diff = diff
        if max_diff < best_mean:
            best_mean = max_diff
            best_v = v

    if best_v is None or best_mean >= INF / 2:
        return None, None

    # attempt to reconstruct a cycle (heuristic backtrace)
    # We walk back max_len steps from best_v then search for a loop.
    path = []
    cur = best_v
    k = max_len
    visited = {}
    while k > 0 and cur is not None:
        path.append(cur)
        if cur in visited:
            start = visited[cur]
            cyc_idx = path[start:]
            cycle_nodes = [V[i] for i in reversed(cyc_idx)]
            if include_node is not None and include_node not in cycle_nodes:
                return None, None
            return cycle_nodes, float(best_mean)
        visited[cur] = len(path) - 1
        cur = pred[k][cur]
        k -= 1

    return None, None


def johnson_simple_cycles_limited(
    nodes: Iterable[Hashable],
    edges: Dict[Tuple[Hashable, Hashable], float],
    include_node: Optional[Hashable] = None,
    max_cycles: int = 256,
    max_len: int = 32,
    stop_if_cost_above: Optional[float] = None,
    ) -> List[Tuple[List[Hashable], float]]:
    """
    Limited simple-cycle enumeration (Johnson-like) with early stopping.
    Returns a list of (cycle_nodes, mean_cost).
    """
    # adjacency
    adj: Dict[Hashable, List[Hashable]] = {}
    for (u, v), _ in edges.items():
        if u == v:
            adj.setdefault(u, []).append(v)
        else:
            adj.setdefault(u, []).append(v)

    out: List[Tuple[List[Hashable], float]] = []

def dfs(start, u, stack, visited):
    if len(out) >= max_cycles or len(stack) > max_len:
        return
    visited.add(u)
    stack.append(u)
    for v in adj.get(u, []):
        if stop_if_cost_above is not None:
            # prune by worst edge (cheap heuristic): if any edge cost already > threshold
            if edges.get((u, v), 0.0) > stop_if_cost_above:
                continue
        if v == start and len(stack) >= 1:
            cyc = stack[:]  # includes u; close to start
            cyc_nodes = cyc[:]
            if include_node is None or include_node in cyc_nodes:
                total = 0.0
                m = 0
                for i in range(len(cyc_nodes)):
                    a = cyc_nodes[i]
                    b = cyc_nodes[(i + 1) % len(cyc_nodes)]
                    total += edges[(a, b)]
                    m += 1
                out.append((cyc_nodes, total / max(1, m)))
        elif v not in visited:
            dfs(start, v, stack, visited)
    stack.pop()
    visited.remove(u)

    for s in nodes:
        dfs(s, s, [], set())
        if len(out) >= max_cycles:
            break
    return out

from **future** import annotations  
from typing import Dict, Hashable, Iterable, List, Tuple, Optional, Set  
import math  
import random  
from collections import defaultdict, deque

Node = Hashable  
Edge = Tuple[Node, Node]  
Adj = Dict[Node, List[Tuple[Node, float]]]

class MinMeanCycleResult:  
"""  
Result of a min-mean-cycle search.  
"""  
def **init**(self,  
cycle: List[Node],  
mean_cost: float,  
used_method: str,  
inspected_cycles: int):  
self.cycle = cycle  
self.mean_cost = mean_cost  
self.used_method = used_method  
self.inspected_cycles = inspected_cycles

def _karp_min_mean_cycle(nodes: List[Node],  
adj: Adj,  
max_len: int = 24) -> Optional[MinMeanCycleResult]:  
"""  
Karp's algorithm for minimum mean cycle on a directed graph with real edge costs.  
We cap the dynamic-program length to <= max_len (pragmatic finitude).  
Returns None if not enough nodes/edges to form a cycle.  
"""  
n = min(len(nodes), max_len)  
if n < 2:  
return None  
# map node -> index 0..n-1 (truncate if > max_len)  
nodes = nodes[:n]  
idx = {v: i for i, v in enumerate(nodes)}

```
# DP[k][v] = min cost to reach v with exactly k edges
# initialize
DP = [[math.inf] * n for _ in range(n + 1)]
# arbitrary start: zero to self for all v at k=0
for i in range(n):
    DP[0][i] = 0.0

# forward DP
for k in range(1, n + 1):
    for v in nodes:
        j = idx[v]
        best = DP[k][j]  # carry
        # incoming edges u -> v
        # for efficiency, iterate all u and check if has edge to v
        for u in nodes:
            iu = idx[u]
            # scan adjacency from u
            for (w, c) in adj.get(u, []):
                if w == v and u in idx:
                    cand = DP[k - 1][iu] + c
                    if cand < best:
                        best = cand
        DP[k][j] = best

# compute mean cycle weight
best_mean = math.inf
best_v = None
for v in nodes:
    j = idx[v]
    max_val = -math.inf
    for k in range(n):
        if DP[n][j] < math.inf and DP[k][j] < math.inf and n != k:
            val = (DP[n][j] - DP[k][j]) / (n - k)
            if val > max_val:
                max_val = val
    if max_val < best_mean:
        best_mean = max_val
        best_v = v

if best_v is None or best_mean is math.inf:
    return None

# We do not reconstruct the exact cycle in this capped version (cost-only).
# Return single-node placeholder to indicate success on best_v.
return MinMeanCycleResult(cycle=[best_v], mean_cost=float(best_mean),
                          used_method="karp", inspected_cycles=0)
```

def _bounded_simple_cycles(adj: Adj,  
start_nodes: Iterable[Node],  
length_cap: int,  
enum_cap: int,  
stall_cap: int) -> Iterable[List[Node]]:  
"""  
Enumerate simple cycles with DFS bounded by:  
- length_cap: max cycle length  
- enum_cap: max cycles to yield  
- stall_cap: max expansions without improvement before stopping  
"""  
yielded = 0  
stall = 0

```
visited: Set[Node] = set()
stack: List[Node] = []

def dfs(start: Node, current: Node):
    nonlocal yielded, stall
    visited.add(current)
    stack.append(current)
    if current in adj:
        for (nxt, _) in adj[current]:
            if yielded >= enum_cap or stall >= stall_cap:
                break
            if nxt == start and 2 <= len(stack) <= length_cap:
                # yield a cycle (stack plus back to start)
                yielded += 1
                stall = 0
                yield list(stack)
            elif nxt not in visited and len(stack) < length_cap:
                for cyc in dfs(start, nxt):
                    if yielded >= enum_cap or stall >= stall_cap:
                        break
                    yield cyc
    stack.pop()
    visited.discard(current)
    stall += 1

for s in start_nodes:
    if yielded >= enum_cap:
        break
    # fresh DFS per start node
    visited.clear()
    stack.clear()
    for cyc in dfs(s, s):
        yield cyc
        if yielded >= enum_cap:
            break
```

def _cycle_cost(cycle: List[Node], adj: Adj) -> Optional[float]:  
total = 0.0  
for i in range(len(cycle)):  
u = cycle[i]  
v = cycle[(i + 1) % len(cycle)]  
# find u->v cost  
found = False  
for (w, c) in adj.get(u, []):  
if w == v:  
total += c  
found = True  
break  
if not found:  
return None  
return total / max(1, len(cycle))

def find_min_mean_cycle(adj: Adj,  
max_nodes_karp: int = 24,  
johnson_len_cap: int = 32,  
enum_cap: int = 256,  
stall_cap: int = 64,  
leave_cost_cutoff: Optional[float] = None) -> Optional[MinMeanCycleResult]:  
"""  
Find a minimum mean cycle cost with pragmatic caps:  
- try Karp capped to <= max_nodes_karp nodes  
- fallback to bounded DFS simple-cycle enumeration if needed  
- optionally discard cycles whose per-step cost exceeds leave_cost_cutoff *best_leave

```
adj: dict u -> list of (v, cost)

Returns MinMeanCycleResult or None if no cycle found within caps.
"""
nodes = list(adj.keys())
# 1) Try Karp (cost-only, no explicit cycle reconstruction in the capped variant)
karp_res = _karp_min_mean_cycle(nodes, adj, max_len=max_nodes_karp)
best_res = karp_res

# 2) Fallback bounded simple cycles to get an explicit cycle and possibly better mean
best_cycle: List[Node] = []
best_mean = math.inf
inspected = 0
for cyc in _bounded_simple_cycles(adj, nodes, johnson_len_cap, enum_cap, stall_cap):
    inspected += 1
    m = _cycle_cost(cyc + [cyc[0]], adj)  # ensure wrap-around
    if m is None:
        continue
    if leave_cost_cutoff is not None and m > leave_cost_cutoff:
        continue
    if m < best_mean:
        best_mean = m
        best_cycle = cyc[:]

if best_cycle:
    cand = MinMeanCycleResult(cycle=best_cycle, mean_cost=float(best_mean),
                              used_method="bounded_dfs", inspected_cycles=inspected)
    # choose better between karp cost and bounded dfs if both exist
    if best_res is None or cand.mean_cost < best_res.mean_cost:
        best_res = cand

return best_res