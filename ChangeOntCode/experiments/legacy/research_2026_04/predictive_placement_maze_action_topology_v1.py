from statistics import mean
from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.maze_adapter import COAdapterMaze
from environments.maze1.env import GridMazeEnv, MazeSpec


def _core(topology_override=None):
    cfg={
        "name":"predictive_maze_topology_v1",
        "elements":{"candidate_surface":{"enabled":True},"commitment_surface":{"enabled":True,"collapse_enabled":False}},
        "primitives":{"signal_bus":{}},
        "problem_contract":{"actions":{"count":4},"observation_channels":["visible_position","visible_goal","legality_geometry","trace_history"],"task_anchor":{"kind":"goal_reach","provided_externally":True},"timescale_profile":{"horizon_fixity":"fixed","drift":"slow"},"observability_profile":{"state":"direct","outcome":"direct","constraints":"direct"},"reversibility_profile":{"action_reversibility":"partly_reversible","commitment_cost":"medium"}},
    }
    if topology_override is not None:
        cfg["study_overrides"]={"environment_basis_override":{"enabled":True,"authority":"study_override","axes":{"action_topology":topology_override}}}
    return build_co_core(cfg)


def run_trial(spec, shape, seed, step_limit=140):
    env=GridMazeEnv(spec=spec)
    env.reset(seed=seed)
    core=_core(shape); ag=COAdapterMaze(core=core)
    steps=0; solved=False; actions=[]; controls=[]
    while steps < step_limit and env.pos != env.goal:
        obs={"family":"maze","t":steps,**env.get_observation()}
        sel=ag.select(obs)
        a=sel.get("action") if isinstance(sel,dict) else sel
        if a not in ("UP","DOWN","LEFT","RIGHT"):
            a="RIGHT"
        _,reward,done,_=env.step(a)
        ag.update({"observation":tuple(env.pos),"reward":reward,"done":done,"action":a})
        actions.append(a)
        hs=core.header.state
        controls.append({"rival_breadth":hs.rival_breadth,"path_sensitivity":hs.path_sensitivity,"local_authority":hs.local_authority})
        steps+=1
        if done:
            solved=True
            break
    return {"solved":solved,"steps":steps,"actions":actions,"controls":controls}


def main():
    variants={
        "visible_static": lambda seed: MazeSpec(width=7,height=7,seed=seed,partial_observability=False,dynamic_walls=False),
        "partial_dynamic": lambda seed: MazeSpec(width=7,height=7,seed=seed,partial_observability=True,view_radius=1,dynamic_walls=True,wall_flip_prob=0.08,max_flips_per_step=1),
    }
    shapes={"canonical":None,"topology_low":0.0,"topology_high":1.0}
    out={"study":"predictive_placement_maze_action_topology_v1","family":"maze","axis":"action_topology","results":{}}
    for vname, spec_fn in variants.items():
        out["results"][vname]={}
        for sname, sval in shapes.items():
            trials=[run_trial(spec_fn(seed), sval, seed=seed, step_limit=140) for seed in range(10)]
            solved=[t for t in trials if t["solved"]]
            out["results"][vname][sname]={
                "solve_rate": mean(1.0 if t["solved"] else 0.0 for t in trials),
                "mean_steps_solved": mean(t["steps"] for t in solved) if solved else None,
                "seed0_actions": trials[0]["actions"],
                "mean_controls": {k:mean(c[k] for t in trials for c in t["controls"]) for k in ["rival_breadth","path_sensitivity","local_authority"]},
            }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))
