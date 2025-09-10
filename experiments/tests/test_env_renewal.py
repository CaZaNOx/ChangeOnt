# FILE: tests/test_env_renewal.py
from experiments.env import CodebookRenewalEnvW, EnvCfg

def test_env_basic():
    cfg = EnvCfg(A=4, L_win=4, p_ren=0.1, p_merge=0.2, p_split=0.1, p_noise=0.0, p_adv=0.0, T_max=50, k=6)
    env = CodebookRenewalEnvW(cfg, seed=123)
    obs, rew, done, info = env.reset()
    assert done is False
    for _ in range(10):
        obs, rew, done, info = env.step(0)
    assert isinstance(obs, int)




from future import annotations  
from experiments.env import CodebookRenewalEnvW, RenCfg  
from agents.stoa.common.fsm import FSMCounter

def test_renewal_env_basic():  
    cfg = RenCfg(A=6, p_ren=0.1, p_merge=0.2, p_split=0.2, p_noise=0.02, T_max=200, k=12, seed=123)  
    env = CodebookRenewalEnvW(cfg)  
    obs, r, done, _ = env.reset()  
    assert isinstance(obs, int) and 0 <= obs < cfg.A  
    assert r in (0.0, 1.0)  
    agent = FSMCounter(period=12)  
    t = 0  
    total = 0.0  
    while not done and t < cfg.T_max:  
        a = agent.act(obs)  
        obs, r, done, _ = env.step(a)  
        assert isinstance(obs, int) and 0 <= obs < cfg.A  
        assert r in (0.0, 1.0)  
        total += r  
        t += 1  
        assert done or t == cfg.T_max  
        assert 0.0 <= total <= 1.0
