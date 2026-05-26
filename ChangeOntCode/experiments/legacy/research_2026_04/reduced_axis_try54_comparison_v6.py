from __future__ import annotations

import json
from math import sqrt
from statistics import mean
from typing import Any, Dict, List, Mapping

from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.placement.legacy.primitive_fields import derive_environment_basis_bundle
from agents.co.placement.legacy.reduced_axes import project_full_to_reduced7, project_full_to_reduced6, project_full_to_reduced5, project_full_to_reduced4
from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import EnvCfg, CodebookRenewalEnvW
from environments.maze1.env import GridMazeEnv, MazeSpec

MODES = {
    "full10": None,
    "reduced7": "investigatory_7a_v1",
    "reduced6": "investigatory_6a_v1",
    "reduced5": "investigatory_5a_v1",
    "reduced4": "investigatory_4a_v1",
}


def _l2(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    keys = sorted(set(a.keys()) | set(b.keys()))
    return sqrt(sum((float(a.get(k, 0.0)) - float(b.get(k, 0.0))) ** 2 for k in keys))


def _base_contract(family: str, actions_count: int) -> Dict[str, Any]:
    if family == 'bandit':
        return {"actions":{"count":actions_count},"observation_channels":["action_identity","reward_feedback","trace_history"],"task_anchor":{"kind":"reward_maximization","provided_externally":True},"timescale_profile":{"horizon_fixity":"fixed","drift":"unknown"},"observability_profile":{"state":"partial","outcome":"direct","constraints":"unknown"},"reversibility_profile":{"action_reversibility":"reversible","commitment_cost":"medium"}}
    if family == 'renewal':
        return {"actions":{"count":actions_count},"observation_channels":["symbol_observation","reward_feedback","trace_history"],"task_anchor":{"kind":"predictive_reward_alignment","provided_externally":True},"timescale_profile":{"horizon_fixity":"mixed","drift":"unknown"},"observability_profile":{"state":"direct","outcome":"direct","constraints":"unknown"},"reversibility_profile":{"action_reversibility":"reversible","commitment_cost":"medium"}}
    return {"actions":{"count":actions_count},"observation_channels":["visible_position","visible_goal","legality_geometry","trace_history"],"task_anchor":{"kind":"goal_reach","provided_externally":True},"timescale_profile":{"horizon_fixity":"fixed","drift":"slow"},"observability_profile":{"state":"direct","outcome":"direct","constraints":"direct"},"reversibility_profile":{"action_reversibility":"partly_reversible","commitment_cost":"medium"}}


def _core(family: str, *, reduction_mode: str | None = None, axis_override: Dict[str, float] | None = None):
    cfg={
        "name": f"reduction_cmp_v6_{family}_{reduction_mode or '10a'}",
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


def _bundle(core, packet: Dict[str, Any]) -> Dict[str, Any]:
    return derive_environment_basis_bundle(packet, core.export_runtime_contract())


def sample_states() -> List[Dict[str, Any]]:
    out=[]
    for label, probs in [("bandit_easy", [0.85,0.55,0.25,0.10]), ("bandit_hard", [0.55,0.50,0.45,0.40])]:
        for seed in range(2):
            env=BernoulliBanditEnv(probs,horizon=30); env.reset(seed=seed)
            core=_core('bandit'); ag=COAdapterBandit(core=core,n_arms=len(probs))
            for t in range(8):
                sel=ag.select({'family':'bandit','t':t,'n_arms':len(probs)})
                packet=dict(ag._last_obs or {})
                if packet:
                    bundle=_bundle(core, packet)
                    out.append({'family':'bandit','variant':label,'seed':seed,'t':t,
                                'axes10':bundle['effective_axes'],
                                'axes7':project_full_to_reduced7(bundle['effective_axes']),
                                'axes6':project_full_to_reduced6(bundle['effective_axes']),
                                'axes5':project_full_to_reduced5(bundle['effective_axes']),
                                'axes4':project_full_to_reduced4(bundle['effective_axes'])})
                a=sel.get('action',0); _,r,d,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(d)})
                if d: break
    ren_variants=[('renewal_stable_noisy',0.2,0.02),('renewal_volatile_noisy',0.2,0.12)]
    for label, noise, p_ren in ren_variants:
        for seed in range(2):
            env=CodebookRenewalEnvW(EnvCfg(A=8,L_win=6,p_ren=p_ren,p_noise=noise,T_max=30), seed=seed)
            obs,_,done,_=env.reset(); core=_core('renewal'); ag=COAdapterRenewal(core=core); t=0
            while not done and t < 8:
                sel=ag.select({'family':'renewal','t':t,'A':8,'obs':obs})
                packet=dict(ag._last_obs or {})
                if packet:
                    bundle=_bundle(core, packet)
                    out.append({'family':'renewal','variant':label,'seed':seed,'t':t,
                                'axes10':bundle['effective_axes'],
                                'axes7':project_full_to_reduced7(bundle['effective_axes']),
                                'axes6':project_full_to_reduced6(bundle['effective_axes']),
                                'axes5':project_full_to_reduced5(bundle['effective_axes']),
                                'axes4':project_full_to_reduced4(bundle['effective_axes'])})
                a=sel.get('action',0); obs,r,done,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(done),'obs':obs,'A':8}); t += 1
    maze_variants=[
        ('maze_open_visible', lambda s: MazeSpec(width=9,height=9,seed=s,partial_observability=False,dynamic_walls=False)),
        ('maze_narrow_partial_dynamic', lambda s: MazeSpec(width=9,height=9,seed=s,partial_observability=True,view_radius=0,dynamic_walls=True,wall_flip_prob=0.15,max_flips_per_step=2)),
    ]
    for label, spec_fn in maze_variants:
        for seed in range(2):
            env=GridMazeEnv(spec=spec_fn(seed)); env.reset(seed=seed); core=_core('maze'); ag=COAdapterMaze(core=core)
            for t in range(8):
                obs={"family":"maze","t":t,**env.get_observation()}; sel=ag.select(obs)
                packet=dict(ag._last_obs or {})
                if packet:
                    bundle=_bundle(core, packet)
                    out.append({'family':'maze','variant':label,'seed':seed,'t':t,
                                'axes10':bundle['effective_axes'],
                                'axes7':project_full_to_reduced7(bundle['effective_axes']),
                                'axes6':project_full_to_reduced6(bundle['effective_axes']),
                                'axes5':project_full_to_reduced5(bundle['effective_axes']),
                                'axes4':project_full_to_reduced4(bundle['effective_axes'])})
                a=sel.get('action','RIGHT')
                if a not in ('UP','DOWN','LEFT','RIGHT'): a='RIGHT'
                _,r,d,_=env.step(a); ag.update({'observation':tuple(env.pos),'reward':r,'done':d,'action':a})
                if d: break
    return out


