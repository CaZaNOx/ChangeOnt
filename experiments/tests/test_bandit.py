from __future__ import annotations  
from experiments.bandit import DriftingBandit, BanditCfg

def test_drifting_bandit_bounds():  
    cfg = BanditCfg(K=3, T=200, drift_amp=0.5, drift_period=50, base=0.4, noise=0.03, seed=7)  
    env = DriftingBandit(cfg)  
    _o, _r, done, _ = env.reset()  
    t = 0  
    rewards = []  
    while not done:  
        _o, r, done, info = env.step(action=t % cfg.K)  
        assert 0.01 <= info["p"] <= 0.99  
        assert r in (0.0, 1.0)  
        rewards.append(r)  
        t += 1  
        assert len(rewards) == cfg.T
