from **future** import annotations  
from experiments.grid_maze import GridMaze, MazeCfg

def test_grid_maze_goal_reachable():  
cfg = MazeCfg()  
env = GridMaze(cfg)  
obs, r, done, _ = env.reset()  
assert not done  
t = 0  
# naive greedy to goal  
while not done and t < cfg.W * cfg.H:  
x,y = obs  
gx,gy = cfg.goal  
if gy>y: a=0  
elif gx>x: a=1  
elif gy<y: a=2  
elif gx<x: a=3  
else: a=0  
obs, r, done, _ = env.step(a)  
t += 1  
assert done  
assert r == 1.0