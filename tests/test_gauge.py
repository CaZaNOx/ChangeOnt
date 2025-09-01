# FILE: tests/test_gauge.py
import numpy as np
from core.gauge import Gauge

def test_gauge_update_in_bounds():
    g = Gauge(n_classes=5)
    for _ in range(100):
        v = g.update(idx=2, PE=1.0, EU=0.0)
        assert 0.0 <= v <= 1.0
