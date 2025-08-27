import os, json, random
import numpy as np
from benchmarks.renewal_codebook.env import CodebookRenewalEnvW, EnvCfg
from experiments.logging.jsonl_writer import JSONLWriter
from experiments.logging.metrics import summarize_episode
from baselines.fsm_counter.fsm import FSMCounter
from core.agents.agent_haq import HAQAgent

def run_renewal(cfg):
    seed = int(cfg["seed"])
    random.seed(seed); np.random.seed(seed % (2**32-1))

    # ...
    env_cfg = EnvCfg(
        A=cfg["env"]["A"],
        Lwin=cfg["env"]["L_win"],
        p_ren=cfg["env"]["p_ren"],
        p_merge=cfg["env"]["p_merge"],
        p_split=cfg["env"]["p_split"],
        p_noise=cfg["env"]["p_noise"],
        p_adv=cfg["env"]["p_adv"],
        Tmax=cfg["env"]["T_max"],
        k=cfg["env"]["k"],
        p_loop=cfg["env"].get("p_loop", 0.0),
        p_loop_marker=cfg["env"].get("p_loop_marker", 0.0),
    )
    # ...

    out_dir = cfg["logging"]["out_dir"]
    stem = cfg["logging"]["stem"]
    os.makedirs(out_dir, exist_ok=True)

    agents = []
    for a in cfg["agents"]:
        if a["kind"] == "baseline_fsm":
            agents.append( (a["name"], FSMCounter(env_cfg.A, period=env_cfg.k)) )
        elif a["kind"] == "haq":
            agents.append( (a["name"], HAQAgent(env_cfg.A, seed=seed)) )
        else:
            raise ValueError(f"Unknown agent kind: {a['kind']}")

    for name, agent in agents:
        outpath = os.path.join(out_dir, f"{stem}_{name}.jsonl")
        with JSONLWriter(outpath) as w:
            ep_rows = []
            for ep in range(cfg["episodes"]):
                env = CodebookRenewalEnvW(env_cfg, seed=seed+ep)
                obs, _, done, info = env.reset()
                agent.reset()
                t = 0
                total = 0.0
                flips = []
                events = []

                while not done:
                    act = agent.act(obs, t_global=t)
                    obs, rew, done, info = env.step(act)
                    total += rew
                    
                    if name == "HAQ" and (t % 50 == 0):
                        # Access the last computed costs from agent (you can stash them after act())
                        pass
                    if agent.just_flipped:
                        flips.append(t)
                    if info.get("renewal") or info.get("kth_opportunity"):
                        events.append(t)
                    

                    w.write({
                        "agent": name, "ep": ep, "t": t, "obs": int(obs),
                        "act": int(act), "reward": float(rew),
                        "flip": bool(agent.just_flipped),
                        "event": bool(info.get("renewal") or info.get("kth_opportunity"))
                    })
                    t += 1

                row = summarize_episode(name, ep, flips, events, outpath, cfg["metrics"])
                row["total_reward"] = total
                ep_rows.append(row)

            # print compact aggregate
            flips_list = [r["flips"] for r in ep_rows]
            fdr_list = [r["FDRw"] for r in ep_rows]
            slope_list= [r["slope"] for r in ep_rows]
            print(f"[{name}] flips/ep mean={np.mean(flips_list):.2f}, FDRw mean={np.mean(fdr_list):.3f}, slope mean={np.mean(slope_list):.4f}")