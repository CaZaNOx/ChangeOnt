# PATH: experiments/runners/bandit_runner.py
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any

from environments.bandit.bandit import BernoulliBanditEnv
from agents.stoa.bandit.stoa_agent_bandit import UCB1Agent, EpsilonGreedyAgent
from experiments.logging.logging import write_metric_line, write_budget_csv
from agents.stoa.bandit.ts import ThompsonSampling
from agents.stoa.bandit.k1_ucb import KLUCB

# ---- CO adapter (uses your adapter + a small core builder) ----
try:
    from agents.co.adapters.bandit_adapter import COAdapterBandit  # your class
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
        env = data.get("env", {})
        agent = data.get("agent", {"type": args.agent.lower(), "params": {}})
        out = data.get("out", "outputs/bandit_ucb")
        return BanditConfig(
            probs=list(env.get("probs", [0.1, 0.2, 0.8])),
            horizon=int(env.get("horizon", 5000)),
            agent=agent if isinstance(agent, dict) else {"type": str(agent).lower(), "params": {}},
            seed=int(data.get("seed", 0)),
            out=str(out),
        )
    # CLI fallback
    probs = [float(x) for x in args.probs.split(",")] if args.probs else [0.1, 0.2, 0.8]
    agent = {"type": args.agent.lower(), "params": {"epsilon": float(args.epsilon)}}
    return BanditConfig(probs=probs, horizon=int(args.horizon), agent=agent, seed=int(args.seed), out=str(args.out))

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

    for p in (metrics_path, budget_path):
        if p.exists(): p.unlink()

    env = BernoulliBanditEnv(cfg.probs, horizon=cfg.horizon)
    env.reset(seed=cfg.seed)

    agent_dict = dict(cfg.agent)
    atype = str(agent_dict.get("type", "ucb1")).lower()
    aparams = dict(agent_dict.get("params", {}))
    aname = agent_dict.get("name")
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
        core = build_co_core(aparams)  # passes header/elements/math_policy if your core supports it
        agent = COAdapterBandit(core=core, name=(aname or "CO"))
    else:
        raise ValueError(f"unknown agent type: {atype}")

    write_metric_line(metrics_path, {
        "record_type": "header",
        "runner": "bandit",
        "seed": int(cfg.seed),
        "env": {"probs": cfg.probs, "horizon": int(cfg.horizon)},
        "agent": agent_tag
    })

    best_mean = max(cfg.probs)
    cum_regret = 0.0
    pulls = [0] * env.n_arms
    budget_rows = []

    t = 0
    done = False
    HEARTBEAT = 500

    while not done:
        # Your adapter returns a dict with "action"; support both dict & int
        sel = None
        try:
            sel = agent.select({"t": t, "n_arms": env.n_arms})  # type: ignore[attr-defined]
        except Exception:
            pass
        if isinstance(sel, dict) and "action" in sel:
            a = int(sel["action"])
        elif isinstance(sel, int):
            a = sel
        else:
            a = 0  # safe default

        _, r, done, info = env.step(a)

        # Your adapter expects a dict on update
        try:
            agent.update({"action": a, "reward": r, "done": done})  # type: ignore[attr-defined]
        except Exception:
            pass

        pulls[a] += 1
        t += 1

        inst_pseudo = best_mean - cfg.probs[a]
        if inst_pseudo < 0.0: inst_pseudo = 0.0
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

if __name__ == "__main__":
    main()