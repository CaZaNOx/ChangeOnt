# agents/co/core/primitives/P6_change_ops.py
from typing import Sequence, Any, Dict, Tuple
from collections import defaultdict, Counter
from .P1_bend_metric import bend_distance

def _kgrams(seq: Sequence[Any], k: int) -> list[Tuple[Any, ...]]:
    return [tuple(seq[i:i+k]) for i in range(max(0, len(seq)-k+1))]

def learn_prototypes(history: Sequence[Any], k: int, eps: float, base_metric: str = "edit") -> Dict:
    """
    Very small unsupervised prototype learner:
      - extract k-grams
      - greedy medoid clustering under edit/overlap distance with threshold eps*k
    """
    grams = _kgrams(history, k)
    if not grams:
        return {"prototypes": [], "assign": [], "eps": eps, "k": k, "mean_distortion": 0.0, "n_prototypes": 0}

    thr = max(0, int(round(eps * k)))
    clusters: list[list[Tuple[Any,...]]] = []
    for g in grams:
        placed = False
        for cl in clusters:
            # distance: edit distance between tuples as sequences
            d = bend_distance(list(g), list(cl[0]), base_metric)
            if d <= thr:
                cl.append(g)
                placed = True
                break
        if not placed:
            clusters.append([g])

    # medoids = first element (simple)
    protos = [cl[0] for cl in clusters]
    # assignment + distortion
    dists = []
    assign = []
    for g in grams:
        best = None
        bestd = 1e9
        for idx, p in enumerate(protos):
            d = bend_distance(list(g), list(p), base_metric)
            if d < bestd:
                bestd = d; best = idx
        assign.append(best)
        dists.append(bestd)

    mean_dist = float(sum(dists))/max(1, len(dists))
    return {
        "prototypes": protos,
        "assign": assign,
        "eps": eps,
        "k": k,
        "mean_distortion": mean_dist,
        "n_prototypes": len(protos),
    }

def features_from(history: Sequence[Any], P: Dict, eps: float) -> Dict[str, float]:
    """Counts per prototype and pairwise adjacencies (simple features)."""
    k = P.get("k", 3)
    grams = _kgrams(history, k)
    protos = P.get("prototypes", [])
    if not protos:
        return {"counts": {}, "pairs": {}}

    thr = max(0, int(round(eps * k)))
    # nearest proto index
    idxs = []
    for g in grams:
        best = None; bestd = 1e9
        for i, p in enumerate(protos):
            d = bend_distance(list(g), list(p), "edit")
            if d < bestd:
                bestd = d; best = i
        if best is not None and bestd <= thr:
            idxs.append(best)

    counts = Counter(idxs)
    pairs = Counter((i, j) for i, j in zip(idxs, idxs[1:]) if i is not None and j is not None)
    # flatten keys for logger-friendliness
    feats = {f"c_{i}": float(v) for i, v in counts.items()}
    feats.update({f"c_{i}_{j}": float(v) for (i, j), v in pairs.items()})
    return {"counts": feats, "pairs": feats}  # reuse dict for simplicity

def compose(p_i: Sequence[Any], p_j: Sequence[Any], eps: float) -> tuple:
    """
    Overlap-aware concat: find best suffix/prefix overlap (Hamming), merge.
    """
    k = min(len(p_i), len(p_j))
    best_r = 0
    for r in range(1, k):
        suf = p_i[-r:]
        pre = p_j[:r]
        if sum(int(a != b) for a, b in zip(suf, pre)) <= int(round(eps * r)):
            best_r = r
    if best_r == 0:
        return tuple(p_i) + tuple(p_j)
    return tuple(p_i[:-best_r]) + tuple(p_j)
