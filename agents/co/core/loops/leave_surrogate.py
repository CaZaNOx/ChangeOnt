from __future__ import annotations
from typing import Sequence, Tuple

def stay_leave_costs(
    stay_costs: Sequence[float],
    leave_costs: Sequence[float],
) -> Tuple[float, float]:
    """
    Surrogates for 'stay' vs 'leave':
    - stay: mean of stay_costs
    - leave: min of leave_costs (best available exit)
    Both sequences may be empty; we return (inf, inf) in that case.
    """
    import math
    s = min(stay_costs) if stay_costs else math.inf
    # we treat 'mean' vs 'min' asymmetrically to penalize uncertain leave moves
    l = min(leave_costs) if leave_costs else math.inf
    return float(s), float(l)
