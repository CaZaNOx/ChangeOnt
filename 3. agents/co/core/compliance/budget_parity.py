from **future** import annotations  
from typing import Dict, Optional

_DTYPE_BITS = {  
"float32": 32, "fp32": 32,  
"float16": 16, "fp16": 16, "bfloat16": 16,  
"int8": 8, "uint8": 8, "int16": 16, "int32": 32,  
}

class BudgetMeter:  
"""  
Budget parity meter. Track:  
- parameter bits  
- runtime buffers (KV caches, quotient tables, gauges)  
- FLOPs/step (moving average)  
All counts are _agent-side only_ (plant/env excluded).  
"""  
def **init**(self, name: str, context_cap: Optional[int] = None, precision: str = "float32"):  
self.name = str(name)  
self.precision = precision  
self.param_bits = 0  
self.runtime_bits = 0  
self.extra_bits: Dict[str, int] = {}  
self.flops_accum = 0.0  
self.steps = 0  
self.context_cap = context_cap

```
# ---- memory accounting ---------------------------------------------------
@staticmethod
def _bits(n_elems: int, dtype: str) -> int:
    bits = _DTYPE_BITS.get(dtype, 32)
    return int(n_elems * bits)

def add_params(self, n_elems: int, dtype: Optional[str] = None) -> None:
    self.param_bits += self._bits(int(n_elems), dtype or self.precision)

def add_runtime(self, tag: str, n_elems: int, dtype: Optional[str] = None) -> None:
    bits = self._bits(int(n_elems), dtype or self.precision)
    self.runtime_bits += bits
    self.extra_bits[tag] = self.extra_bits.get(tag, 0) + bits

def add_quotient_table(self, n_classes: int, avg_outdeg: int, store_cost: bool = True, dtype: Optional[str] = None) -> None:
    """
    Approx memory for quotient adjacency table:
      entries ~= n_classes * avg_outdeg
      store (to_idx, cost) -> assume index fits in 32 bits; cost dtype by precision
    """
    entries = int(max(0, n_classes) * max(0, avg_outdeg))
    idx_bits = 32
    cost_bits = _DTYPE_BITS.get(dtype or self.precision, 32) if store_cost else 0
    bits = entries * (idx_bits + cost_bits)
    self.runtime_bits += bits
    self.extra_bits["quotient"] = self.extra_bits.get("quotient", 0) + bits

def add_gauge_table(self, n_classes: int, dtype: Optional[str] = None) -> None:
    bits = self._bits(int(n_classes), dtype or self.precision)
    self.runtime_bits += bits
    self.extra_bits["gauge"] = self.extra_bits.get("gauge", 0) + bits

def add_kv_cache(self, layers: int, heads: int, ctx: int, d_head: int, dtype: Optional[str] = None) -> None:
    """
    KV cache bits ~= 2 (K,V) * layers * heads * ctx * d_head * dtype_bits
    """
    elems = 2 * int(layers) * int(heads) * int(ctx) * int(d_head)
    bits = self._bits(elems, dtype or self.precision)
    self.runtime_bits += bits
    self.extra_bits["kv_cache"] = self.extra_bits.get("kv_cache", 0) + bits

# ---- compute accounting --------------------------------------------------
def step_flops(self, flops: float) -> None:
    self.flops_accum += float(flops)
    self.steps += 1

# ---- snapshots -----------------------------------------------------------
def as_dict(self) -> Dict[str, float]:
    mean_flops = (self.flops_accum / self.steps) if self.steps > 0 else 0.0
    d = {
        "name": self.name,
        "precision": self.precision,
        "context_cap": self.context_cap if self.context_cap is not None else -1,
        "param_bits": int(self.param_bits),
        "runtime_bits": int(self.runtime_bits),
        "flops_per_step_mean": float(mean_flops),
    }
    for k, v in self.extra_bits.items():
        d[f"bits_{k}"] = int(v)
    return d

def pretty(self) -> str:
    d = self.as_dict()
    lines = [f"[BudgetMeter:{self.name}]"]
    for k in sorted(d.keys()):
        lines.append(f"{k}: {d[k]}")
    return "\n".join(lines)