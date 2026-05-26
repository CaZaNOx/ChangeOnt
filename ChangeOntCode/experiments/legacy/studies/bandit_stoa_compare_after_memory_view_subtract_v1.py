from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from environments.bandit.bandit import BernoulliBanditEnv
from agents.stoa.bandit.stoa_agent_bandit import UCB1Agent, EpsilonGreedyAgent
from agents.stoa.bandit.ts import ThompsonSampling
from agents.stoa.bandit.k1_ucb import KLUCB
from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit

OUT = Path("outputs/bandit_stoa_compare_after_memory_view_subtract_v1.json")


def _make_agent(agent_name: str, n_arms: int, seed: int):
    name = agent_name.lower()
    if name == "ucb1":
        return UCB1Agent(n_arms)
    if name == "ts":
        return ThompsonSampling(n_arms)
    if name == "kl_ucb":
        return KLUCB(n_arms)
    if name == "epsgreedy":
        return EpsilonGreedyAgent(n_arms, epsilon=0.1, seed=seed)
    if name == "co":
        core = build_co_core({})
        return COAdapterBandit(core=core, n_arms=n_arms)
    raise ValueError(agent_name)


def _run_one(agent_name: str, probs: list[float], horizon: int, seed: int) -> dict:
    env = BernoulliBanditEnv(probs, horizon=horizon)
    env.reset(seed=seed)
    agent = _make_agent(agent_name, env.n_arms, seed)
    best_mean = max(probs)
    regret = 0.0
    actions = []
    rewards = []
    for t in range(horizon):
        if agent_name == "co":
            sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
            act = int(sel["action"]) if isinstance(sel, dict) and "action" in sel else int(sel or 0)
            _, r, done, _ = env.step(act)
            agent.update({"action": act, "reward": float(r), "done": bool(done)})
        else:
            if hasattr(agent, "select"):
                act = int(agent.select())
            elif hasattr(agent, "act"):
                act = int(agent.act())
            elif hasattr(agent, "choose_action"):
                act = int(agent.choose_action())
            else:
                raise RuntimeError(f"unsupported API for {agent_name}")
            _, r, done, _ = env.step(act)
            try:
                agent.update(act, r)
            except TypeError:
                try:
                    agent.update(r)
                except Exception:
                    pass
        regret += max(0.0, best_mean - probs[act])
        actions.append(int(act))
        rewards.append(float(r))
        if done:
            break
    return {
        "final_regret": regret,
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "first_20_actions": actions[:20],
    }


def main() -> None:
    horizon = 1000
    seeds = [1, 2, 3, 4, 5]
    tasks = {
        "confusable_stationary": [0.46, 0.50, 0.54],
        "clarified_stationary": [0.20, 0.50, 0.80],
    }
    agents = ["co", "ucb1", "ts", "kl_ucb", "epsgreedy"]
    results = {
        "study": "bandit_stoa_compare_after_memory_view_subtract_v1",
        "horizon": horizon,
        "seeds": seeds,
        "tasks": {},
    }
    for task_name, probs in tasks.items():
        task_out = {"probs": probs, "agents": {}}
        for agent_name in agents:
            runs = [_run_one(agent_name, probs, horizon, seed) for seed in seeds]
            task_out["agents"][agent_name] = {
                "mean_final_regret": mean(r["final_regret"] for r in runs),
                "mean_reward": mean(r["mean_reward"] for r in runs),
                "runs": runs,
            }
        ranking = sorted(
            ((a, float(task_out["agents"][a]["mean_final_regret"])) for a in agents),
            key=lambda kv: kv[1],
        )
        task_out["regret_ranking"] = ranking
        results["tasks"][task_name] = task_out
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
