# agents/co/utils/log_hook.py
from typing import Dict, List, Any

class LogHook:
    """
    Light log buffer for adapters/runners to push time-step metrics.
    """
    def __init__(self, maxlen: int = 10000):
        self.maxlen = maxlen
        self.rows: List[Dict[str, Any]] = []

    def push(self, row: Dict[str, Any]):
        self.rows.append(dict(row))
        if len(self.rows) > self.maxlen:
            self.rows = self.rows[-self.maxlen:]

    def snapshot(self) -> List[Dict[str, Any]]:
        return list(self.rows)

    def reduce(self, keys: List[str]) -> Dict[str, Any]:
        agg = {}
        if not self.rows: return agg
        for k in keys:
            try:
                vals = [float(r[k]) for r in self.rows if k in r]
                if vals:
                    agg[f"mean_{k}"] = sum(vals)/len(vals)
                    agg[f"last_{k}"] = vals[-1]
            except Exception:
                pass
        return agg
