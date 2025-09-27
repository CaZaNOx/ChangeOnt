# pytest -q experiments/tests/test_renewal_invariant.py
from experiments.env import CodebookRenewalEnvW, EnvCfg
from agents.stoa.agent_fsm import PhaseFSM

def test_reward_act_obs_invariant():
    env = CodebookRenewalEnvW(EnvCfg(A=8, L_win=6, p_ren=0.02, p_noise=0.0, T_max=100), seed=7)
    obs, _, _, info = env.reset()
    agent = PhaseFSM(A=8, L_win=6)
    agent.reset(obs)
    mismatches = 0
    for _ in range(100):
        a = agent.act(obs)
        obs, r, done, info = env.step(a)
        if ((r == 1.0) != (a == (info.get("obs", obs)))):
            mismatches += 1
        if done:
            break
    assert mismatches == 0
