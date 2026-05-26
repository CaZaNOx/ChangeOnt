from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    assert_valid_co_rollout,
    build_validated_co_core,
    load_co_manifest_params,
)
from experiments.studies._descriptor_plane_v4 import (
    POSTURES,
    bandit_descriptor,
    renewal_descriptor,
    posture_scores,
    predicted_order,
    problem_contract_for_family,
    target_scope_for_family,
)

OUT = Path('outputs/problem_plane_stress_v2.json')
STUDY = 'problem_plane_stress_v2'
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
SEEDS = [1, 2]
BANDIT_HORIZON = 220
RENEWAL_HORIZON = 240
BANDIT_TASKS = [
    {"name": "bandit_gap_002", "family": "bandit", "probs": [0.49, 0.50, 0.51]},
    {"name": "bandit_gap_004", "family": "bandit", "probs": [0.48, 0.50, 0.52]},
    {"name": "bandit_gap_008", "family": "bandit", "probs": [0.46, 0.50, 0.54]},
    {"name": "bandit_gap_015", "family": "bandit", "probs": [0.425, 0.50, 0.575]},
    {"name": "bandit_gap_030", "family": "bandit", "probs": [0.35, 0.50, 0.65]},
    {"name": "bandit_easy_offset", "family": "bandit", "probs": [0.10, 0.20, 0.80]},
]
RENEWAL_TASKS = [
    {"name": "renewal_stable", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.01, "p_noise": 0.00},
    {"name": "renewal_lowmixed_a", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.02, "p_noise": 0.01},
    {"name": "renewal_lowmixed_b", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.03, "p_noise": 0.02},
    {"name": "renewal_mixed", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.05, "p_noise": 0.04},
    {"name": "renewal_highmixed", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.08, "p_noise": 0.06},
    {"name": "renewal_volatile", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.15, "p_noise": 0.10},
]


def _params(spec: Dict[str, Any], posture_name: str, descriptor: Dict[str, float], pred_scores: Dict[str, float], pred: List[str]) -> Dict[str, Any]:
    family = str(spec['family'])
    p = deepcopy(CANONICAL_PARAMS)
    p['descriptor_hypothesis'] = {
        'target_scope': target_scope_for_family(family),
        'axes': dict(descriptor),
        'status': 'investigatory',
        'source': STUDY,
    }
    p['kernel_posture'] = {
        'name': posture_name,
        'axes': dict(POSTURES[posture_name]),
        'status': 'investigatory',
    }
    p['prediction_protocol'] = {
        'base_problem': {'name': spec['name']},
        'predicted_ordering_before': list(pred),
        'predicted_scores': dict(pred_scores),
        'status': 'investigatory',
    }
    p['problem_contract'] = problem_contract_for_family(family, spec)
    return p


