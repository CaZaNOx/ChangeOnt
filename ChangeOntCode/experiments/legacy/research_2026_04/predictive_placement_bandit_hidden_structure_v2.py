from statistics import mean
from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit
from environments.bandit.bandit import BernoulliBanditEnv


def _core(hidden_override=None):
    cfg={
        "name":"predictive_bandit_hidden_v2",
        "elements":{"candidate_surface":{"enabled":True},"commitment_surface":{"enabled":True,"collapse_enabled":False}},
        "primitives":{"signal_bus":{},"bandit_stats":{}},
        "problem_contract":{"actions":{"count":4},"observation_channels":["action_identity","reward_feedback","trace_history"],"task_anchor":{"kind":"reward_maximization","provided_externally":True},"timescale_profile":{"horizon_fixity":"fixed","drift":"unknown"},"observability_profile":{"state":"partial","outcome":"direct","constraints":"unknown"},"reversibility_profile":{"action_reversibility":"reversible","commitment_cost":"medium"}},
    }
    if hidden_override is not None:
        cfg["study_overrides"]={"environment_basis_override":{"enabled":True,"authority":"study_override","axes":{"hidden_structure_dependence":hidden_override}}}
    return build_co_core(cfg)


def run_trial(probs, shape, seed, horizon=60):
    env=BernoulliBanditEnv(probs,horizon=horizon); env.reset(seed=seed)
    core=_core(shape); ag=COAdapterBandit(core=core,n_arms=len(probs))
    regret=0.0; rewards=[]; actions=[]; best=max(probs)
    warmup=[0,1,2,3][:len(probs)]
    for a in warmup:
        _,r,d,_=env.step(a); ag.update({"action":a,"reward":float(r),"done":bool(d)}) ; regret += best-probs[a]; rewards.append(r); actions.append(a)
    controls=[]
    for t in range(len(warmup), horizon):
        sel=ag.select({"family":"bandit","t":t,"n_arms":len(probs)})
        a=sel["action"]; _,r,d,_=env.step(a); ag.update({"action":a,"reward":float(r),"done":bool(d)})
        regret += best-probs[a]; rewards.append(r); actions.append(a)
        hs=core.header.state
        controls.append({"rival_breadth":hs.rival_breadth,"nonlocal_authority":hs.nonlocal_authority,"local_authority":hs.local_authority})
    return {"regret":regret,"reward_rate":mean(rewards),"actions":actions,"controls":controls}


def main():
    variants={"easy_gap":[0.85,0.55,0.25,0.1],"hard_gap":[0.55,0.50,0.45,0.40]}
    shapes={"canonical":None,"hidden_low":0.0,"hidden_high":1.0}
    out={"study":"predictive_placement_bandit_hidden_structure_v2","family":"bandit","axis":"hidden_structure_dependence","warmup_schedule":[0,1,2,3],"results":{}}
    for vname, probs in variants.items():
        out["results"][vname]={}
        for sname, sval in shapes.items():
            trials=[run_trial(probs, sval, seed=s, horizon=60) for s in range(10)]
            out["results"][vname][sname]={
                "mean_regret":mean(t["regret"] for t in trials),
                "mean_reward_rate":mean(t["reward_rate"] for t in trials),
                "seed0_actions":trials[0]["actions"],
                "mean_controls":{k:mean(c[k] for t in trials for c in t["controls"]) for k in ["rival_breadth","nonlocal_authority","local_authority"]},
            }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))
