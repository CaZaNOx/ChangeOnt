from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from environments.bandit.bandit import BernoulliBanditEnv
from agents.stoa.bandit.stoa_agent_bandit import UCB1Agent, EpsilonGreedyAgent
from agents.stoa.bandit.ts import ThompsonSampling
from agents.stoa.bandit.k1_ucb import KLUCB
from agents.co.adapters.bandit_adapter import COAdapterBandit
from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    assert_valid_co_rollout,
    build_validated_co_core,
    load_co_manifest_params,
)

OUT = Path("outputs/bandit_stoa_compare_canonical_v2.json")
STUDY = "bandit_stoa_compare_canonical_v2"
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)


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
        core = build_validated_co_core(
            dict(CANONICAL_PARAMS),
            study_name=STUDY,
            manifest_path=DEFAULT_CANONICAL_MANIFEST,
            agent_name=DEFAULT_CANONICAL_AGENT_NAME,
        )
        return COAdapterBandit(core=core, n_arms=n_arms)
    raise ValueError(agent_name)


def _run_one(agent_name: str, probs: List[float], horizon: int, seed: int) -> Dict[str, Any]:
    env = BernoulliBanditEnv(probs, horizon=horizon)
    env.reset(seed=seed)
    agent = _make_agent(agent_name, env.n_arms, seed)
    best_mean = max(probs)
    regret = 0.0
    actions: List[int] = []
    rewards: List[float] = []
    signal_bus_votes: List[int] = []
    co_policies: List[str] = []
    for t in range(horizon):
        if agent_name == "co":
            sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
            if isinstance(sel, dict):
                act = int(sel.get("action", 0))
                signal_bus_votes.append(int(sel.get("signal_bus_votes", 0) or 0))
                co_policies.append(str(sel.get("co_policy", "bandit:safe_default")))
            else:
                act = int(sel or 0)
                signal_bus_votes.append(0)
                co_policies.append("bandit:safe_default")
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
    if agent_name == "co":
        assert_valid_co_rollout(study_name=STUDY, signal_bus_votes=signal_bus_votes, co_policies=co_policies)
    return {
        "final_regret": regret,
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "first_20_actions": actions[:20],
        **(
            {
                "signal_bus_votes_first20": signal_bus_votes[:20],
                "co_policy_first20": co_policies[:20],
                "co_votes_nonzero_steps": sum(1 for v in signal_bus_votes if v != 0),
            }
            if agent_name == "co"
            else {}
        ),
    }


def main() -> None:
    horizon = 400
    seeds = [1, 2, 3]
    tasks = {
        "easy_stationary": [0.10, 0.20, 0.80],
        "clarified_stationary": [0.20, 0.50, 0.80],
        "confusable_stationary": [0.46, 0.50, 0.54],
    }
    agents = ["co", "ucb1", "ts", "kl_ucb", "epsgreedy"]
    canonical_core = build_validated_co_core(
        dict(CANONICAL_PARAMS),
        study_name=STUDY,
        manifest_path=DEFAULT_CANONICAL_MANIFEST,
        agent_name=DEFAULT_CANONICAL_AGENT_NAME,
    )
    results: Dict[str, Any] = {
        "study": STUDY,
        "status": "executed",
        "manifest_path": DEFAULT_CANONICAL_MANIFEST.as_posix(),
        "co_agent_name": DEFAULT_CANONICAL_AGENT_NAME,
        "co_element_names": [e.__class__.__name__ for e in canonical_core.elements],
        "horizon": horizon,
        "seeds": seeds,
        "tasks": {},
        "judgment": "Executed on the canonical CO manifest with a hard non-empty-core guard and a rollout guard against all-safe-default/no-vote runs.",
    }
    for task_name, probs in tasks.items():
        task_out: Dict[str, Any] = {"probs": probs, "agents": {}}
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
