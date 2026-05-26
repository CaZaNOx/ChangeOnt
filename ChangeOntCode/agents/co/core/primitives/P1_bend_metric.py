from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence, Tuple
import math

# Bounded kernel realization of doctrinal bend.
# The primitive models directional deformation burden by aligning two bounded traces
# under weighted insertion/deletion/substitution costs. Costs are not attached to a
# neutral static geometry; they arise from preserved-vs-altered structure and from
# the asymmetry of carrying a source trace into a target trace.

L = 12
PAD_TOKEN = -1
PAD_COST = 0.25
MISMATCH_COST = 1.0
DEL_COST = 0.50
INS_COST = 0.50
TRANSPOSE_FACTOR = 0.65
RECENCY_GAMMA = 1.35


@dataclass(frozen=True)
class _EditCell:
    cost: float
    prev: Tuple[int, int]
    op: str


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _freeze(x: Any) -> Any:
    if isinstance(x, dict):
        return tuple(sorted((str(k), _freeze(v)) for k, v in x.items()))
    if isinstance(x, (list, tuple)):
        return tuple(_freeze(v) for v in x)
    if isinstance(x, set):
        return tuple(sorted(_freeze(v) for v in x))
    return x


def _normalize(trace: Sequence[Any]) -> List[Any]:
    t = list(trace)
    if len(t) > L:
        t = t[-L:]
    if len(t) < L:
        t = [PAD_TOKEN] * (L - len(t)) + t
    return [_freeze(v) for v in t]


def _weights(n: int = L) -> List[float]:
    raw = [(i + 1) ** RECENCY_GAMMA for i in range(n)]
    s = sum(raw) or 1.0
    return [float(x / s) for x in raw]


_W = _weights()


def _token_features(tok: Any) -> Dict[str, float]:
    if tok == PAD_TOKEN:
        return {"pad": 1.0, "arity": 0.0, "magnitude": 0.0, "hash": 0.0}
    if isinstance(tok, (int, float)):
        mag = math.tanh(abs(float(tok)) / 10.0)
        sign = 0.5 if float(tok) >= 0 else 0.0
        return {"pad": 0.0, "arity": 1.0, "magnitude": mag, "sign": sign, "hash": 0.0}
    if isinstance(tok, tuple):
        ln = len(tok)
        nums = [float(v) for v in tok if isinstance(v, (int, float))]
        mag = math.tanh((sum(abs(v) for v in nums) / max(1, len(nums))) / 10.0) if nums else 0.0
        return {"pad": 0.0, "arity": min(1.0, ln / 6.0), "magnitude": mag, "hash": (hash(tok) & 255) / 255.0}
    s = str(tok)
    return {"pad": 0.0, "arity": min(1.0, len(s) / 12.0), "magnitude": 0.0, "hash": (hash(s) & 255) / 255.0}


def token_similarity(a: Any, b: Any) -> float:
    if a == b:
        return 1.0
    if a == PAD_TOKEN or b == PAD_TOKEN:
        return 0.0
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        gap = abs(float(a) - float(b))
        scale = max(1.0, min(12.0, 1.0 + 0.25 * (abs(float(a)) + abs(float(b)))))
        return _clamp01(1.0 - gap / scale)
    fa = _token_features(a)
    fb = _token_features(b)
    keys = sorted(set(fa) | set(fb))
    dif = sum(abs(float(fa.get(k, 0.0)) - float(fb.get(k, 0.0))) for k in keys)
    sim = max(0.0, 1.0 - dif / max(1.0, float(len(keys))))
    # modest string/tuple structural reinforcement
    if isinstance(a, tuple) and isinstance(b, tuple):
        common = sum(1 for x, y in zip(a, b) if x == y)
        sim = max(sim, common / max(1, min(len(a), len(b))))
    return max(0.0, min(1.0, sim))


