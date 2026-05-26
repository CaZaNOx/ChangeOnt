from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List, Tuple

from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.placement.legacy.primitive_fields import derive_environment_basis_bundle
from agents.co.placement.legacy.reduced_axes import project_full_to_reduced7
from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import EnvCfg, CodebookRenewalEnvW
from environments.maze1.env import GridMazeEnv, MazeSpec


def _bin05(x: float) -> int:
    x=float(x)
    if x < 0.15: return 0
    if x < 0.35: return 1
    if x < 0.55: return 2
    if x < 0.75: return 3
    return 4


def _base_contract(family: str, actions_count: int) -> Dict[str, Any]:
    if family == 'bandit':
        return {"actions":{"count":actions_count},"observation_channels":["action_identity","reward_feedback","trace_history"],"task_anchor":{"kind":"reward_maximization","provided_externally":True},"timescale_profile":{"horizon_fixity":"fixed","drift":"unknown"},"observability_profile":{"state":"partial","outcome":"direct","constraints":"unknown"},"reversibility_profile":{"action_reversibility":"reversible","commitment_cost":"medium"}}
    if family == 'renewal':
        return {"actions":{"count":actions_count},"observation_channels":["symbol_observation","reward_feedback","trace_history"],"task_anchor":{"kind":"predictive_reward_alignment","provided_externally":True},"timescale_profile":{"horizon_fixity":"mixed","drift":"unknown"},"observability_profile":{"state":"direct","outcome":"direct","constraints":"unknown"},"reversibility_profile":{"action_reversibility":"reversible","commitment_cost":"medium"}}
    return {"actions":{"count":actions_count},"observation_channels":["visible_position","visible_goal","legality_geometry","trace_history"],"task_anchor":{"kind":"goal_reach","provided_externally":True},"timescale_profile":{"horizon_fixity":"fixed","drift":"slow"},"observability_profile":{"state":"direct","outcome":"direct","constraints":"direct"},"reversibility_profile":{"action_reversibility":"partly_reversible","commitment_cost":"medium"}}


def _core(family: str, *, reduction_mode: str | None = None, axis_override: Dict[str, float] | None = None):
    cfg={
        "name": f"reduced_axis_compare_{family}_{reduction_mode or '10a'}",
        "elements":{"candidate_surface":{"enabled":True},"commitment_surface":{"enabled":True,"collapse_enabled":False}},
        "primitives":{"signal_bus":{},"bandit_stats":{},"ngram_model":{}},
        "problem_contract": _base_contract(family, 4 if family != 'renewal' else 8),
    }
    study_overrides={}
    if reduction_mode:
        study_overrides["axis_reduction"]={"enabled":True,"authority":"investigatory_override","mode":reduction_mode}
    if axis_override:
        study_overrides["environment_basis_override"]={"enabled":True,"authority":"study_override","axes":dict(axis_override)}
    if study_overrides:
        cfg["study_overrides"]=study_overrides
    return build_co_core(cfg)


def _packet_bundle(core, packet: Dict[str, Any]) -> Dict[str, Any]:
    return derive_environment_basis_bundle(packet, core.export_runtime_contract())


def sample_bandit_packets() -> List[Dict[str, Any]]:
    out=[]
    probs_variants=[("bandit_easy", [0.85,0.55,0.25,0.10]), ("bandit_hard", [0.55,0.50,0.45,0.40])]
    for label, probs in probs_variants:
        for seed in range(2):
            env=BernoulliBanditEnv(probs,horizon=28); env.reset(seed=seed)
            core=_core('bandit') ; ag=COAdapterBandit(core=core,n_arms=len(probs))
            for t in range(8):
                sel=ag.select({"family":"bandit","t":t,"n_arms":len(probs)})
                packet=dict(ag._last_obs or {})
                if packet:
                    bundle=_packet_bundle(core, packet)
                    out.append({"family":"bandit","variant":label,"seed":seed,"t":t,"packet":packet,"bundle":bundle})
                a=sel.get('action',0)
                _,r,d,_=env.step(a)
                ag.update({"action":a,"reward":float(r),"done":bool(d)})
                if d: break
    return out


def sample_renewal_packets() -> List[Dict[str, Any]]:
    out=[]
    variants=[("renewal_stable_noisy",0.05,0.02), ("renewal_volatile_noisy",0.20,0.12)]
    for label, noise, p_ren in variants:
        for seed in range(2):
            env=CodebookRenewalEnvW(EnvCfg(A=4,L_win=6,p_ren=p_ren,p_noise=noise,T_max=30), seed=seed)
            obs,_,done,_=env.reset()
            core=_core('renewal'); ag=COAdapterRenewal(core=core)
            t=0
            while not done and t < 10:
                sel=ag.select({"family":"renewal","t":t,"A":4,"obs":obs})
                packet=dict(ag._last_obs or {})
                if packet:
                    bundle=_packet_bundle(core, packet)
                    out.append({"family":"renewal","variant":label,"seed":seed,"t":t,"packet":packet,"bundle":bundle})
                a=sel.get('action',0)
                obs,r,done,_=env.step(a)
                ag.update({"action":a,"reward":float(r),"done":bool(done),"obs":obs,"A":4})
                t += 1
    return out


