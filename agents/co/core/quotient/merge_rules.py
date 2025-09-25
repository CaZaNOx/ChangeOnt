# PATH: agents/co/core/quotient/merge_rules.py
from __future__ import annotations
from typing import Sequence, Dict, List, Optional

def warped_hamming_distance(a: Sequence[int], b: Sequence[int], *, pad_weight: float=0.25) -> float:
    la, lb = len(a), len(b)
    L = max(la, lb)
    if L == 0:
        return 0.0
    d = 0.0
    for i in range(L):
        ai = a[i] if i < la else None
        bi = b[i] if i < lb else None
        d += pad_weight if (ai is None or bi is None) else (0.0 if ai == bi else 1.0)
    return d / L

def warped_bend_distance(a: Sequence[int], b: Sequence[int], *, pad_weight: float=0.25,
                         gauge_weights: Optional[Sequence[float]]=None) -> float:
    la, lb = len(a), len(b)
    L = max(la, lb)
    if L == 0:
        return 0.0
    dist = 0.0
    wsum = 0.0
    for i in range(L):
        w = gauge_weights[i] if (gauge_weights is not None and i < len(gauge_weights)) else 1.0
        ai = a[i] if i < la else None
        bi = b[i] if i < lb else None
        dist += w * (pad_weight if (ai is None or bi is None) else (0.0 if ai == bi else 1.0))
        wsum += w
    return (dist/wsum) if wsum > 0 else 0.0

def merge_pass(classes: Dict[int, List[int]], traces: Dict[int, List[int]], *, tau: float=0.25) -> Dict[int, List[int]]:
    """Merge classes whose representative traces are within tau (warped-Hamming)."""
    reps = [members[0] for members in classes.values() if members]
    new_classes: Dict[int, List[int]] = {r: [r] for r in reps}
    for i in range(len(reps)):
        ri = reps[i]
        for j in range(i+1, len(reps)):
            rj = reps[j]
            di = traces.get(ri, [])
            dj = traces.get(rj, [])
            d = warped_hamming_distance(di, dj)
            if d <= tau:
                keep, drop = (ri, rj) if ri < rj else (rj, ri)
                new_classes.setdefault(keep, []).extend(new_classes.get(drop, [drop]))
                if drop in new_classes:
                    del new_classes[drop]
    return new_classes