def _weighted_edit_alignment(source: Sequence[Any], target: Sequence[Any]) -> Dict[str, float]:
    a = _normalize(source)
    b = _normalize(target)
    n, m = len(a), len(b)
    wa = _weights(n)
    wb = _weights(m)

    dp: List[List[_EditCell]] = [[_EditCell(0.0, (0, 0), "") for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = dp[i - 1][0].cost + DEL_COST * wa[i - 1]
        dp[i][0] = _EditCell(cost, (i - 1, 0), "del")
    for j in range(1, m + 1):
        cost = dp[0][j - 1].cost + INS_COST * wb[j - 1]
        dp[0][j] = _EditCell(cost, (0, j - 1), "ins")

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sim = token_similarity(a[i - 1], b[j - 1])
            avg_w = 0.5 * (wa[i - 1] + wb[j - 1])
            sub_cost = dp[i - 1][j - 1].cost + MISMATCH_COST * avg_w * (1.0 - sim)
            best = _EditCell(sub_cost, (i - 1, j - 1), "match" if sim >= 0.999999 else "sub")

            del_cost = dp[i - 1][j].cost + DEL_COST * wa[i - 1]
            if del_cost < best.cost - 1e-12:
                best = _EditCell(del_cost, (i - 1, j), "del")

            ins_cost = dp[i][j - 1].cost + INS_COST * wb[j - 1]
            if ins_cost < best.cost - 1e-12:
                best = _EditCell(ins_cost, (i, j - 1), "ins")

            if i >= 2 and j >= 2 and a[i - 2] == b[j - 1] and a[i - 1] == b[j - 2]:
                tw = 0.5 * (wa[i - 2] + wa[i - 1] + wb[j - 2] + wb[j - 1]) / 2.0
                trans_cost = dp[i - 2][j - 2].cost + TRANSPOSE_FACTOR * tw
                if trans_cost < best.cost - 1e-12:
                    best = _EditCell(trans_cost, (i - 2, j - 2), "trans")

            dp[i][j] = best

    # Traceback to get preserved / altered decomposition.
    i, j = n, m
    preserved = 0.0
    insertion = 0.0
    deletion = 0.0
    substitution = 0.0
    transposition = 0.0
    aligned_similarity = 0.0
    while i > 0 or j > 0:
        cell = dp[i][j]
        op = cell.op
        pi, pj = cell.prev
        if op in {"match", "sub"}:
            sim = token_similarity(a[i - 1], b[j - 1])
            avg_w = 0.5 * (wa[i - 1] + wb[j - 1])
            preserved += avg_w * sim
            aligned_similarity += sim * avg_w
            if op == "sub":
                substitution += avg_w * (1.0 - sim)
        elif op == "del":
            deletion += wa[i - 1]
        elif op == "ins":
            insertion += wb[j - 1]
        elif op == "trans":
            tw = 0.5 * (wa[i - 2] + wa[i - 1] + wb[j - 2] + wb[j - 1]) / 2.0
            transposition += tw
            # transposition preserves token identity but alters local order
            preserved += 0.5 * tw
        i, j = pi, pj

    total_source = sum(wa)
    total_target = sum(wb)
    total_mass = 0.5 * (total_source + total_target)
    raw_cost = dp[n][m].cost
    max_cost = total_source * DEL_COST + total_target * INS_COST + max(total_source, total_target) * MISMATCH_COST
    if max_cost <= 1e-12:
        norm_burden = 0.0
    else:
        norm_burden = max(0.0, min(1.0, raw_cost / max_cost))

    preserved_mass = max(0.0, min(1.0, preserved / max(1e-9, total_mass)))
    altered_mass = max(0.0, min(1.0, 1.0 - preserved_mass))
    return {
        "preserved_mass": float(preserved_mass),
        "altered_mass": float(altered_mass),
        "insertion_cost": float(min(1.0, insertion)),
        "deletion_cost": float(min(1.0, deletion)),
        "substitution_cost": float(min(1.0, substitution)),
        "transposition_cost": float(min(1.0, transposition)),
        "directional_burden": float(norm_burden),
        "raw_cost": float(raw_cost),
        "similarity_mass": float(max(0.0, min(1.0, aligned_similarity / max(1e-9, total_mass)))),
    }


def bend_components(path, path_prime) -> Dict[str, float]:
    return _weighted_edit_alignment(path, path_prime)


def directional_bend(source, target) -> float:
    return float(bend_components(source, target)["directional_burden"])


def bend_distance(path, path_prime, metric: str = "edit", tau: float = 0.0) -> float:
    mode = str(metric).lower()
    if mode in {"directional", "directed", "burden"}:
        return directional_bend(path, path_prime)
    ab = directional_bend(path, path_prime)
    ba = directional_bend(path_prime, path)
    return float(0.5 * (ab + ba))


def is_same(path, path_prime, tau: float) -> bool:
    return bend_distance(path, path_prime, "edit", tau) <= tau


def d_bend(trace_a: List[int], trace_b: List[int]) -> float:
    return float(bend_distance(trace_a, trace_b))


def closure(paths: Iterable[Sequence[Any]], eps: float) -> List[Sequence[Any]]:
    paths = list(paths)
    kept: List[Sequence[Any]] = []
    for p in paths:
        if not any(bend_distance(p, q, "edit") <= eps for q in kept):
            kept.append(p)
    return kept
