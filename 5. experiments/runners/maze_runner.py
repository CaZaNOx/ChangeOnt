from **future** import annotations  
from typing import Dict, Any, List

from experiments.grid_maze import GridMaze, MazeCfg

def run_maze(cfg: Dict[str, Any],  
agent_name: str = "bfs_greedy",  
episodes: int = 1,  
writer=None) -> Dict[str, Any]:  
"""  
Deterministic maze runner.  
'bfs_greedy': simple greedy to goal (Manhattan steps).  
"""  
mcfg = MazeCfg(  
W=cfg.get("W", 7), H=cfg.get("H",7),  
start=tuple(cfg.get("start",(0,0))),  
goal=tuple(cfg.get("goal",(6,6))),  
walls=tuple(tuple(w) for w in cfg.get("walls", [(1,1),(1,2),(2,1),(3,3),(4,3),(4,4)]))  
)  
env = GridMaze(mcfg)

```
class Greedy:
    def reset(self): pass
    def act(self, obs):
        x,y = obs
        gx,gy = mcfg.goal
        if gy>y: return 0  # up
        if gx>x: return 1  # right
        if gy<y: return 2  # down
        if gx<x: return 3  # left
        return 0

agent = Greedy()
totals: List[float] = []
for ep in range(int(episodes)):
    obs, _, done, _ = env.reset()
    agent.reset()
    t = 0; G = 0.0
    while not done and t < (mcfg.W*mcfg.H):
        a = agent.act(obs)
        obs, r, done, _ = env.step(a)
        G += r
        if writer is not None:
            writer.write_step({"ep":ep,"t":t,"obs":list(obs),"a":int(a),"reward":float(r)})
        t += 1
    totals.append(G)
    if writer is not None:
        writer.write_episode({"ep":ep,"return":float(G)})
return {"episodes": len(totals), "mean_return": sum(totals)/max(1,len(totals))}