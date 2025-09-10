from **future** import annotations  
from typing import Dict, Hashable, Tuple, List

Node = Hashable  
Adj = Dict[Node, List[Tuple[Node, float]]]

def perceived_adj_from_edges(observed_edges: Dict[Tuple[Node, Node], float],  
gauge: Dict[Node, float],  
nonneg: bool = True) -> Adj:  
"""  
Build perceived-cost adjacency from:  
observed_edges[(u,v)] = base_cost δ(u->v) (constant in time)  
gauge[u], gauge[v] ∈ [0,1]  
c_G(u->v) = δ(u->v) - 0.5*(G[u]+G[v]); clamp to >=0 if nonneg=True  
"""  
adj: Adj = {}  
for (u, v), delta in observed_edges.items():  
Gu = float(gauge.get(u, 0.0))  
Gv = float(gauge.get(v, 0.0))  
c = float(delta) - 0.5 * (Gu + Gv)  
if nonneg and c < 0.0:  
c = 0.0  
adj.setdefault(u, []).append((v, float(c)))  
# ensure nodes with no outgoing still appear  
for (u, v) in observed_edges.keys():  
adj.setdefault(v, adj.get(v, []))  
adj.setdefault(u, adj.get(u, []))  
return adj