# agents/co/core/primitives/infimum_lift.py
from __future__ import annotations
from typing import Dict, Iterable, Tuple
import math
"""
Infimum-lift (baseline implementation):

Given a raw symbol sequence, this module:
  1) estimates a nominal period (if any),
  2) constructs a quotient/partition (currently trivial or classifier-based),
  3) lifts the sequence into the quotient space,
  4) returns the mapping and lifted sequence for downstream use.

The goal is to keep this minimal & deterministic; combination layers can swap
in richer partitioners/classifiers later without changing the call shape.
"""

def lift_edge_cost(
    classes: Dict[int, Iterable[int]],
    base_cost: Dict[Tuple[int, int], float],
    src_class: int,
    dst_class: int,
    *,
    witness: Dict[Tuple[int, int], Tuple[int, int]] | None = None,
) -> Tuple[float, Tuple[int, int] | None]:
    """
    Infimum-lift: class->class edge cost is the minimum of member->member perceived costs.
    Returns (cost, witness_pair). If no member edge exists, returns (inf, None).
    """
    best = math.inf
    best_pair: Tuple[int, int] | None = None
    for u in classes.get(src_class, ()):
        for v in classes.get(dst_class, ()):
            c = base_cost.get((u, v), math.inf)
            if c < best:
                best = c
                best_pair = (u, v)
    if witness is not None and best_pair is not None:
        witness[(src_class, dst_class)] = best_pair
    return best, best_pair

def cycle_cost_with_witness(
    cycle: list[int],
    classes: Dict[int, Iterable[int]],
    base_cost: Dict[Tuple[int, int], float],
) -> float:
    """
    Enforce witness-consistent cycles: consecutive lifted edges must chain the same representative.
    Reject (return inf) if witness consistency is impossible.
    """
    if len(cycle) < 2:
        return math.inf
    total = 0.0
    prev_rep: int | None = None
    for i in range(len(cycle)):
        a = cycle[i]
        b = cycle[(i + 1) % len(cycle)]
        cost, pair = lift_edge_cost(classes, base_cost, a, b)
        if not math.isfinite(cost) or pair is None:
            return math.inf
        u, v = pair
        if prev_rep is not None and u != prev_rep:
            # Breaks witness chain: reject
            return math.inf
        prev_rep = v
        total += cost
    return total
