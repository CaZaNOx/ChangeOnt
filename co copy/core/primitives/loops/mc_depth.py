from __future__ import annotations

def horizon_pairs_for_debt(
    base_horizon: int = 40,
    pairs: int = 8,
    recent_flips: int = 0,
    cooldown_boost: int = 0,
) -> tuple[int, int]:
    """
    Simple policy: increase MC horizon/pairs modestly with recent flip counts and cooldown pressure.
    Returns (horizon, pairs).
    """
    h = int(base_horizon + 2 * recent_flips + cooldown_boost)
    p = int(pairs + max(0, recent_flips // 3))
    return max(1, h), max(1, p)
