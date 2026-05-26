from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from agents.co.adapters.renewal_adapter import COAdapterRenewal
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    build_validated_co_core,
    load_co_manifest_params,
)
from experiments.studies._descriptor_plane_v4 import (
    POSTURES,
    posture_scores,
    predicted_order,
    problem_contract_for_family,
    renewal_descriptor,
    target_scope_for_family,
)

OUT = Path('outputs/renewal_tested_continuity_composition_audit_v1.json')
STUDY = 'renewal_tested_continuity_composition_audit_v1'
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
RENEWAL_HORIZON = 220
SEED = 1
RENEWAL_TASKS = [
    {'name': 'renewal_stable', 'family': 'renewal', 'A': 8, 'L_win': 6, 'p_ren': 0.01, 'p_noise': 0.00},
    {'name': 'renewal_mixed', 'family': 'renewal', 'A': 8, 'L_win': 6, 'p_ren': 0.05, 'p_noise': 0.04},
    {'name': 'renewal_volatile', 'family': 'renewal', 'A': 8, 'L_win': 6, 'p_ren': 0.15, 'p_noise': 0.10},
]
FIELDS = [
    'goal_relation', 'tested_hint', 'continuity_support', 'context_relation', 'reward_relation',
    'sequence_relation', 'action_support_hint', 'context_support_hint', 'row_support_hint',
    'ngram_support_hint', 'context_entropy_hint', 'row_entropy_hint'
]


def _co_params(spec: Dict[str, Any]) -> Dict[str, Any]:
    scope = target_scope_for_family('renewal')
    descriptor = renewal_descriptor(p_ren=spec['p_ren'], p_noise=spec['p_noise'], horizon=RENEWAL_HORIZON, action_count=spec['A'])
    pred_scores = posture_scores(descriptor, target_scope=scope)
    pred = predicted_order(descriptor, target_scope=scope)
    best_posture = pred[0]
    params = dict(CANONICAL_PARAMS)
    params['descriptor_hypothesis'] = {'target_scope': scope, 'axes': dict(descriptor), 'status': 'investigatory', 'source': STUDY}
    params['kernel_posture'] = {'name': best_posture, 'axes': dict(POSTURES[best_posture]), 'status': 'investigatory'}
    params['prediction_protocol'] = {'base_problem': {'name': spec['name']}, 'predicted_ordering_before': list(pred), 'predicted_scores': dict(pred_scores), 'status': 'investigatory'}
    params['problem_contract'] = problem_contract_for_family('renewal', spec)
    return params


def _candidate_by_id(candidates: List[Dict[str, Any]], cid: int) -> Dict[str, Any] | None:
    for c in candidates:
        if int(c.get('candidate_id', -1)) == int(cid):
            return c
    return None


def _mean_fields(cands: List[Dict[str, Any]]) -> Dict[str, float]:
    if not cands:
        return {}
    return {f: float(mean(float(c.get(f, 0.0) or 0.0) for c in cands)) for f in FIELDS}


def _run(spec: Dict[str, Any]) -> Dict[str, Any]:
    A = int(spec['A']); L = int(spec['L_win'])
    env = CodebookRenewalEnvW(EnvCfg(A=A, L_win=L, p_ren=float(spec['p_ren']), p_noise=float(spec['p_noise']), T_max=RENEWAL_HORIZON), seed=SEED)
    obs, _, done, _ = env.reset()
    core = build_validated_co_core(_co_params(spec), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
    agent = COAdapterRenewal(core=core)
    rewards = []
    chosen = []
    top_goal = []
    top_tested = []
    top_cont = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        payload = {'family': 'renewal', 'obs': int(obs), 't': t, 'A': A, 'L_win': L}
        packet = agent._packet(payload, t)
        candidates = [c for c in list(packet.get('candidates') or []) if isinstance(c, dict) and bool(c.get('legal', True))]
        if candidates:
            top_goal.append(max(candidates, key=lambda c: float(c.get('goal_relation', 0.0) or 0.0)))
            top_tested.append(max(candidates, key=lambda c: float(c.get('tested_hint', 0.0) or 0.0)))
            top_cont.append(max(candidates, key=lambda c: float(c.get('continuity_support', 0.0) or 0.0)))
        sel = agent.select(payload)
        act = int(sel.get('action', 0))
        cand = _candidate_by_id(candidates, act)
        if cand is not None:
            chosen.append(cand)
        obs, r, done, _ = env.step(act)
        agent.update({'observation': int(obs), 'reward': float(r), 'done': bool(done), 'action': act})
        rewards.append(float(r))
        t += 1
    return {
        'mean_reward': sum(rewards) / float(len(rewards) or 1),
        'chosen_mean': _mean_fields(chosen),
        'top_goal_mean': _mean_fields(top_goal),
        'top_tested_mean': _mean_fields(top_tested),
        'top_continuity_mean': _mean_fields(top_cont),
        'steps': len(rewards),
    }


def main() -> None:
    out = {'study': STUDY, 'status': 'executed', 'seed': SEED, 'by_task': {}}
    for spec in RENEWAL_TASKS:
        out['by_task'][spec['name']] = _run(spec)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
