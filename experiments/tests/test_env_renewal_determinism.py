from experiments.env import CodebookRenewalEnvW, EnvCfg

def test_env_deterministic_seed():
    cfg = EnvCfg(A=4, L_win=3, p_ren=0.0, p_noise=0.0, T_max=20)
    e1 = CodebookRenewalEnvW(cfg, seed=123)
    e2 = CodebookRenewalEnvW(cfg, seed=123)
    o1,_,_,_ = e1.reset()
    o2,_,_,_ = e2.reset()
    assert o1 == o2
    seq1, seq2 = [], []
    for _ in range(20):
        a1 = o1; a2 = o2
        o1, r1, d1, _ = e1.step(a1)
        o2, r2, d2, _ = e2.step(a2)
        seq1.append((o1,r1,d1))
        seq2.append((o2,r2,d2))
    assert seq1 == seq2
