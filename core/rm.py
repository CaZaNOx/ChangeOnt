# FILE: core/rm.py
import numpy as np

def alpha_t(t: int, c: float = 50.0, gamma: float = 0.6) -> np.float32:
    """Robbins–Monro step size: (t+c)^-gamma, float32."""
    return np.float32((t + c) ** (-gamma))
