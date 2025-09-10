from **future** import annotations  
from typing import Iterable, Tuple, Hashable

Edge = Tuple[Hashable, Hashable]

def jaccard_similarity(a: Iterable[Edge], b: Iterable[Edge]) -> float:  
A = set(a)  
B = set(b)  
if not A and not B:  
return 1.0  
inter = len(A & B)  
union = len(A | B)  
if union == 0:  
return 1.0  
return float(inter / union)

def lln_stable(prev_edges: Iterable[Edge],  
curr_edges: Iterable[Edge],  
jaccard_thresh: float = 0.90) -> bool:  
"""  
Returns True when 1 - Jaccard <= 0.10 (equivalently, Jaccard >= 0.90).  
"""  
J = jaccard_similarity(prev_edges, curr_edges)  
return bool(J >= float(jaccard_thresh))