from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ComputeStats:
    flops_per_step: float = 0.0
    params: int = 0
    precision: str = "fp32"
    memory_bits: int = 0
    context_len: int = 0

def rough_stats_for(agent) -> ComputeStats:
    """
    Very rough, dependency-free compute stats for baselines.
    You can replace with precise accounting later.
    """
    params = int(getattr(agent, "num_params", 0))
    ctx = int(getattr(agent, "n_arms", 0))
    return ComputeStats(
        flops_per_step=0.0,  # unknown here; runners can override
        params=params,
        precision="fp32",
        memory_bits=0,
        context_len=ctx,
    )
