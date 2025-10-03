from __future__ import annotations

import argparse
import json
import random
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# numpy optional
try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

from environments.renewal.env import CodebookRenewalEnvW, EnvCfg

try:
    from experiments.logging.logging import JSONLWriter as KernelWriter  # type: ignore
except Exception:
    KernelWriter = None  # type: ignore


class _LocalJSONLWriter:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._f = open(path, "w", encoding="utf-8")

    def write_header(self, hdr: dict) -> None:
        self._f.write(json.dumps(hdr) + "\n")
        self._f.flush()

    def write(self, rec: dict) -> None:
        self._f.write(json.dumps(rec) + "\n")

    def close(self) -> None:
        try:
            self._f.flush()
        finally:
            self._f.close()


def _open_writer(path: Path, header: dict) -> Tuple[object, str]:
    if KernelWriter is not None:
        try:
            w = KernelWriter(path)  # type: ignore[call-arg]
            try:
                w.write_header(header)  # type: ignore[attr-defined]
            except Exception:
                w.write({"record_type": "header", **header})
            return w, "ctor_path_then_header_write"
        except Exception:
            pass
    lw = _LocalJSONLWriter(path)
    lw.write_header({"record_type": "header", **header})
    return lw, "local_writer"


try:
    from experiments.logging.logging import write_metric_line, write_budget_csv
except Exception:
    kernel_write_budget_csv = None  # type: ignore


def _write_budget_csv(path: Path, rows: list[dict]) -> None:
    if write_budget_csv is not None:
        if not rows:
            rows = [{"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}]
        try:
            write_budget_csv(path, rows)  # type: ignore[call-arg]
            return
        except Exception:
            pass
    import csv
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        rows = [{"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}]
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)


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


@dataclass
class _RunCfg:
    seed: int
    steps: int
    out_dir: Path
    mode: str
    agent: Dict[str, Any]


def run(config_path: Optional[str]) -> dict:
    cfg: dict = {
        "seed": 7,
        "steps": 1000,
        "env": {"A": 8, "L_win": 6, "p_ren": 0.02, "p_noise": 0.00, "T_max": 1000},
        "out_dir": "outputs/renewal_fsm",
        "mode": "last",
        "agent": {"type": "last", "params": {}}
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

    # agent selection (mapping preferred; still honor "mode")
    agent_cfg = dict(cfg.get("agent", {}))
    mode = str(agent_cfg.get("type", cfg.get("mode", "last"))).lower()
    params = dict(agent_cfg.get("params", {}))

    A = int(cfg["env"]["A"])
    L = int(cfg["env"]["L_win"])

    agent = _PredictLastFSM(A)
    if mode == "phase":
        from agents.stoa.agent_fsm import PhaseFSM
        agent = PhaseFSM(A=A, L_win=L)
    elif mode == "ngram":
        from agents.stoa.agent_fsm import NGramFSM
        agent = NGramFSM(A=A, k=max(0, L - 1))
    elif mode == "haq":
        from agents.co.agent_renewal import HAQAgent, HAQCfg
        # build HAQCfg with env defaults, allow params override (supports L or L_win)
        cfg_kwargs = {"A": A, "L_win": L, **params}
        if "L" in params:
            cfg_kwargs.pop("L_win", None)
        try:
            agent = HAQAgent(HAQCfg(**cfg_kwargs))
        except TypeError:
            # try the alternative naming
            cfg_kwargs2 = {"A": A, "L": L, **params}
            agent = HAQAgent(HAQCfg(**cfg_kwargs2))

    agent.reset(obs)

    metrics_path = out_dir / "metrics.jsonl"
    header = {"runner": "renewal", "seed": seed, "env": cfg["env"], "float32": True, "mode": mode, "agent": agent_cfg}
    w, writer_mode = _open_writer(metrics_path, header)

    try:
        budget_row = agent.budget_row()  # type: ignore[attr-defined]
        if not isinstance(budget_row, dict):
            raise TypeError
    except Exception:
        budget_row = {"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}
    budget_csv = out_dir / "budget.csv"
    _write_budget_csv(budget_csv, [budget_row])

    try:
        from experiments.plotting.plotting import save_quick_plot
        save_quick_plot(metrics_path, out_dir / "quick_plot.png", title=f"Renewal {mode}")
    except Exception:
        pass

    cum = 0.0
    for t in range(steps):
        act = agent.act(obs)  # type: ignore[attr-defined]
        obs, r, done, info = env.step(act)
        cum += float(r)
        obs_log = int(info.get("obs", obs)) if isinstance(info, dict) else int(obs)
        w.write({"t": t, "obs": obs_log, "act": int(act), "reward": float(r), "cum_reward": float(cum)})
        if done:
            break

    try:
        w.close()
    except Exception:
        pass

    return {"metrics": str(metrics_path), "budget": str(budget_csv), "writer_mode": writer_mode}


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
        paths["metrics"] = str(dst_m)
        paths["budget"] = str(dst_b)

    print(json.dumps(paths))


if __name__ == "__main__":
    main()
