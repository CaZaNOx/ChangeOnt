# E_E_compressibility.py
from typing import Iterable, Any, Dict

class EE_Compressibility:
    """
    Element E: Memory compressibility → robustness predictor.
    Skeleton: LZ-like counter (very simple) and linear predictor.
    """
    def __init__(self, window: int = 32):
        self.window = max(4, int(window))

    def _lz_counter(self, seq: Iterable[Any]) -> float:
        # toy distinct-substring counter within a sliding window
        buf = []
        seen = set()
        k = self.window
        for x in seq:
            buf.append(x)
            if len(buf) > k:
                buf.pop(0)
            s = tuple(buf)
            seen.add(s)
        return float(len(seen))

    def predict_robustness(self, seq: Iterable[Any]) -> Dict[str, float]:
        lz = self._lz_counter(seq)
        # toy monotone mapping: lower LZ -> higher robustness
        robustness = 1.0 / (1.0 + lz) if lz > 0 else 0.0
        return {"lz": lz, "robustness_pred": robustness}
