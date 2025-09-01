# FILE: tests/test_metrics.py
from evaluation.metrics.theil_sen import theil_sen_slope
from evaluation.metrics.volatility import jaccard_volatility
from evaluation.metrics.lln_stability import lln_stable
from evaluation.metrics.au_regret import au_regret_window

def test_theil_sen_basic():
    xs = list(range(10))
    ys = [2*x for x in xs]
    s = theil_sen_slope(xs, ys)
    assert 1.5 < s < 2.5

def test_volatility_edges():
    seq = [0,1,2,3]*200
    v = jaccard_volatility(seq, W=50)
    assert 0.0 <= v <= 1.0

def test_lln_stability_small():
    # Not enough samples
    seq = [0,1,2,3]*50
    ok, _ = lln_stable(seq, W=200)
    assert ok is False

def test_au_regret_window():
    a = [0,1,0,1]*50
    b = [0,0,0,0]*50
    m = au_regret_window(a, b, win=20)
    assert m >= 0.0