def near_location(states: List[Dict[str, Any]]) -> Dict[str, Any]:
    pairs=[('bandit','renewal'),('bandit','maze'),('renewal','maze')]
    out={}
    for mode,key in [('full10','axes10'),('reduced7','axes7'),('reduced6','axes6'),('reduced5','axes5'),('reduced4','axes4')]:
        out[mode]={}
        for a,b in pairs:
            bestd=None; best=None
            A=[s for s in states if s['family']==a]; B=[s for s in states if s['family']==b]
            for sa in A:
                for sb in B:
                    d=_l2(sa[key], sb[key])
                    if bestd is None or d<bestd:
                        bestd=d; best=(sa,sb)
            out[mode][f'{a}_{b}']={'distance':bestd,'a_variant':best[0]['variant'],'a_t':best[0]['t'],'b_variant':best[1]['variant'],'b_t':best[1]['t']}
    return out


def bandit_compare() -> Dict[str, Any]:
    variants={"easy_gap":[0.85,0.55,0.25,0.10],"hard_gap":[0.55,0.50,0.45,0.40]}
    shapes={"canonical":None,"hidden_low":0.0,"hidden_high":1.0}
    out={}
    for mode_name, reduction_mode in MODES.items():
        out[mode_name]={}
        for vname, probs in variants.items():
            out[mode_name][vname]={}
            for sname, sval in shapes.items():
                trials=[]
                for seed in range(2):
                    env=BernoulliBanditEnv(probs,horizon=30); env.reset(seed=seed)
                    core=_core('bandit', reduction_mode=reduction_mode, axis_override=None if sval is None else {'hidden_structure_dependence':sval})
                    ag=COAdapterBandit(core=core,n_arms=len(probs))
                    regret=0.0; rewards=[]; best=max(probs)
                    warmup=[0,1,2,3,0,1]
                    for a in warmup:
                        _,r,d,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(d)}); regret += best-probs[a]; rewards.append(r)
                    for t in range(len(warmup),30):
                        sel=ag.select({'family':'bandit','t':t,'n_arms':len(probs)})
                        a=sel['action']; _,r,d,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(d)})
                        regret += best-probs[a]; rewards.append(r)
                    trials.append({'regret':regret,'reward_rate':mean(rewards)})
                out[mode_name][vname][sname]={'mean_regret':mean(t['regret'] for t in trials),'mean_reward_rate':mean(t['reward_rate'] for t in trials)}
    return out