def _run_bandit(spec: Dict[str, Any], posture: str, descriptor: Dict[str, float], pred_scores: Dict[str, float], pred: List[str], seed: int) -> float:
    core = build_validated_co_core(
        _params(spec, posture, descriptor, pred_scores, pred),
        study_name=STUDY,
        manifest_path=DEFAULT_CANONICAL_MANIFEST,
        agent_name=DEFAULT_CANONICAL_AGENT_NAME,
    )
    env = BernoulliBanditEnv(spec['probs'], horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = COAdapterBandit(core=core, n_arms=env.n_arms)
    best = max(spec['probs'])
    regret = 0.0
    votes: List[int] = []
    policies: List[str] = []
    for t in range(BANDIT_HORIZON):
        sel = agent.select({'family': 'bandit', 't': t, 'n_arms': env.n_arms})
        a = int(sel.get('action', 0))
        votes.append(int(sel.get('signal_bus_votes', 0)))
        policies.append(str(sel.get('co_policy', 'bandit:safe_default')))
        _, r, done, _ = env.step(a)
        agent.update({'action': a, 'reward': float(r), 'done': bool(done)})
        regret += max(0.0, best - spec['probs'][a])
        if done:
            break
    assert_valid_co_rollout(study_name=STUDY, signal_bus_votes=votes, co_policies=policies)
    return regret


def _run_renewal(spec: Dict[str, Any], posture: str, descriptor: Dict[str, float], pred_scores: Dict[str, float], pred: List[str], seed: int) -> float:
    core = build_validated_co_core(
        _params(spec, posture, descriptor, pred_scores, pred),
        study_name=STUDY,
        manifest_path=DEFAULT_CANONICAL_MANIFEST,
        agent_name=DEFAULT_CANONICAL_AGENT_NAME,
    )
    env = CodebookRenewalEnvW(
        EnvCfg(
            A=int(spec['A']),
            L_win=int(spec['L_win']),
            p_ren=float(spec['p_ren']),
            p_noise=float(spec['p_noise']),
            T_max=RENEWAL_HORIZON,
        ),
        seed=seed,
    )
    obs, _, done, _ = env.reset()
    agent = COAdapterRenewal(core=core)
    rewards: List[float] = []
    votes: List[int] = []
    policies: List[str] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        sel = agent.select({'family': 'renewal', 'obs': int(obs), 't': t, 'A': int(spec['A']), 'L_win': int(spec['L_win'])})
        a = int(sel.get('action', 0))
        votes.append(int(sel.get('signal_bus_votes', 0)))
        policies.append(str(sel.get('co_policy', 'renewal:safe_default')))
        obs, r, done, _ = env.step(a)
        agent.update({'observation': int(obs), 'reward': float(r), 'done': bool(done), 'action': a})
        rewards.append(float(r))
        t += 1
    if policies and all(p == 'renewal:safe_default' for p in policies) and all(v == 0 for v in votes):
        raise RuntimeError('invalid renewal rollout')
    return sum(rewards) / float(len(rewards) or 1)


def _eval(spec: Dict[str, Any]) -> Dict[str, Any]:
    family = str(spec['family'])
    descriptor = (
        bandit_descriptor(spec['probs'], horizon=BANDIT_HORIZON)
        if family == 'bandit'
        else renewal_descriptor(
            p_ren=spec['p_ren'],
            p_noise=spec['p_noise'],
            horizon=RENEWAL_HORIZON,
            action_count=spec['A'],
        )
    )
    scope = target_scope_for_family(family)
    pred_scores = posture_scores(descriptor, target_scope=scope)
    pred = predicted_order(descriptor, target_scope=scope)
    rec: Dict[str, Any] = {}
    for posture in POSTURES:
        vals = [
            _run_bandit(spec, posture, descriptor, pred_scores, pred, s) if family == 'bandit'
            else _run_renewal(spec, posture, descriptor, pred_scores, pred, s)
            for s in SEEDS
        ]
        rec[posture] = {'mean_score': mean(vals), 'seed_scores': vals}
    if family == 'bandit':
        observed = [k for k, _ in sorted(((k, v['mean_score']) for k, v in rec.items()), key=lambda kv: (kv[1], kv[0]))]
    else:
        observed = [k for k, _ in sorted(((k, v['mean_score']) for k, v in rec.items()), key=lambda kv: (-kv[1], kv[0]))]
    return {
        'descriptor': descriptor,
        'predicted_order': pred,
        'observed_order': observed,
        'exact_match': pred == observed,
        'postures': rec,
    }


def main() -> None:
    out: Dict[str, Any] = {
        'study': STUDY,
        'status': 'executed',
        'seeds': SEEDS,
        'bandit_horizon': BANDIT_HORIZON,
        'renewal_horizon': RENEWAL_HORIZON,
        'bandit': {},
        'renewal': {},
    }
    for spec in BANDIT_TASKS:
        out['bandit'][spec['name']] = _eval(spec)
    for spec in RENEWAL_TASKS:
        out['renewal'][spec['name']] = _eval(spec)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
