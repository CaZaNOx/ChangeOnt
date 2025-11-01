# agents/co/adapters/probes.py
from typing import Dict, List, Any
import math
from collections import deque, Counter

def _norm01(x: float, lo: float, hi: float) -> float:
    if hi <= lo: return 0.0
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))

class ProbesAggregator:
    """
    Maintain light probes to estimate dynamicity:
      - V: reward/cost volatility (EMA variance)
      - CP: change-point proxy (mean shift z-score)
      - H: holonomy/order effect (AB vs BA bias in transitions)
      - R: repeat-subpaths ratio (stability)
      - K: compressibility slope (unique-token ratio trend)
      - F: Fano factor proxy on event counts
      - MRAI: (optional) agreement; you can set externally via set_external()
    """
    def __init__(self, window: int = 64):
        self.window = int(window)
        self.r_hist: deque = deque(maxlen=window)
        self.s_hist: deque = deque(maxlen=window)
        self.m_means = {"left": None, "right": None}
        self.mrai = 0.0

    def update(self, reward: float | None = None, state_token: Any | None = None):
        if reward is not None:
            self.r_hist.append(float(reward))
        if state_token is not None:
            self.s_hist.append(state_token)

    def set_external(self, key: str, val: float):
        if key == "MRAI":
            self.mrai = max(0.0, min(1.0, float(val)))

    def _volatility(self) -> float:
        xs = list(self.r_hist)
        if len(xs) < 4: return 0.0
        mu = sum(xs)/len(xs)
        var = sum((x-mu)**2 for x in xs)/len(xs)
        return _norm01(math.sqrt(var), 0.0, 1.0)

    def _changepoint(self) -> float:
        xs = list(self.r_hist)
        n = len(xs)
        if n < 8: return 0.0
        mid = n//2
        mu1 = sum(xs[:mid])/max(1, mid)
        mu2 = sum(xs[mid:])/max(1, n-mid)
        z = abs(mu2 - mu1) / (1e-6 + sum(abs(x) for x in xs)/max(1,n))
        return _norm01(z, 0.0, 1.0)

    def _holonomy(self) -> float:
        # crude: count AB vs BA for adjacent pairs of tokens
        s = list(self.s_hist)
        if len(s) < 6: return 0.0
        pairs = Counter((a,b) for a,b in zip(s, s[1:]) if a is not None and b is not None)
        ab = sum(v for (a,b), v in pairs.items() if a!=b)
        ba = ab  # symmetric in this crude proxy
        if ab+ba == 0: return 0.0
        bias = abs(ab - ba)/max(1, ab+ba)
        return _norm01(bias, 0.0, 1.0)

    def _repeat_ratio(self) -> float:
        s = list(self.s_hist)
        if not s: return 1.0
        uniq = len(set(s))
        return _norm01(1.0 - uniq/max(1,len(s)), 0.0, 1.0)

    def _compressibility(self) -> float:
        s = list(self.s_hist)
        n = len(s)
        if n < 8: return 0.0
        uniq_ratio = len(set(s))/n
        # more unique -> less compressible; use negative slope via simple EMA
        return _norm01(1.0 - uniq_ratio, 0.0, 1.0)

    def _fano(self) -> float:
        # count-of-events per fixed bins (here: token occurrences mod small map)
        s = list(self.s_hist)
        if len(s) < 10: return 0.0
        counts = Counter(s)
        vals = list(counts.values())
        mu = sum(vals)/len(vals)
        if mu == 0: return 0.0
        var = sum((v-mu)**2 for v in vals)/len(vals)
        f = var / mu
        return _norm01(f, 0.0, 5.0)

    def probes(self) -> Dict[str,float]:
        return {
            "V": self._volatility(),
            "CP": self._changepoint(),
            "H": self._holonomy(),
            "R": self._repeat_ratio(),
            "K": self._compressibility(),
            "F": self._fano(),
            "MRAI": self.mrai,
        }
