# experiments/runners/renewal_runner.py
from __future__ import annotations

import argparse
import json
import random
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

# numpy is optional; we seed it if available
try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    np = None  # type: ignore


# --- ENV (frozen) ---
from experiments.env import CodebookRenewalEnvW, EnvCfg


# --- LOGGING WRITERS (kernel first; local fallbacks kept minimal & compatible) ---

try:
    # Preferred: your kernel JSONL writer
    from kernel.logging import JSONLWriter as KernelWriter  # type: ignore
except Exception:  # pragma: no cover
    KernelWriter = None  # type: ignore


class _LocalJSONLWriter:
    """Tiny JSONL writer with the same surface as KernelWriter(path)."""
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
    """
    Returns (writer, writer_mode_tag).
    Tries kernel writer first; falls back to local.
    """
    if KernelWriter is not None:
        try:
            w = KernelWriter(path)  # type: ignore[call-arg]
            # Some kernel writers expect a separate header call:
            try:
                w.write_header(header)  # type: ignore[attr-defined]
            except Exception:
                # Fallback: write header as first record
                w.write({"record_type": "header", **header})
            return w, "ctor_path_then_header_write"
        except Exception:
            pass

    # Local fallback: header goes in explicitly
    lw = _LocalJSONLWriter(path)
    lw.write_header({"record_type": "header", **header})
    return lw, "local_writer"


# CSV budget write helper (use kernel if available; else a minimal local writer)
try:
    from kernel.logging import write_budget_csv as kernel_write_budget_csv  # type: ignore
except Exception:  # pragma: no cover
    kernel_write_budget_csv = None  # type: ignore


def _write_budget_csv(path: Path, rows: list[dict]) -> None:
    """
    Always writes at least one DATA row (not just a header),
    to avoid 'empty CSV' parity issues.
    """
    if kernel_write_budget_csv is not None:
        # We still guard for header-only behavior by ensuring rows is non-empty.
        if not rows:
            rows = [{"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}]
        try:
            kernel_write_budget_csv(path, rows)  # type: ignore[call-arg]
            return
        except Exception:
            pass

    # Local CSV writer
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


# --- small utilities ---

def _seed_all(seed: int) -> None:
    random.seed(seed)
    if np is not None:
        try:
            np.random.seed(seed)  # type: ignore[attr-defined]
        except Exception:
            pass


def _safe_copy(src: Path, dst: Path, retries: int = 12, delay: float = 0.12) -> None:
    """
    Windows-safe copy with brief retry loop (avoids WinError 32 when a viewer holds the file).
    """
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(retries):
        try:
            shutil.copy2(src, dst)
            return
        except PermissionError:
            time.sleep(delay)
    # final attempt (raise if still locked)
    shutil.copy2(src, dst)


# --- minimal last-FSM baseline (kept for default mode="last") ---

class _PredictLastFSM:
    """
    action_t = obs_{t-1}, with sensible init.
    """
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
        # trivial footprint (example)
        return {"params_bits": 0, "flops_per_step": 1, "memory_bytes": 0}


# --- main run ---

@dataclass
class _RunCfg:
    seed: int
    steps: int
    out_dir: Path
    mode: str


def run(config_path: Optional[str]) -> dict:
    """
    Renewal runner: modes = last | phase | ngram | haq
    Writes:
      - metrics.jsonl (header + step lines)
      - budget.csv    (always includes ≥1 data row)
    Returns dict with paths (for optional copy in __main__).
    """
    # defaults
    cfg = {
        "seed": 7,
        "steps": 1000,
        "env": {"A": 8, "L_win": 6, "p_ren": 0.02, "p_noise": 0.00, "T_max": 1000},
        "out_dir": "outputs/renewal_fsm",
        "mode": "last",  # last | phase | ngram | haq
    }

    # merge from YAML/JSON if provided
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

    mode = str(cfg.get("mode", "last")).lower()
    A = int(cfg["env"]["A"])
    L = int(cfg["env"]["L_win"])

    # agent selection
    agent = _PredictLastFSM(A)
    if mode in ("phase", "ngram", "haq"):
        if mode == "phase":
            from agents.stoa.agent_fsm import PhaseFSM
            agent = PhaseFSM(A=A, L_win=L)
        elif mode == "ngram":
            from agents.stoa.agent_fsm import NGramFSM
            agent = NGramFSM(A=A, k=max(0, L - 1))
        elif mode == "haq":
            # tolerate either L_win or L in HAQCfg
            from agents.co.agent_haq import HAQAgent, HAQCfg
            try:
                agent = HAQAgent(HAQCfg(A=A, L_win=L, ema_alpha=0.1))
            except TypeError:
                agent = HAQAgent(HAQCfg(A=A, L=L, ema_alpha=0.1))

    agent.reset(obs)

    # logging
    metrics_path = out_dir / "metrics.jsonl"
    header = {"runner": "renewal", "seed": seed, "env": cfg["env"], "float32": True, "mode": mode}
    w, writer_mode = _open_writer(metrics_path, header)

    # budget row (GUARANTEED data row)
    try:
        budget_row = agent.budget_row()  # type: ignore[attr-defined]
        if not isinstance(budget_row, dict):
            raise TypeError("budget_row must return dict")
    except Exception:
        budget_row = {"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}
    budget_csv = out_dir / "budget.csv"
    _write_budget_csv(budget_csv, [budget_row])

    # main loop
    cum = 0.0
    for t in range(steps):
        act = agent.act(obs)
        obs, r, done, info = env.step(act)
        cum += float(r)
        # tolerant to info["obs"] missing
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

    # Optional safe copy to a user-provided directory
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
