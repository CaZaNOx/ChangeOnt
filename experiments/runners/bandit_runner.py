from **future** import annotations  
import math  
from typing import Dict, Any, List

from benchmarks.nonstationary_bandit.bandit import DriftingBandit, BanditCfg

def run_bandit(cfg: Dict[str, Any],  
agent_name: str = "ucb",  
episodes: int = 1,  
seed: int = 1729,  
writer=None) -> Dict[str, Any]:  
"""  
Simple nonstationary bandit runner with two baselines:  
- 'ucb' (classical Upper Confidence Bound on rolling window)  
- 'eps' (epsilon-greedy)  
"""  
bcfg = BanditCfg(  
K=cfg.get("K", 5),  
T=cfg.get("T", 1000),  
drift_amp=cfg.get("drift_amp", 0.4),  
drift_period=cfg.get("drift_period", 200),  
base=cfg.get("base", 0.4),  
noise=cfg.get("noise", 0.05),  
seed=seed  
)  
env = DriftingBandit(bcfg)

```
class UCB:
    def __init__(self, K:int, c:float=2.0):
        self.K = K; self.c = c
        self.n = [0]*K
        self.s = [0.0]*K
        self.t = 0
    def reset(self):
        self.n = [0]*self.K; self.s=[0.0]*self.K; self.t=0
    def act(self, _obs):
        self.t += 1
        vals = []
        for a in range(self.K):
            m = (self.s[a]/self.n[a]) if self.n[a]>0 else 1.0
            bonus = self.c * math.sqrt(math.log(self.t+1.0)/(self.n[a]+1e-6))
            vals.append(m + bonus)
        return int(max(range(self.K), key=lambda a: vals[a]))
    def update(self, a:int, r:float):
        self.n[a] += 1; self.s[a] += r

class Eps:
    def __init__(self, K:int, eps:float=0.1):
        self.K=K; self.eps=eps
        self.n=[0]*K; self.s=[0.0]*K
    def reset(self):
        self.n=[0]*self.K; self.s=[0.0]*self.K
    def act(self, _obs):
        import random
        if random.random() < self.eps:
            return int(random.randrange(self.K))
        means = [(self.s[a]/self.n[a]) if self.n[a]>0 else 0.5 for a in range(self.K)]
        return int(max(range(self.K), key=lambda a: means[a]))
    def update(self, a:int, r:float):
        self.n[a]+=1; self.s[a]+=r

agent = UCB(K=bcfg.K) if agent_name.lower()=="ucb" else Eps(K=bcfg.K)
totals: List[float] = []
for ep in range(int(episodes)):
    _obs, _r, done, _ = env.reset()
    agent.reset()
    t = 0; G = 0.0
    while not done:
        a = agent.act(0)
        _obs, r, done, info = env.step(a)
        agent.update(info["a"], r)
        G += r
        if writer is not None:
            writer.write_step({"ep":ep,"t":t,"a":int(info["a"]),"p":float(info["p"]), "reward":float(r)})
        t += 1
    totals.append(G)
    if writer is not None:
        writer.write_episode({"ep":ep,"return":float(G)})
return {"episodes": len(totals), "mean_return": sum(totals)/max(1,len(totals))}