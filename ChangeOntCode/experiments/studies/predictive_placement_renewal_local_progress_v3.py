from statistics import mean
from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from environments.renewal.env import EnvCfg, CodebookRenewalEnvW


def _core(progress_override=None):
    cfg={
        "name":"predictive_renewal_progress_v3",
        "elements":{"candidate_surface":{"enabled":True},"commitment_surface":{"enabled":True,"collapse_enabled":False}},
        "primitives":{"signal_bus":{},"ngram_model":{}},
        "problem_contract":{"actions":{"count":8},"observation_channels":["symbol_observation","reward_feedback","trace_history"],"task_anchor":{"kind":"predictive_reward_alignment","provided_externally":True},"timescale_profile":{"horizon_fixity":"mixed","drift":"unknown"},"observability_profile":{"state":"direct","outcome":"direct","constraints":"unknown"},"reversibility_profile":{"action_reversibility":"reversible","commitment_cost":"medium"}},
    }
    if progress_override is not None:
        cfg["study_overrides"]={"environment_basis_override":{"enabled":True,"authority":"study_override","axes":{"local_progress_reliability":progress_override}}}
    return build_co_core(cfg)


def run_trial(noise, p_ren, shape, seed, horizon=140):
    env=CodebookRenewalEnvW(EnvCfg(A=8,L_win=6,p_ren=p_ren,p_noise=noise,T_max=horizon), seed=seed)
    obs,_,done,_=env.reset()
    core=_core(shape); ag=COAdapterRenewal(core=core)
    rewards=[]; actions=[]
    warmup=[0,1,2,3,4,5]
    for a in warmup:
        obs,r,done,_=env.step(a); ag.update({"action":a,"reward":float(r),"done":bool(done),"obs":obs,"A":8}); rewards.append(r); actions.append(a)
        if done: break
    controls=[]
    t=len(actions)
    while not done and t < horizon:
        sel=ag.select({"family":"renewal","t":t,"A":8,"obs":obs})
        a=sel["action"]
        obs,r,done,_=env.step(a)
        ag.update({"action":a,"reward":float(r),"done":bool(done),"obs":obs,"A":8})
        rewards.append(r); actions.append(a)
        hs=core.header.state
        controls.append({"evidence_gate":hs.evidence_gate,"local_authority":hs.local_authority,"nonlocal_authority":hs.nonlocal_authority})
        t+=1
    return {"reward_rate":mean(rewards),"actions":actions,"controls":controls}


def main():
    variants={
        "stable_clean":{"noise":0.0,"p_ren":0.02},
        "stable_noisy":{"noise":0.2,"p_ren":0.02},
        "volatile_clean":{"noise":0.0,"p_ren":0.12},
        "volatile_noisy":{"noise":0.2,"p_ren":0.12},
    }
    shapes={"canonical":None,"progress_low":0.0,"progress_high":1.0}
    out={"study":"predictive_placement_renewal_local_progress_v3","family":"renewal","axis":"local_progress_reliability","warmup_schedule":[0,1,2,3,4,5],"results":{}}
    for vname, cfg in variants.items():
        out["results"][vname]={}
        for sname, sval in shapes.items():
            trials=[run_trial(cfg["noise"], cfg["p_ren"], sval, seed=s, horizon=140) for s in range(12)]
            out["results"][vname][sname]={
                "mean_reward_rate":mean(t["reward_rate"] for t in trials),
                "seed0_actions":trials[0]["actions"],
                "mean_controls":{k:mean(c[k] for t in trials for c in t["controls"]) for k in ["evidence_gate","local_authority","nonlocal_authority"]},
            }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))
