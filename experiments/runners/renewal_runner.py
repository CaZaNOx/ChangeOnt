from future import annotations  
import os  
from typing import Dict, List, Tuple

from benchmarks.renewal_codebook import CodebookRenewalEnvW, RenewalConfig  
from core.agents.agent_haq import EnhancedHAQAgent, HAQConfig  
from baselines.fsm_counter import FSMCounterBaseline  
from experiments.logging import JSONLWriter, fdr_windowed, theil_sen_slope, au_regret_window

def _run_policy(env: CodebookRenewalEnvW, policy, episodes: int, out_steps_path: str) -> Tuple[List[List[float]], List[List[int]], List[List[int]]]:  
    """  
    Returns:  
    rewards_per_ep: list of per-episode reward series  
    flips_per_ep: list of per-episode flip times (only for agents with .flips; else empty)  
    events_per_ep: list of per-episode event times (renewals or kth opportunities)  
    """  
    writer = JSONLWriter(out_steps_path)  
    rewards_all = []  
    flips_all = []  
    events_all = []


    for ep in range(episodes):
        # reset env + policy
        env.__init__(env.cfg)  # re-seed per our simple toy (same seed base)
        if hasattr(policy, "reset"):
            policy.reset()
        t = 0
        rewards = []
        flips = []
        events = []
        obs, rew, done, info = env.reset()
        # initial line
        row = {"ep": ep, "t": 0, "obs": int(obs), "act": 0, "reward": float(rew),
            "flip": False, "event": bool(info["renewal"] or info["kth_opportunity"])}
        writer.write(row)
        if row["event"]:
            events.append(0)
        while not done:
            act = policy.act(obs, t_global=t) if hasattr(policy, "act") else 0
            obs, rew, done, info = env.step(int(act))
            rewards.append(float(rew))
            is_flip = False
            if hasattr(policy, "flips"):
                if policy.flips and policy.flips[-1] == t:
                    is_flip = True
                    flips.append(t)
            is_event = bool(info["renewal"] or info["kth_opportunity"])
            if is_event and info["event_time"] is not None:
                events.append(int(info["event_time"]))
            writer.write({
                "ep": ep, "t": t+1, "obs": int(obs), "act": int(act), "reward": float(rew),
                "flip": is_flip, "event": is_event
            })
            t += 1
        rewards_all.append(rewards)
        flips_all.append(flips)
        events_all.append(events)
    writer.close()
    return rewards_all, flips_all, events_all

def run_renewal_experiment(cfg: Dict) -> Dict:  
    # build env  
    rcfg = RenewalConfig(  
    A=cfg["renewal"]["A"], L_win=cfg["renewal"]["L_win"],  
    p_ren=cfg["renewal"]["p_ren"], p_merge=cfg["renewal"]["p_merge"],  
    p_split=cfg["renewal"]["p_split"], p_noise=cfg["renewal"]["p_noise"],  
    p_adv=cfg["renewal"]["p_adv"], T_max=cfg["renewal"]["T_max"],  
    k=cfg["renewal"]["k"], seed=cfg["seed"]  
    )  
    env = CodebookRenewalEnvW(rcfg)  
    episodes = int(cfg["episodes"])


    out_dir = cfg["logging"]["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    # run baseline FSM
    fsm = FSMCounterBaseline(k_cap=cfg.get("agents", {}).get("fsm", {}).get("k_cap", 24))
    fsm_rewards, fsm_flips, fsm_events = _run_policy(env, fsm, episodes, os.path.join(out_dir, "steps_fsm.jsonl"))

    # run HAQ
    haq = EnhancedHAQAgent(A=rcfg.A, config=HAQConfig(seed=31415))
    haq_rewards, haq_flips, haq_events = _run_policy(env, haq, episodes, os.path.join(out_dir, "steps_haq.jsonl"))

    # per-episode metrics (HAQ vs FSM)
    delta = int(cfg["logging"]["delta_align"])
    W = int(cfg["logging"]["window"])
    episodes_rows = []
    for ep in range(episodes):
        flips = haq_flips[ep]
        events = haq_events[ep]
        fdr = fdr_windowed(flips, events, delta=delta)

        # slope on cumulative reward (HAQ)
        ys = []
        cum = 0.0
        for r in haq_rewards[ep]:
            cum += r
            ys.append(cum)
        xs = list(range(1, len(ys)+1))
        slope = theil_sen_slope(xs, ys, max_pairs=400) if ys else 0.0

        # AUReg_window vs FSM
        au = au_regret_window(
            baseline_rewards=fsm_rewards[ep],
            agent_rewards=haq_rewards[ep],
            window=W
        )
        episodes_rows.append({
            "ep": ep,
            "flips": int(len(flips)),
            "FDR_windowed": float(fdr),
            "slope_window": float(slope),
            "AUReg_window": float(au)
        })

    # write aggregate summary
    summary_path = os.path.join(out_dir, "episodes_summary.jsonl")
    writer = JSONLWriter(summary_path)
    for row in episodes_rows:
        writer.write(row)
    writer.close()

    return {
        "out_dir": out_dir,
        "episodes": episodes_rows
    }


-----


from **future** import annotations  
from typing import Dict, Any, List

from benchmarks.renewal_codebook.env import CodebookRenewalEnvW, RenCfg  
from baselines.fsm_counter.fsm import FSMCounter

def run_renewal(cfg: Dict[str, Any],  
agent_name: str = "fsm",  
episodes: int = 5,  
seed: int = 1729,  
writer=None) -> Dict[str, Any]:  
"""  
Minimal runner for the renewal plant.  
agent_name: "fsm" (baseline) or "random"  
"""  
rcfg = RenCfg(  
A=cfg.get("A", 6),  
p_ren=cfg.get("p_ren", 0.08),  
p_merge=cfg.get("p_merge", 0.25),  
p_split=cfg.get("p_split", 0.15),  
p_noise=cfg.get("p_noise", 0.02),  
T_max=cfg.get("T_max", 600),  
k=cfg.get("k", 12),  
seed=seed,  
)  
env = CodebookRenewalEnvW(rcfg)

```
if agent_name.lower() == "fsm":
    agent = FSMCounter(period=cfg.get("period", 12))
else:
    class RandomAgent:
        def reset(self): pass
        def act(self, obs): 
            # never exit (makes AUReg=0), but deterministic behavior
            return 0
    agent = RandomAgent()

returns: List[float] = []
for ep in range(int(episodes)):
    obs, rew, done, info = env.reset()
    agent.reset()
    t = 0; G = 0.0
    while not done:
        act = agent.act(obs)
        obs, r, done, info = env.step(act)
        G += r
        if writer is not None:
            writer.write_step({"ep":ep,"t":t,"obs":int(obs),"act":int(act),"reward":float(r)})
        t += 1
    returns.append(G)
    if writer is not None:
        writer.write_episode({"ep":ep,"return":float(G)})
return {"episodes": len(returns), "mean_return": sum(returns)/max(1,len(returns))}