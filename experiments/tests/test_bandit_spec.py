# pytest -q experiments/tests/test_bandit_spec.py
import math
from experiments.runners.bandit_runner import UCB1Agent, EpsilonGreedyAgent

def test_ucb1_index_exact():
    ag = UCB1Agent(n_arms=2)
    # force counts/values
    ag.counts = [10, 5]
    ag.values = [0.5, 0.7]
    ag.t = 100  # index uses log(t)
    u0 = ag.values[0] + math.sqrt(2.0*math.log(ag.t) / ag.counts[0])
    u1 = ag.values[1] + math.sqrt(2.0*math.log(ag.t) / ag.counts[1])
    sel = 0 if u0 >= u1 else 1
    assert ag.select() in (0,1)  # play-each-once branch will fire until counts>0
    # After bootstrapping both arms once, selection must match the index argmax.
    ag.counts = [10, 10]
    assert ag.select() == (0 if (ag.values[0] + math.sqrt(2.0*math.log(ag.t+1)/10)) >=
                               (ag.values[1] + math.sqrt(2.0*math.log(ag.t+1)/10)) else 1)

def test_incremental_update():
    ag = EpsilonGreedyAgent(n_arms=1, epsilon=0.0, seed=0)
    # start at 0.0, after two rewards 1 then 0, value must be 0.5
    a = ag.select()
    ag.update(a, 1.0)
    a = ag.select()
    ag.update(a, 0.0)
    assert abs(ag.values[0] - 0.5) < 1e-12
