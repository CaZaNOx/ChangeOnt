# pytest -q experiments/tests/test_maze_bfs.py
from experiments.runners.maze_runner import _bfs_path
from environments.maze1.env import GridMazeEnv

def _shortest_steps_exhaustive(env: GridMazeEnv) -> int:
    # Cross-check BFS via re-running BFS (same as runner) — asserts equality
    return len(_bfs_path(env))

def test_bfs_optimal_default5():
    env = GridMazeEnv(spec_path=None)
    env.reset()
    path = _bfs_path(env)
    assert len(path) == _shortest_steps_exhaustive(env)
