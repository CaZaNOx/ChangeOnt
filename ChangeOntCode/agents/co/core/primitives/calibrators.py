# agents/co/core/primitives/calibrators.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

@dataclass
class RMState:
    t: int = 0
    theta_min: float = 0.0
    theta_max: float = 1.0
    base_lr: float = 0.1
    decay: float = 0.51  # > 0.5 for convergence
    momentum: float = 0.0
    m: float = 0.0

def rm_update(theta: float, grad_like: float, st: RMState) -> Tuple[float, RMState]:
    """
    Robbins–Monro-style update with optional momentum + projection.
    grad_like: positive -> push theta up; negative -> push down.
    """
    st.t += 1
    lr = st.base_lr / (st.t ** st.decay)
    st.m = st.momentum * st.m + (1.0 - st.momentum) * grad_like
    new_theta = theta + lr * st.m
    if new_theta < st.theta_min: new_theta = st.theta_min
    if new_theta > st.theta_max: new_theta = st.theta_max
    return new_theta, st
