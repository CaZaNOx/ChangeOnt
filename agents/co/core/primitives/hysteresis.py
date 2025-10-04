from __future__ import annotations
from dataclasses import dataclass

@dataclass
class FlipState:
    active: bool = False
    cooldown: int = 0  # steps remaining before another flip allowed

def hysteresis_step(
    score: float,
    st: FlipState,
    *,
    theta_on: float = 0.25,
    theta_off: float = 0.15,
    min_dwell: int = 10,
) -> FlipState:
    """
    Two-threshold hysteresis with cooldown/dwell.
    - If inactive and score >= theta_on and cooldown == 0 -> activate and set dwell.
    - If active and score <= theta_off and cooldown == 0 -> deactivate and set dwell.
    - Otherwise, keep state; cooldown counts down to 0.
    """
    s = max(0.0, min(1.0, score))
    cd = max(0, st.cooldown - 1)

    if cd == 0:
        if not st.active and s >= theta_on:
            return FlipState(active=True, cooldown=min_dwell)
        if st.active and s <= theta_off:
            return FlipState(active=False, cooldown=min_dwell)
    return FlipState(active=st.active, cooldown=cd)
