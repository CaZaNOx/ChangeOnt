from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Dict
from pathlib import Path

from agents.co.core.gauge.haq import Gauge, GaugeConfig
from agents.co.core.headers.collapse import CollapseHeader, CollapseConfig
from agents.co.core.headers.meta_flip import HysteresisFlip, FlipConfig
from experiments.logging import JSONLWriter

@dataclass
class RunnerConfig:
    steps: int = 500
    seed: int = 1729
    phase_len: int = 50
    out_dir: str = "outputs"

def toy_environment(step: int, phase_len: int = 50) -> int:
    """Simple renewal drift: emits a class id that flips every phase_len steps."""
    return (step // phase_len) % 2

def run(cfg: RunnerConfig) -> Dict[str, str]:
    random.seed(cfg.seed)
    out = Path(cfg.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    metrics_path = out / "metrics.jsonl"
    budget_path = out / "budget.csv"

    gauge = Gauge(GaugeConfig())
    collapse = CollapseHeader(CollapseConfig())
    flip = HysteresisFlip(FlipConfig())

    with open(budget_path, "w", encoding="utf-8") as f:
        f.write("step,flops_per_step,memory_bits,precision,context\n")

    with JSONLWriter(str(metrics_path)) as m_out:
        for t in range(cfg.steps):
            y = toy_environment(t, cfg.phase_len)

            # boundary heuristic to create pressure
            boundary = 1 if (t % cfg.phase_len) in (0, 1, 2) else 0
            pe = 1.0 if boundary else 0.2
            eu = 0.2 if boundary else 0.6
            g = gauge.step(pe=pe, eu=eu)

            loop_score = 0.8 if boundary else 0.1
            mode = flip.step(loop_score)

            # Toy prediction: exploit tries to match y; explore flips it.
            pred = y if mode == 0 else (1 - y)

            frozen, ent_bits, var_rel = collapse.update([y])

            rec = {
                "step": t,
                "y": y,
                "pred": pred,
                "g": g,
                "loop_score": loop_score,
                "mode": mode,
                "collapse": int(frozen),
                "entropy_bits": ent_bits,
                "var_rel": var_rel,
            }
            m_out.write(rec)
            with open(budget_path, "a", encoding="utf-8") as f:
                f.write(f"{t},1.0,1000000,32,128\n")

    return {"metrics": str(metrics_path), "budget": str(budget_path)}

if __name__ == "__main__":
    cfg = RunnerConfig()
    paths = run(cfg)
    print(json.dumps(paths))