def renewal_compare() -> Dict[str, Any]:
    variants={
        'stable_noisy': {'noise':0.2,'p_ren':0.02},
        'volatile_noisy': {'noise':0.2,'p_ren':0.12},
    }
    shapes={"canonical":None,"local_support_low":0.0,"local_support_high":1.0}
    out={}
    for mode_name, reduction_mode in MODES.items():
        out[mode_name]={}
        for vname, cfg in variants.items():
            out[mode_name][vname]={}
            for sname, sval in shapes.items():
                override=None if sval is None else {'coverage_adequacy':sval,'local_progress_reliability':sval}
                trials=[]
                for seed in range(2):
                    env=CodebookRenewalEnvW(EnvCfg(A=8,L_win=6,p_ren=cfg['p_ren'],p_noise=cfg['noise'],T_max=30), seed=seed)
                    obs,_,done,_=env.reset(); core=_core('renewal', reduction_mode=reduction_mode, axis_override=override); ag=COAdapterRenewal(core=core)
                    rewards=[]
                    warmup=[0,1,2,3,4,5]
                    for a in warmup:
                        obs,r,done,_=env.step(a); ag.update({'action':a,'reward':float(r),'done':bool(done),'obs':obs,'A':8}); rewards.append(r)
                        if done: break
                    t=len(rewards)
                    while not done and t < 30:
                        sel=ag.select({'family':'renewal','t':t,'A':8,'obs':obs}); a=sel['action']; obs,r,done,_=env.step(a)
                        ag.update({'action':a,'reward':float(r),'done':bool(done),'obs':obs,'A':8}); rewards.append(r); t += 1
                    trials.append({'mean_reward_rate':mean(rewards)})
                out[mode_name][vname][sname]={'mean_reward_rate':mean(t['mean_reward_rate'] for t in trials)}
    return out


def maze_compare() -> Dict[str, Any]:
    variants={
        'open_visible': lambda s: MazeSpec(width=9,height=9,seed=s,partial_observability=False,dynamic_walls=False),
        'narrow_partial_dynamic': lambda s: MazeSpec(width=9,height=9,seed=s,partial_observability=True,view_radius=0,dynamic_walls=True,wall_flip_prob=0.15,max_flips_per_step=2),
    }
    shapes={"canonical":None,"topology_low":0.0,"topology_high":1.0}
    out={}
    for mode_name, reduction_mode in MODES.items():
        out[mode_name]={}
        for vname, spec_fn in variants.items():
            out[mode_name][vname]={}
            for sname, sval in shapes.items():
                override=None if sval is None else {'action_topology':sval}
                trials=[]
                for seed in range(2):
                    env=GridMazeEnv(spec=spec_fn(seed)); env.reset(seed=seed); core=_core('maze', reduction_mode=reduction_mode, axis_override=override); ag=COAdapterMaze(core=core)
                    solved=False; steps=0
                    for t in range(30):
                        obs={'family':'maze','t':t,**env.get_observation()}; sel=ag.select(obs); a=sel.get('action','RIGHT')
                        if a not in ('UP','DOWN','LEFT','RIGHT'): a='RIGHT'
                        _,r,d,_=env.step(a); ag.update({'observation':tuple(env.pos),'reward':r,'done':d,'action':a}); steps += 1
                        if d:
                            solved=True
                            break
                    trials.append({'solve_rate':1.0 if solved else 0.0,'steps':steps})
                out[mode_name][vname][sname]={'solve_rate':mean(t['solve_rate'] for t in trials),'mean_steps':mean(t['steps'] for t in trials)}
    return out


def main() -> Dict[str, Any]:
    states=sample_states()
    return {
        'study':'reduced_axis_try6_comparison_v6',
        'sample_count':len(states),
        'near_location_compare': near_location(states),
        'bandit_hidden_compare': bandit_compare(),
        'renewal_local_support_compare': renewal_compare(),
        'maze_topology_compare': maze_compare(),
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
