from __future__ import annotations  
from experiments.runners.renewal_runner import run_renewal  
from experiments.runners.bandit_runner import run_bandit  
from experiments.runners.maze_runner import run_maze

class _NoopWriter:  
def write_step(self, rec): pass  
def write_episode(self, rec): pass

def test_run_renewal_minimal():  
res = run_renewal({"A":6,"T_max":100,"k":12}, agent_name="fsm", episodes=2, seed=77, writer=_NoopWriter())  
assert "episodes" in res and "mean_return" in res

def test_run_bandit_minimal():  
res = run_bandit({"K":3,"T":100}, agent_name="ucb", episodes=1, seed=11, writer=_NoopWriter())  
assert "episodes" in res and "mean_return" in res

def test_run_maze_minimal():  
res = run_maze({"W":5,"H":5,"goal":[4,4]}, agent_name="bfs_greedy", episodes=1, writer=_NoopWriter())  
assert "episodes" in res and "mean_return" in res
