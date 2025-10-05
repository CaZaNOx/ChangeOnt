# FILE: experiments/runners/renewal_runner.py
from __future__ import annotations

import argparse
import json
import random
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from agents.stoa.renewal.vo_markov import VOKT
from experiments.logging.logging import write_metric_line, write_budget_csv


def _seed_all(seed: int) -> None:
    random.seed(seed)
    if np is not None:
        try:
            np.random.seed(seed)  # type: ignore[attr-defined]
        except Exception:
            pass


def _safe_copy(src: Path, dst: Path, retries: int = 12, delay: float = 0.12) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(retries):
        try:
            shutil.copy2(src, dst)
            return
        except PermissionError:
            time.sleep(delay)
    shutil.copy2(src, dst)


@dataclass
class _RunCfg:
    seed: int
    steps: int
    out_dir: Path
    mode: str
    agent: Dict[str, Any]
    env: Dict[str, Any]


def run(config_path: Optional[str]) -> dict:
    cfg: Dict[str, Any] = {
        "seed": 7,
        "steps": 1000,
        "env": {"A": 8, "L_win": 6, "p_ren": 0.02, "p_noise": 0.00, "T_max": 1000},
        "out_dir": "outputs/renewal_fsm",
        "mode": "last",
        "agent": {"type": "last", "params": {}},
    }

    if config_path:
        text = Path(config_path).read_text(encoding="utf-8")
        try:
            import yaml  # type: ignore
            loaded = yaml.safe_load(text) or {}
        except Exception:
            loaded = json.loads(text)
        for k, v in loaded.items():
            if k == "env" and isinstance(v, dict):
                cfg["env"].update(v)
            else:
                cfg[k] = v

    seed = int(cfg.get("seed", 7))
    steps = int(cfg.get("steps", cfg["env"].get("T_max", 1000)))
    out_dir = Path(cfg.get("out_dir", "outputs/renewal_fsm"))
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = out_dir / "metrics.jsonl"
    budget_path = out_dir / "budget.csv"
    plot_path = out_dir / "quick_plot.png"

    _seed_all(seed)

    env = CodebookRenewalEnvW(
        EnvCfg(
            A=int(cfg["env"]["A"]),
            L_win=int(cfg["env"]["L_win"]),
            p_ren=float(cfg["env"]["p_ren"]),
            p_noise=float(cfg["env"]["p_noise"]),
            T_max=int(cfg["env"]["T_max"]),
        ),
        seed=seed,
    )
    obs, _, done, info = env.reset()

    agent_cfg = dict(cfg.get("agent", {}))
    mode = str(agent_cfg.get("type", cfg.get("type", cfg.get("mode", "last")))).lower()
    params = dict(agent_cfg.get("params", cfg.get("params", {})))

    A = int(cfg["env"]["A"])
    L = int(cfg["env"]["L_win"])

    class _PredictLastFSM:
        def __init__(self, A: int):
            self.A = int(A)
            self.prev_obs = 0
        def reset(self, obs: int) -> None:
            self.prev_obs = int(obs)
        def act(self, obs: int) -> int:
            a = self.prev_obs
            self.prev_obs = int(obs)
            return int(a)
        def budget_row(self) -> dict:
            return {"params_bits": 0, "flops_per_step": 1, "memory_bytes": 0}

    agent = _PredictLastFSM(A)
    if mode == "phase":
        from agents.stoa.renewal.agent_fsm import PhaseFSM
        agent = PhaseFSM(A=A, L_win=L)
    elif mode == "ngram":
        from agents.stoa.renewal.agent_fsm import NGramFSM
        agent = NGramFSM(A=A, k=max(0, L - 1))
    elif mode == "vom":
        agent = VOKT(A=A, max_order=int(params.get("max_order", max(0, L - 1))))
    elif mode == "haq":
        from agents.co.agent_renewal import HAQAgent, HAQCfg  # type: ignore
        cfg_kwargs = {"A": A, "L_win": L, **params}
        if "L" in params:
            cfg_kwargs.pop("L_win", None)
        try:
            agent = HAQAgent(HAQCfg(**cfg_kwargs))
        except TypeError:
            cfg_kwargs2 = {"A": A, "L": L, **params}
            agent = HAQAgent(HAQCfg(**cfg_kwargs2))

    agent.reset(obs)  # type: ignore[attr-defined]

    # budget row
    try:
        budget_row = agent.budget_row()  # type: ignore[attr-defined]
        if not isinstance(budget_row, dict):
            raise TypeError
    except Exception:
        budget_row = {"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}
    write_budget_csv(budget_path, [budget_row])

    # OPTIONAL header (harmless; some tooling reads it)
    write_metric_line(metrics_path, {
        "record_type": "header",
        "runner": "renewal",
        "seed": seed,
        "env": cfg["env"],
        "mode": mode,
        "agent": {"type": mode, "params": params},
        "float32": True,
    })

    # --- SINGLE SERIES logging (raw renewal schema) ---
    # Per-step: one line {'t': t, 'cum_reward': cum}
    # Final:    one line {'final_cum_reward': cum}
    cum = 0.0
    for t in range(steps):
        act = agent.act(obs)  # type: ignore[attr-defined]
        obs, r, done, info = env.step(act)
        cum += float(r)

        write_metric_line(metrics_path, {"t": int(t), "cum_reward": float(cum)})

        if done:
            break

    write_metric_line(metrics_path, {"final_cum_reward": float(cum)})

    # quick plot (reads raw just fine); title includes seed
    try:
        from experiments.plotting.plotting import save_quick_plot
        save_quick_plot(metrics_path, plot_path, title=f"Renewal {mode}_s{seed}")
    except Exception:
        pass

    return {"metrics": str(metrics_path), "budget": str(budget_path)}


def main() -> None:
    ap = argparse.ArgumentParser(description="Renewal FSM/CO runner")
    ap.add_argument("--config", type=str, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    paths = run(args.config)

    if args.out:
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        src_m = Path(paths["metrics"])
        src_b = Path(paths["budget"])
        dst_m = out_dir / src_m.name
        dst_b = out_dir / src_b.name
        _safe_copy(src_m, dst_m)
        _safe_copy(src_b, dst_b)


if __name__ == "__main__":
    main()
