# PATH: experiments/runners/bandit_runner.py
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from environments.bandit.bandit import BernoulliBanditEnv
from kernel.logging import write_metric_line, write_budget_csv

# ---- simple STOA agents (inline, deterministic tie-breaks) ----

class UCB1Agent:
    def __init__(self, n_arms: int):
        self.n = n_arms
        self.counts = [0] * n_arms
        self.values = [0.0] * n_arms
        self.t = 0

    def select(self) -> int:
        # play each arm once first
        for a in range(self.n):
            if self.counts[a] == 0:
                return a
        import math
        self.t += 1
        ucb_vals = [
            self.values[a] + (2.0 * math.log(self.t) / self.counts[a]) ** 0.5
            for a in range(self.n)
        ]
        best = max(ucb_vals)
        for a in range(self.n):
            if ucb_vals[a] == best:
                return a
        return 0

    def update(self, a: int, r: float) -> None:
        self.counts[a] += 1
        n = self.counts[a]
        q = self.values[a]
        self.values[a] = q + (r - q) / n


class EpsilonGreedyAgent:
    def __init__(self, n_arms: int, epsilon: float = 0.1, seed: int = 0):
        from random import Random
        self.n = n_arms
        self.eps = float(epsilon)
        self.counts = [0] * n_arms
        self.values = [0.0] * n_arms
        self.rng = Random(seed)

    def select(self) -> int:
        if self.rng.random() < self.eps:
            return self.rng.randrange(self.n)
        best = max(self.values)
        for a in range(self.n):
            if self.values[a] == best:
                return a
        return 0

    def update(self, a: int, r: float) -> None:
        self.counts[a] += 1
        n = self.counts[a]
        q = self.values[a]
        self.values[a] = q + (r - q) / n


# ---- CO adapter (seeded & deterministic) ----
try:
    from agents.co.agent_bandit import COBanditAgent, COBanditCfg
    HAS_CO = True
except Exception:
    HAS_CO = False


# ---- config dataclass ----
@dataclass
class BanditConfig:
    probs: List[float]
    horizon: int
    agent: str = "ucb1"           # 'ucb1' | 'epsgreedy' | 'haq'
    epsilon: float = 0.1          # only for epsgreedy
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
        agent = data.get("agent", {})
        out = data.get("out", "outputs/bandit_ucb")
        return BanditConfig(
            probs=list(env.get("probs", [0.1, 0.2, 0.8])),
            horizon=int(env.get("horizon", 5000)),
            agent=str(agent.get("type", data.get("agent", "ucb1"))).lower(),
            epsilon=float(agent.get("params", {}).get("epsilon", 0.1)),
            seed=int(data.get("seed", 0)),
            out=str(out),
        )
    probs = [float(x) for x in args.probs.split(",")] if args.probs else [0.1, 0.2, 0.8]
    return BanditConfig(
        probs=probs, horizon=int(args.horizon), agent=args.agent.lower(),
        epsilon=float(args.epsilon), seed=int(args.seed), out=str(args.out),
    )


def _write_progress(out_dir: Path, t: int) -> None:
    try:
        (out_dir / "progress.json").write_text(json.dumps({"t": t}), encoding="utf-8")
    except Exception:
        pass


def main() -> None:
    ap = argparse.ArgumentParser(description="Bandit runner (UCB1 / ε-greedy / CO-HAQ)")
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

    # ---- truncate old files to avoid appends across runs ----
    if metrics_path.exists():
        metrics_path.unlink()
    if budget_path.exists():
        budget_path.unlink()

    env = BernoulliBanditEnv(cfg.probs, horizon=cfg.horizon)
    env.reset(seed=cfg.seed)

    if cfg.agent == "ucb1":
        agent = UCB1Agent(env.n_arms); agent_tag = "ucb1"
    elif cfg.agent in ("epsgreedy", "epsilon_greedy"):
        agent = EpsilonGreedyAgent(env.n_arms, epsilon=cfg.epsilon, seed=cfg.seed); agent_tag = "epsgreedy"
    elif cfg.agent == "haq":
        if not HAS_CO:
            raise RuntimeError("CO adapter not available: agents.co.agent_bandit")
        agent = COBanditAgent(COBanditCfg(n_arms=env.n_arms, seed=cfg.seed, ema_alpha=0.0)); agent_tag = "haq"
    else:
        raise ValueError(f"unknown agent type: {cfg.agent}")

    # ---- header for segmentation & provenance ----
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
        a = agent.select()
        _, r, done, info = env.step(a)
        agent.update(a, r)
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
        from kernel.plotting import save_quick_plot
        save_quick_plot(metrics_path, plot_path, title=f"Bandit {agent_tag.upper()}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
