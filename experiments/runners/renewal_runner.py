# experiments/runners/renewal_runner.py
from __future__ import annotations
import argparse, json, random, shutil
from pathlib import Path
from typing import Optional

from experiments.env import CodebookRenewalEnvW, EnvCfg

# Prefer your project writers; fallback to a minimal local writer if absent.
Writer = None
try:
    from kernel.logging import JSONLWriter as Writer  # type: ignore
except Exception:
    pass
if Writer is None:
    try:
        from experiments.logging import JSONLWriter as Writer  # type: ignore
    except Exception:
        pass

class _LocalJSONLWriter:
    def __init__(self, path: Path, header: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.f = open(path, "w", encoding="utf-8")
        hdr = dict(header); hdr["record_type"] = "header"
        self.f.write(json.dumps(hdr) + "\n")
    def write(self, rec: dict):
        if "record_type" not in rec:
            rec["record_type"] = "step"
        self.f.write(json.dumps(rec) + "\n")
    def write_line(self, rec: dict):  # compat
        self.write(rec)
    def close(self):
        try: self.f.close()
        except Exception: pass

def _seed_all(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except Exception:
        pass

# Simple finite Mealy baseline (kept for backwards-compat)
class _PredictLastFSM:
    """
    Deterministic Mealy FSM:
      state = last observed symbol (finite set {0..A-1})
      λ(q, x) = x   (predict next == current obs)
      δ(q, x) = x
    """
    def __init__(self, A: int):
        self.A = int(A); self.state = 0
    def reset(self, init_obs: int) -> None:
        self.state = int(init_obs)
    def act(self, obs: int) -> int:
        self.state = int(obs); return self.state
    def transition(self, q: int, x: int) -> int: return int(x)
    def output(self, q: int, x: int) -> int: return int(x)
    def budget_row(self) -> dict:
        return {"params_bits": self.A, "flops_per_step": 1, "memory_bytes": self.A}

def _open_writer(path: Path, header: dict):
    """
    Create a JSONL writer compatible with your logging.
    Tries Writer(path, header) -> Writer(path)+write(header) -> local writer.
    Returns (writer, mode_str).
    """
    if Writer is not None:
        try:
            w = Writer(path, header)  # type: ignore[call-arg]
            return w, "ctor_path_header"
        except TypeError:
            try:
                w = Writer(path)  # type: ignore[call-arg]
                hdr = {"record_type": "header", **header}
                if hasattr(w, "write"):
                    w.write(hdr)  # type: ignore[attr-defined]
                elif hasattr(w, "write_line"):
                    w.write_line(hdr)  # type: ignore[attr-defined]
                else:
                    raise TypeError("Writer has neither write nor write_line")
                return w, "ctor_path_then_header_write"
            except Exception:
                pass
        except Exception:
            pass
    return _LocalJSONLWriter(path, header), "local_writer"

def run(config_path: Optional[str]) -> dict:
    # Load config (YAML or JSON). If none, defaults are fine.
    cfg = {
        "seed": 7,
        "steps": 1000,
        "mode": "last",  # last | phase | ngram
        "env": {"A": 8, "L_win": 6, "p_ren": 0.02, "p_noise": 0.00, "T_max": 1000},
        "out_dir": "outputs/renewal_fsm"
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
        seed=seed
    )
    obs, _, done, info = env.reset()

    # --- choose FSM baseline ---
    mode = str(cfg.get("mode", "last")).lower()
    A = int(cfg["env"]["A"]); L = int(cfg["env"]["L_win"])
    agent = _PredictLastFSM(A)  # default

    try:
        from agents.stoa.agent_fsm import PhaseFSM, NGramFSM  # reuse your file
        if mode == "phase":
            agent = PhaseFSM(A=A, L_win=L)
        elif mode == "ngram":
            agent = NGramFSM(A=A, k=max(0, L-1))
    except Exception:
        # keep default _PredictLastFSM if import fails
        pass

    agent.reset(obs)

    # JSONL open with provenance header
    log_path = out_dir / "metrics.jsonl"
    header = {"runner": "renewal", "seed": seed, "env": cfg["env"], "float32": True, "mode": mode}
    w, writer_mode = _open_writer(log_path, header)

    # Budget snapshot (CSV if kernel exposes it; else write as JSONL budget record)
    budget_row = agent.budget_row() if hasattr(agent, "budget_row") else {"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}
    budget_csv = out_dir / "budget.csv"
    try:
        from kernel.logging import write_budget_csv as _wb  # type: ignore
        _wb(budget_csv, [budget_row])
    except Exception:
        if hasattr(w, "write"):
            w.write({"record_type": "budget", **budget_row})
        elif hasattr(w, "write_line"):
            w.write_line({"record_type": "budget", **budget_row})

    cum = 0.0
    for t in range(steps):
        if done:
            break
        act = agent.act(obs)
        obs, r, done, info = env.step(act)
        cum += float(r)
        rec = {"t": int(t), "obs": int(obs), "act": int(act), "reward": float(r), "cum_reward": float(cum)}
        if hasattr(w, "write"):
            w.write(rec)
        elif hasattr(w, "write_line"):
            w.write_line(rec)

    if hasattr(w, "close"):
        w.close()
            # quick plot (same pipeline as bandit/maze)
    try:
        from kernel.plotting import save_quick_plot
        plot_path = out_dir / "quick_plot.png"
        save_quick_plot(log_path, plot_path, title=f"Renewal {str(mode).upper()}")
    except Exception:
        pass


    return {"metrics": str(log_path), "budget": str(budget_csv), "writer_mode": writer_mode}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default=None)
    ap.add_argument("--out", type=str, default=None)  # optional relocation
    args = ap.parse_args()
    paths = run(args.config)
    # Relocate outputs if --out given (Windows-safe copy; skip if same path)
    if args.out:
        out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
        src_m = Path(paths["metrics"]).resolve()
        src_b = Path(paths["budget"]).resolve()
        dst_m = (out_dir / src_m.name).resolve()
        dst_b = (out_dir / src_b.name).resolve()

        if src_m != dst_m:
            try: shutil.copy2(src_m, dst_m)
            except PermissionError: pass
        if src_b.exists() and src_b != dst_b:
            try: shutil.copy2(src_b, dst_b)
            except PermissionError: pass

        paths["metrics"] = str(dst_m)
        paths["budget"]  = str(dst_b)

    print(json.dumps(paths))

if __name__ == "__main__":
    main()
