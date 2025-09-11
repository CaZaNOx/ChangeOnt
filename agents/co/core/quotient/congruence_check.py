from __future__ import annotations
from typing import List

def congruence_ok(keep_root: int, drop_root: int, new_partition: List[int]) -> bool:
    """
    Lightweight 'congruence' guard:
    - Prevent merges that would isolate an active attractor (heuristic).
    - Here we ensure 'keep_root' class size won't explode beyond a simple cap ratio.
    A real implementation would check empirical action deviations; this is a safe placeholder.
    """
    # Count sizes
    from collections import Counter
    cnt = Counter(new_partition)
    # If drop_root was unique representative, merging is trivial
    # Else, block pathological ballooning (> 80% of all items in one class)
    total = sum(cnt.values())
    return cnt.get(keep_root, 0) <= 0.8 * total
