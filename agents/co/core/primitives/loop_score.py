# PATH: agents/co/core/primitives/loop_score.py
from __future__ import annotations
from typing import Sequence, Tuple, Optional

# numpy is optional; we gracefully fall back to pure Python if it's missing
try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

__all__ = ["loop_score", "estimate_loop_period"]


def _to_array(x: Sequence[float]):
    """Return (arr, n) where arr is a zero-mean float array/list and n is its length."""
    n = len(x)
    if n == 0:
        return [], 0
    if np is not None:
        arr = np.asarray(x, dtype=float)
        arr = arr - (float(arr.mean()) if n > 0 else 0.0)
        return arr, n
    # pure Python fallback
    m = sum(float(v) for v in x) / float(n)
    arr = [float(v) - m for v in x]
    return arr, n


def _normalized_acf(arr, n: int, max_lag: int):
    """
    Normalized autocorrelation r_k for k=0..max_lag (r_0 == 1.0).
    If variance is ~0, returns zeros (no periodic signal).
    """
    if n < 2:
        return [1.0] + [0.0] * max(0, max_lag)

    if np is not None:
        var = float(np.sum(arr * arr))
        if var <= 1e-12:
            return [1.0] + [0.0] * max(0, max_lag)

        # compute full ACF via np.correlate; take non-negative lags
        full = np.correlate(arr, arr, mode="full")
        acf = full[n - 1 : n - 1 + max_lag + 1]  # lags 0..max_lag
        acf = acf / acf[0]  # normalize so r_0 == 1
        return [float(v) for v in acf]
    else:
        # pure Python O(n * max_lag) fallback
        var = sum(v * v for v in arr)
        if var <= 1e-12:
            return [1.0] + [0.0] * max(0, max_lag)

        out = []
        for lag in range(max_lag + 1):
            s = 0.0
            cnt = n - lag
            for i in range(cnt):
                s += arr[i] * arr[i + lag]
            # normalize so r_0 == 1.0
            # (this divides by the same s at lag=0)
            if lag == 0:
                s0 = s if s != 0.0 else 1.0
                out.append(1.0)
            else:
                out.append(float(s / s0))
        return out


def estimate_loop_period(
    x: Sequence[float],
    min_period: int = 2,
    max_period: Optional[int] = None,
    multi_cycle_penalty: bool = True,
) -> Tuple[int, float]:
    """
    Estimate a dominant loop period via the ACF peak and return (period, peak_strength).

    - min_period: smallest candidate period to consider (>=2).
    - max_period: largest period; default = len(x)//2 (needs at least ~2 cycles to be credible).
    - peak_strength: normalized ACF at the chosen period in [0,1]; higher => more periodic.

    If the series is too short or essentially constant, returns (0, 0.0).
    """
    arr, n = _to_array(x)
    if n < 3:
        return 0, 0.0

    if max_period is None:
        max_period = max(min(n // 2, 512), min_period)

    min_p = max(2, int(min_period))
    max_p = max(min_p, int(max_period))

    acf = _normalized_acf(arr, n, max_p)
    # search best lag in [min_p, max_p]
    best_p, best_r = 0, 0.0
    for p in range(min_p, max_p + 1):
        r = acf[p] if p < len(acf) else 0.0
        if r > best_r:
            best_r = r
            best_p = p

    if best_p <= 0 or best_r <= 0.0:
        return 0, 0.0

    # (optional) penalize if we haven't observed at least ~2 cycles
    if multi_cycle_penalty and best_p > 0:
        cycles = n / float(best_p)
        if cycles < 2.0:
            # linearly down-weight until two cycles
            best_r *= max(0.0, (cycles - 1.0))
            best_r = min(max(best_r, 0.0), 1.0)

    return best_p, float(min(max(best_r, 0.0), 1.0))


def loop_score(
    x: Sequence[float],
    min_period: int = 2,
    max_period: Optional[int] = None,
    multi_cycle_penalty: bool = True,
) -> float:
    """
    Return a scalar loopiness score in [0,1] for the sequence `x`.

    Implementation notes:
      - Uses the normalized autocorrelation function (ACF).
      - Picks the strongest peak in the lag range [min_period, max_period]
        (default max_period ~ len(x)//2).
      - Score = normalized ACF at that lag, optionally down-weighted if fewer
        than ~2 cycles are present in the data.
      - Robust to mean/scale (detrends mean; normalizes by r_0).

    This is drop-in compatible with earlier minimal versions that returned
    a single scalar. If you also need the detected period, call:
        period, strength = estimate_loop_period(x, ...)
    """
    _, strength = estimate_loop_period(
        x,
        min_period=min_period,
        max_period=max_period,
        multi_cycle_penalty=multi_cycle_penalty,
    )
    return strength
