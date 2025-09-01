from future import annotations  
from typing import Iterable, List, Sequence, Tuple  
import math  
import statistics

def theil_sen_slope(xs: Sequence[float], ys: Sequence[float], max_pairs: int = 400) -> float:  
    n = len(xs)  
    if n < 2:  
        return 0.0  
    pairs = []  
    step = max(1, n // int(math.sqrt(max_pairs)))  
    idxs = list(range(0, n, step))  
    for i in idxs:  
        xi = xs[i]  
        for j in idxs:  
            if j <= i:  
                continue  
            dx = xs[j] - xi  
            if dx != 0:  
                pairs.append((ys[j] - ys[i]) / dx)  
            if len(pairs) >= max_pairs:  
                break  
            if len(pairs) >= max_pairs:  
                break  
        return float(statistics.median(pairs) if pairs else 0.0)

def fdr_windowed(flip_times: Sequence[int], event_times: Sequence[int], delta: int = 6) -> float:  
    if not flip_times:  
        return 0.0  
    E = sorted(event_times)  
    hits = 0  
    j = 0  
    for f in sorted(flip_times):  
        # advance pointer j so E[j] is just >= f - delta  
        while j < len(E) and E[j] < f - delta:  
            j += 1  
            ok = False  
            for k in (j-1, j, j+1):  
                if 0 <= k < len(E) and abs(E[k] - f) <= delta:  
                    ok = True  
                    break  
                if ok:  
                    hits += 1  
                    tp = hits  
                    fp = len(flip_times) - tp  
    return float(fp / max(1, tp + fp))

def au_regret_window(  
baseline_rewards: Sequence[float],  
agent_rewards: Sequence[float],  
window: int = 100,  
) -> float:  
    """  
    Renewal toy: per-step reward ∈ {0,1}. For each fixed window, compute  
    Δ = mean(baseline) - mean(agent); return positive-improvement average over windows.  
    """  
    if not baseline_rewards or not agent_rewards:  
        return 0.0  
    n = min(len(baseline_rewards), len(agent_rewards))  
    W = max(1, int(window))  
    diffs = []  
    i = 0  
    while i < n:  
        j = min(n, i + W)  
        b = sum(baseline_rewards[i:j]) / (j - i)  
        a = sum(agent_rewards[i:j]) / (j - i)  
        d = max(0.0, b - a)  
        diffs.append(d)  
        i = j  
    return float(sum(diffs) / len(diffs)) if diffs else 0.0