def sample_maze_packets() -> List[Dict[str, Any]]:
    out=[]
    variants=[("maze_visible_static", lambda s: MazeSpec(width=7,height=7,seed=s,partial_observability=False,dynamic_walls=False)),
              ("maze_partial_dyn", lambda s: MazeSpec(width=7,height=7,seed=s,partial_observability=True,view_radius=1,dynamic_walls=True,wall_flip_prob=0.08,max_flips_per_step=1))]
    for label, spec_fn in variants:
        for seed in range(2):
            env=GridMazeEnv(spec=spec_fn(seed)); env.reset(seed=seed)
            core=_core('maze'); ag=COAdapterMaze(core=core)
            for t in range(8):
                obs={"family":"maze","t":t,**env.get_observation()}
                sel=ag.select(obs)
                packet=dict(ag._last_obs or {})
                if packet:
                    bundle=_packet_bundle(core, packet)
                    out.append({"family":"maze","variant":label,"seed":seed,"t":t,"packet":packet,"bundle":bundle})
                a=sel.get('action','RIGHT')
                if a not in ('UP','DOWN','LEFT','RIGHT'):
                    a='RIGHT'
                _,r,d,_=env.step(a)
                ag.update({"observation":tuple(env.pos),"reward":r,"done":d,"action":a})
                if d: break
    return out


def occupancy_audit() -> Dict[str, Any]:
    states=sample_bandit_packets()+sample_renewal_packets()+sample_maze_packets()
    full_cells=[]; red_cells=[]
    for s in states:
        axes=s['bundle']['effective_axes']
        reduced=project_full_to_reduced7(axes)
        full_cells.append((s['family'], tuple(_bin05(axes[k]) for k in sorted(axes.keys()))))
        red_cells.append((s['family'], tuple(_bin05(reduced[k]) for k in sorted(reduced.keys()))))
    def cross_family_collisions(cells):
        by={} 
        for fam,cell in cells:
            by.setdefault(cell,set()).add(fam)
        return sum(1 for fams in by.values() if len(fams) >= 2)
    return {
        'sample_count': len(states),
        'unique_full10_cells': len(set(cell for _,cell in full_cells)),
        'unique_reduced7_cells': len(set(cell for _,cell in red_cells)),
        'cross_family_collision_cells_full10': cross_family_collisions(full_cells),
        'cross_family_collision_cells_reduced7': cross_family_collisions(red_cells),
    }


def bandit_hidden_compare() -> Dict[str, Any]:
    variants={"easy_gap":[0.85,0.55,0.25,0.10],"hard_gap":[0.55,0.50,0.45,0.40]}
    modes={"full10":None,"reduced7":"investigatory_7a_v1"}
    shapes={"canonical":None,"hidden_low":0.0,"hidden_high":1.0}
    out={}
    for mode_name, reduction_mode in modes.items():
        out[mode_name]={}
        for vname, probs in variants.items():
            out[mode_name][vname]={}
            for sname, sval in shapes.items():
                trials=[]
                for seed in range(2):
                    env=BernoulliBanditEnv(probs,horizon=36); env.reset(seed=seed)
                    core=_core('bandit', reduction_mode=reduction_mode, axis_override=None if sval is None else {'hidden_structure_dependence':sval})
                    ag=COAdapterBandit(core=core,n_arms=len(probs))
                    regret=0.0; rewards=[]; best=max(probs)
                    for a in [0,1,2,3]:
                        _,r,d,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(d)}); regret += best-probs[a]; rewards.append(r)
                    for t in range(4,36):
                        sel=ag.select({'family':'bandit','t':t,'n_arms':len(probs)})
                        a=sel['action']; _,r,d,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(d)})
                        regret += best-probs[a]; rewards.append(r)
                    trials.append({'regret':regret,'reward_rate':mean(rewards)})
                out[mode_name][vname][sname]={'mean_regret':mean(t['regret'] for t in trials),'mean_reward_rate':mean(t['reward_rate'] for t in trials)}
    return out


def renewal_local_support_compare() -> Dict[str, Any]:
    variants={
        'stable_noisy': {'noise':0.2,'p_ren':0.02},
        'volatile_noisy': {'noise':0.2,'p_ren':0.12},
    }
    modes={"full10":None,"reduced7":"investigatory_7a_v1"}
    shapes={"canonical":None,"local_support_low":0.0,"local_support_high":1.0}
    out={}
    for mode_name, reduction_mode in modes.items():
        out[mode_name]={}
        for vname, cfg in variants.items():
            out[mode_name][vname]={}
            for sname, sval in shapes.items():
                override=None
                if sval is not None:
                    override={'coverage_adequacy':sval,'local_progress_reliability':sval}
                trials=[]
                for seed in range(2):
                    env=CodebookRenewalEnvW(EnvCfg(A=8,L_win=6,p_ren=cfg['p_ren'],p_noise=cfg['noise'],T_max=60), seed=seed)
                    obs,_,done,_=env.reset()
                    core=_core('renewal', reduction_mode=reduction_mode, axis_override=override)
                    ag=COAdapterRenewal(core=core)
                    rewards=[]
                    warm=[0,1,2,3,4,5]
                    for a in warm:
                        obs,r,done,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(done),'obs':obs,'A':8}); rewards.append(r)
                        if done: break
                    t=len(rewards)
                    while not done and t < 60:
                        sel=ag.select({'family':'renewal','t':t,'A':8,'obs':obs})
                        a=sel['action']; obs,r,done,_=env.step(a)
                        ag.update({'action':a,'reward':float(r),'done':bool(done),'obs':obs,'A':8}); rewards.append(r); t += 1
                    trials.append({'reward_rate':mean(rewards)})
                out[mode_name][vname][sname]={'mean_reward_rate':mean(t['reward_rate'] for t in trials)}
    return out


def main() -> Dict[str, Any]:
    return {
        'study':'reduced_axis_comparison_v1',
        'reduction_mode':'investigatory_7a_v1',
        'occupancy_audit': occupancy_audit(),
        'bandit_hidden_structure_compare': bandit_hidden_compare(),
        'renewal_local_support_compare': renewal_local_support_compare(),
    }


if __name__ == '__main__':
    import json
    print(json.dumps(main(), indent=2))
