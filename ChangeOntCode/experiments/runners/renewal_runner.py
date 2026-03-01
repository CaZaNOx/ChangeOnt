# FILE: experiments/runners/renewal_runner.py
from __future__ import annotations

import argparse, json, random, shutil, time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from agents.stoa.renewal.vo_markov import VOKT
from experiments.logging.logging import write_metric_line, write_budget_csv
from experiments.config_utils import normalize_agent_config, extract_env_params

# CO adapter + core builder
try:
    from agents.co.adapters.renewal_adapter import COAdapterRenewal
    from agents.co.integration.core_builder import build_co_core
    HAS_CO = True
except Exception:
    HAS_CO = False

def _seed_all(seed: int) -> None:
    random.seed(seed)
    if np is not None:
        try: np.random.seed(seed)  # type: ignore[attr-defined]
        except Exception: pass

def _safe_copy(src: Path, dst: Path, retries: int = 12, delay: float = 0.12) -> None:
    if not src.exists(): return
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


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_run_manifest(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

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
        if any(k in loaded for k in ("job", "env", "agent", "run", "logging")):
            job = loaded.get("job", {}) if isinstance(loaded.get("job"), dict) else {}
            env = loaded.get("env", {}) if isinstance(loaded.get("env"), dict) else {}
            run = loaded.get("run", {}) if isinstance(loaded.get("run"), dict) else {}
            agent = loaded.get("agent", {}) if isinstance(loaded.get("agent"), dict) else {}

            env_params = extract_env_params(env)
            if isinstance(env_params, dict):
                cfg["env"].update(env_params)

            cfg["seed"] = int(loaded.get("seed", job.get("seed", cfg["seed"])))
            cfg["steps"] = int(run.get("steps", loaded.get("steps", cfg["env"].get("T_max", cfg["steps"]))))
            cfg["out_dir"] = loaded.get("out_dir", job.get("out_dir", cfg["out_dir"]))
            cfg["mode"] = loaded.get("mode", job.get("mode", cfg["mode"]))

            cfg["agent"] = normalize_agent_config(agent, default_algo=str(cfg.get("mode", "last")).lower())
        else:
            for k, v in loaded.items():
                if k == "env" and isinstance(v, dict):
                    cfg["env"].update(v)
                else:
                    cfg[k] = v

    job = cfg.get("job", {}) if isinstance(cfg.get("job"), dict) else {}
    seed = int(cfg.get("seed", job.get("seed", 7)))
    steps = int(cfg.get("steps", cfg["env"].get("T_max", 1000)))
    out_dir = Path(cfg.get("out_dir", job.get("out_dir", "outputs/renewal_fsm")))
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = out_dir / "metrics.jsonl"
    budget_path  = out_dir / "budget.csv"
    plot_path    = out_dir / "quick_plot.png"
    manifest_path = out_dir / "run_manifest.json"
    started_at = _iso_now()
    status = "failed"
    error: Optional[str] = None

    for p in (metrics_path, budget_path):
        if p.exists():
            p.unlink()
    if plot_path.exists():
        plot_path.unlink()

    try:
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
        aname  = agent_cfg.get("name")
        agent_tag = mode if not aname else f"{mode}:{aname}"

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
        elif mode == "co":
            if not HAS_CO:
                raise RuntimeError("agent=co requested but agents.co.adapters.renewal_adapter is not importable")
            core = build_co_core(params)
            agent = COAdapterRenewal(core=core, name=(aname or "CO_full"))

        # budget row (one-time)
        write_budget_csv(budget_path, [{"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}])

        write_metric_line(metrics_path, {
            "record_type": "header",
            "runner": "renewal",
            "family": "renewal",
            "seed": seed,
            "env": cfg["env"],
            "mode": mode,
            "agent": agent_tag,
            "out_dir": str(out_dir),
            "float32": True,
        })

        # --- single series logging ---
        cum = 0.0
        for t in range(steps):
            if mode == "co":
                sel = None
                try:
                    sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": A, "L_win": L})  # type: ignore[attr-defined]
                except Exception:
                    pass
                if isinstance(sel, dict) and "action" in sel:
                    act = sel["action"]
                else:
                    act = sel
            
                # -- CO debug
                co_policy    = (sel.get("co_policy") if isinstance(sel, dict) else None) or "n/a"
                co_weight    = (float(sel.get("co_weight", 1.0)) if isinstance(sel, dict) else 1.0)
                co_bus_votes = (int(sel.get("co_bus_votes", 0)) if isinstance(sel, dict) else 0)

                write_metric_line(
                    metrics_path,
                    {
                        "metric": "co_debug",
                        "t": t,
                        "co_policy": co_policy,
                        "co_weight": co_weight,
                        "co_bus_votes": co_bus_votes,
                        "agent": agent_tag,
                        **({
                            k: sel[k] for k in (
                                "birth_events","merge_events","split_events","bend_triggers",
                                "birth_count","prototype_count","class_count","cap_hits",
                                "last_d","identity_ok","ghvc_pressure","ghvc_mdl_gain",
                                "debug_header_updates","translator_mask_mode",
                                "translator_mask_blocked","translator_mask_size","translator_mask_blocks_all",
                                "signals","header_update_count","header_update_source","mask_mode","translator_mask",
                            ) if isinstance(sel, dict) and k in sel
                        }),
                    },
                )
            else:
                try:
                    act = agent.act(obs)  # type: ignore[attr-defined]
                except Exception:
                    act = 0

            if isinstance(act, bool):
                act = int(act)
            if not isinstance(act, int):
                act = 0

            obs, r, done, info = env.step(act)
            cum += float(r)

            if mode == "co":
                try:
                    agent.update({"observation": int(obs), "reward": float(r), "done": bool(done), "action": int(act)})  # type: ignore[attr-defined]
                except Exception:
                    pass

            write_metric_line(metrics_path, {"t": int(t), "cum_reward": float(cum)})
            if done:
                break

        write_metric_line(metrics_path, {"final_cum_reward": float(cum)})

        try:
            from experiments.plotting.plotting import save_quick_plot
            save_quick_plot(metrics_path, plot_path, title=f"Renewal {agent_tag}_s{seed}")
        except Exception:
            pass

        status = "succeeded"
        return {"metrics": str(metrics_path), "budget": str(budget_path)}
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        agent_cfg = dict(cfg.get("agent", {}))
        _write_run_manifest(
            manifest_path,
            {
                "family": "renewal",
                "mode": str(agent_cfg.get("type", cfg.get("mode", "last"))).lower(),
                "seed": int(seed),
                "agent_name": str(agent_cfg.get("name") or str(agent_cfg.get("type", ""))),
                "agent_type": str(agent_cfg.get("type", "")),
                "environment_spec": cfg.get("env", {}),
                "runner": "experiments.runners.renewal_runner",
                "out_dir": str(out_dir),
                "started_at": started_at,
                "ended_at": _iso_now(),
                "status": status,
                "error": error,
            },
        )

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
        def _safe_copy_local(src: Path, dst: Path) -> None:
            try: shutil.copy2(src, dst)
            except Exception: pass
        _safe_copy_local(src_m, out_dir / src_m.name)
        _safe_copy_local(src_b, out_dir / src_b.name)

if __name__ == "__main__":
    main()
