# PATH: experiments/runners/bandit_runner.py
from __future__ import annotations

import argparse, json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

from environments.bandit.bandit import BernoulliBanditEnv
from agents.stoa.bandit.stoa_agent_bandit import UCB1Agent, EpsilonGreedyAgent
from experiments.logging.logging import write_metric_line, write_budget_csv
from experiments.config_utils import normalize_agent_config, extract_env_params
from agents.stoa.bandit.ts import ThompsonSampling
from agents.stoa.bandit.k1_ucb import KLUCB

# CO adapter + core builder
try:
    from agents.co.adapters.bandit_adapter import COAdapterBandit
    from agents.co.integration.core_builder import build_co_core
    HAS_CO = True
except Exception:
    HAS_CO = False

@dataclass
class BanditConfig:
    probs: List[float]
    horizon: int
    agent: Dict[str, Any]
    seed: int = 0
    out: str = "outputs/bandit_ucb"
    mode: Optional[str] = None

def _parse_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        return {}

def _load_config(args: argparse.Namespace) -> BanditConfig:
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            data = json.load(f) if args.config.endswith(".json") else _parse_yaml(f.read())
        job = data.get("job", {}) if isinstance(data.get("job"), dict) else {}
        env = data.get("env", {}) if isinstance(data.get("env"), dict) else {}
        run = data.get("run", {}) if isinstance(data.get("run"), dict) else {}
        agent = data.get("agent", {"type": args.agent.lower(), "params": {}})
        env_params = extract_env_params(env)
        agent = normalize_agent_config(agent, default_algo="ucb1")

        out = data.get("out", data.get("out_dir", job.get("out_dir", "outputs/bandit_ucb")))
        return BanditConfig(
            probs=list(env_params.get("probs", [0.1, 0.2, 0.8])),
            horizon=int(run.get("horizon", env_params.get("horizon", 5000))),
            agent=agent if isinstance(agent, dict) else {"type": str(agent).lower(), "params": {}},
            seed=int(data.get("seed", job.get("seed", 0))),
            out=str(out),
            mode=(data.get("mode", job.get("mode"))),
        )
    # CLI fallback
    probs = [float(x) for x in args.probs.split(",")] if args.probs else [0.1, 0.2, 0.8]
    agent = {"type": args.agent.lower(), "params": {"epsilon": float(args.epsilon)}}
    return BanditConfig(probs=probs, horizon=int(args.horizon), agent=agent, seed=int(args.seed), out=str(args.out))


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_run_manifest(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

def _write_progress(out_dir: Path, t: int) -> None:
    try:
        (out_dir / "progress.json").write_text(json.dumps({"t": t}), encoding="utf-8")
    except Exception:
        pass

def main() -> None:
    ap = argparse.ArgumentParser(description="Bandit runner (UCB1 / ε-greedy / KL-UCB / TS / CO)")
    ap.add_argument("--config", type=str, default=None, help="YAML/JSON config file")
    ap.add_argument("--probs", type=str, default=None, help="Comma-separated arm means (fallback if no config)")
    ap.add_argument("--horizon", type=int, default=5000)
    ap.add_argument("--agent", type=str, default="ucb1")
    ap.add_argument("--epsilon", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=str, default="outputs/bandit_ucb")
    args = ap.parse_args()

    cfg = _load_config(args)
    out_dir = Path(cfg.out); out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "metrics.jsonl"
    budget_path  = out_dir / "budget.csv"
    plot_path    = out_dir / "quick_plot.png"
    manifest_path = out_dir / "run_manifest.json"
    started_at = _iso_now()
    status = "failed"
    error: Optional[str] = None

    for p in (metrics_path, budget_path):
        if p.exists(): p.unlink()
    if plot_path.exists():
        plot_path.unlink()

    try:
        env = BernoulliBanditEnv(cfg.probs, horizon=cfg.horizon)
        env.reset(seed=cfg.seed)

        agent_dict = dict(cfg.agent)
        atype  = str(agent_dict.get("type", "ucb1")).lower()
        aparams = dict(agent_dict.get("params", {}))
        aname  = agent_dict.get("name")
        agent_tag = atype if not aname else f"{atype}:{aname}"

        if atype == "ucb1":
            agent = UCB1Agent(env.n_arms)
        elif atype in ("epsgreedy", "epsilon_greedy"):
            eps = float(aparams.get("epsilon", 0.1))
            agent = EpsilonGreedyAgent(env.n_arms, epsilon=eps, seed=cfg.seed)
        elif atype == "ts":
            agent = ThompsonSampling(env.n_arms)
        elif atype == "kl_ucb":
            agent = KLUCB(env.n_arms, c=float(aparams.get("c", 0.0)))
        elif atype == "co":
            if not HAS_CO:
                raise RuntimeError("CO adapter not available: agents.co.adapters.bandit_adapter")
            core = build_co_core(aparams)
            agent = COAdapterBandit(core=core, name=(aname or "CO"), n_arms=env.n_arms)
        else:
            raise ValueError(f"unknown agent type: {atype}")

        write_metric_line(metrics_path, {
            "record_type": "header",
            "runner": "bandit",
            "family": "bandit",
            "mode": cfg.mode,
            "seed": int(cfg.seed),
            "env": {"probs": cfg.probs, "horizon": int(cfg.horizon)},
            "agent": agent_tag,
            "out_dir": str(out_dir),
        })

        best_mean = max(cfg.probs)
        cum_regret = 0.0
        pulls = [0] * env.n_arms
        budget_rows = []

        t = 0
        done = False
        HEARTBEAT = 500

        while not done:
            if atype == "co":
                # ---- CO path (adapter expects a rich obs dict) ----
                obs = {"family": "bandit", "t": t, "n_arms": env.n_arms}
                sel = None
                try:
                    sel = agent.select(obs)  # adapter may return int or {"action": int}
                except Exception:
                    pass

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

                if isinstance(sel, dict) and "action" in sel:
                    a = int(sel["action"])
                elif isinstance(sel, int):
                    a = sel
                else:
                    a = 0
                _, r, done, info = env.step(a)

                try:
                    agent.update({"action": a, "reward": float(r), "done": bool(done)})
                except Exception:
                    pass

            else:
                # ---- STOA path (native APIs) ----
                if hasattr(agent, "select"):
                    a = int(agent.select())
                elif hasattr(agent, "act"):
                    a = int(agent.act())
                elif hasattr(agent, "choose_action"):
                    a = int(agent.choose_action())
                else:
                    raise RuntimeError(f"Unsupported STOA API for {atype}")

                _, r, done, info = env.step(a)

                try:
                    agent.update(a, r)
                except TypeError:
                    try:
                        agent.update(r)
                    except Exception:
                        pass

            pulls[a] += 1
            t += 1

            inst_pseudo = best_mean - cfg.probs[a]
            if inst_pseudo < 0.0:
                inst_pseudo = 0.0
            cum_regret += inst_pseudo

            write_metric_line(metrics_path, {"metric": "cumulative_regret", "t": t, "value": float(cum_regret)})
            write_metric_line(metrics_path, {"metric": "arm_pull", "t": t, "arm": int(a), "reward": float(r)})

            if (t % HEARTBEAT) == 0:
                _write_progress(out_dir, t)

            budget_rows.append({"t": t, "flops_step": 1, "memory_bytes": 0, "agent": agent_tag})

        write_metric_line(metrics_path, {
            "metric": "pulls_summary", "t": t, "pulls": pulls,
            "best_arm": int(max(range(len(cfg.probs)), key=cfg.probs.__getitem__))
        })

        write_budget_csv(budget_path, budget_rows)

        try:
            from experiments.plotting.plotting import save_quick_plot
            save_quick_plot(metrics_path, plot_path, title=f"Bandit {agent_tag.upper()}")
        except Exception:
            pass
        status = "succeeded"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        _write_run_manifest(
            manifest_path,
            {
                "family": "bandit",
                "mode": cfg.mode,
                "seed": int(cfg.seed),
                "agent_name": str(dict(cfg.agent).get("name") or str(dict(cfg.agent).get("type", ""))),
                "agent_type": str(dict(cfg.agent).get("type", "")),
                "environment_spec": {"probs": cfg.probs, "horizon": int(cfg.horizon)},
                "runner": "experiments.runners.bandit_runner",
                "out_dir": str(out_dir),
                "started_at": started_at,
                "ended_at": _iso_now(),
                "status": status,
                "error": error,
            },
        )

if __name__ == "__main__":
    main()
