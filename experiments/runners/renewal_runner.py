# experiments/runners/renewal_runner.py
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

from core.gauge.haq import Gauge, GaugeConfig
from core.headers.collapse import CollapseHeader, CollapseConfig
from core.headers.meta_flip import HysteresisFlip, FlipConfig

@dataclass
class RunnerConfig:
    steps: int = 1000
    seed: int = 1729

def toy_environment(step: int, phase_len: int = 50) -> int:
    """
    Simple renewal drift: emits a class id that flips every phase_len steps.
    """
    return (step // phase_len) % 2

def run(cfg: RunnerConfig) -> None:
    random.seed(cfg.seed)

    gauge = Gauge(GaugeConfig())
    collapse = CollapseHeader(CollapseConfig())
    flip = HysteresisFlip(FlipConfig())

    metrics_path = "metrics.jsonl"
    budget_path = "budget.csv"
    # For demo we write a tiny compute ledger with arbitrary constants
    with open(budget_path, "w", encoding="utf-8") as f:
        f.write("step,flops_per_step,memory_bits,precision,context\n")

    with open(metrics_path, "w", encoding="utf-8") as m_out:
        for t in range(cfg.steps):
            y = toy_environment(t)
            # fake PE/EU from mismatch between gauge and phase boundary
            # large regret near boundaries to trigger adaptation
            boundary = 1 if (t % 50) in (0, 1, 2) else 0
            pe = 1.0 if boundary else 0.2
            eu = 0.2 if boundary else 0.6
            g = gauge.step(pe=pe, eu=eu)

            # loop_score: higher near boundaries
            loop_score = 0.8 if boundary else 0.1
            mode = flip.step(loop_score)

            frozen, ent_bits, var_rel = collapse.update([y])

            rec = {
                "step": t,
                "y": y,
                "g": g,
                "loop_score": loop_score,
                "mode": mode,
                "collapse": int(frozen),
                "entropy_bits": ent_bits,
                "var_rel": var_rel,
            }
            m_out.write(json.dumps(rec) + "\n")

            with open(budget_path, "a", encoding="utf-8") as f:
                f.write(f"{t},1.0,1e6,32,128\n")

if __name__ == "__main__":
    run(RunnerConfig())
