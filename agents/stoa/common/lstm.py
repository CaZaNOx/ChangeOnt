from __future__ import annotations  
import numpy as np

class LSTM1Baseline:  
    """  
    Same as core LSTM but kept under baselines for clean budget-parity comparisons.  
    """  
    def init(self, A: int, H: int = 64, seed: int = 27182):  
        self.A = int(A); self.H = int(H)  
        self.rng = np.random.default_rng(seed)  
    def randn(shape):  
        return (self.rng.standard_normal(shape) * (1.0 / np.sqrt(shape[0]))).astype(np.float32)  
    self.Wxh = randn((A, 4_H))  
    self.Whh = randn((H, 4_H))  
    self.b = np.zeros((4*H,), dtype=np.float32)  
    self.Wo = randn((H, 1)); self.bo = np.zeros((1,), dtype=np.float32)  
    self.h = np.zeros((H,), dtype=np.float32)  
    self.c = np.zeros((H,), dtype=np.float32)


    def reset(self):
        self.h[:] = 0.0; self.c[:] = 0.0

    def act(self, obs: int, t_global=None) -> int:
        x = np.zeros((self.A,), dtype=np.float32); x[obs % self.A] = 1.0
        z = x @ self.Wxh + self.h @ self.Whh + self.b
        H = self.H
        i = 1.0/(1.0+np.exp(-z[:H]))
        f = 1.0/(1.0+np.exp(-z[H:2*H]))
        o = 1.0/(1.0+np.exp(-z[2*H:3*H]))
        g = np.tanh(z[3*H:])
        self.c = f*self.c + i*g
        self.h = o*np.tanh(self.c)
        p = 1.0/(1.0+np.exp(-(self.h @ self.Wo + self.bo)))[0]
        return 1 if p > 0.5 else 0
    

    -----


    from **future** import annotations  
import math  
import random  
from typing import Optional, List

class LSTM1:  
"""  
Minimal, eval-only LSTM with random weights (no training).  
Input: token id in [0..A-1], embedded as one-hot.  
Output: scalar sigmoid; action=1 if >0.5.  
"""  
def **init**(self, A: int, hidden: int = 64, seed: int = 31415):  
self.A = int(A)  
self.hidden = int(hidden)  
self.rng = random.Random(int(seed))  
# Weights (Python lists for portability)  
self.W = [[self._rand() for _ in range(self.A + self.hidden)] for _ in range(4 * self.hidden)]  
self.b = [self._rand() for _ in range(4 * self.hidden)]  
self.Wo = [self._rand() for _ in range(self.hidden)]  
self.bo = self._rand()  
self.h = [0.0] * self.hidden  
self.c = [0.0] * self.hidden

```
def _rand(self) -> float:
    return (self.rng.random() - 0.5) * 0.2

@staticmethod
def _sig(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

@staticmethod
def _tanh(x: float) -> float:
    e = math.exp(x)
    e2 = math.exp(-x)
    return (e - e2) / (e + e2)

def reset(self):
    self.h = [0.0] * self.hidden
    self.c = [0.0] * self.hidden

def act(self, obs: int) -> int:
    # concat x||h
    x = [0.0] * self.A
    if 0 <= obs < self.A:
        x[obs] = 1.0
    z = x + self.h
    gates: List[float] = []
    for i in range(4 * self.hidden):
        s = self.b[i]
        row = self.W[i]
        for j, v in enumerate(z):
            s += row[j] * v
        gates.append(s)
    i_gate = [self._sig(gates[i]) for i in range(0, self.hidden)]
    f_gate = [self._sig(gates[i]) for i in range(self.hidden, 2 * self.hidden)]
    o_gate = [self._sig(gates[i]) for i in range(2 * self.hidden, 3 * self.hidden)]
    g_gate = [self._tanh(gates[i]) for i in range(3 * self.hidden, 4 * self.hidden)]
    # update
    self.c = [f_gate[i] * self.c[i] + i_gate[i] * g_gate[i] for i in range(self.hidden)]
    self.h = [o_gate[i] * self._tanh(self.c[i]) for i in range(self.hidden)]
    # head
    s = self.bo
    for i in range(self.hidden):
        s += self.Wo[i] * self.h[i]
    y = self._sig(s)
    return 1 if y > 0.5 else 0
```

class LSTM2(LSTM1):  
"""  
Stack a second LSTM layer (same width) with independent random weights.  
"""  
def **init**(self, A: int, hidden: int = 64, seed: int = 27182):  
super().**init**(A=A, hidden=hidden, seed=seed)  
# second layer weights  
self.W2 = [[self._rand() for _ in range(self.hidden + self.hidden)] for _ in range(4 * self.hidden)]  
self.b2 = [self._rand() for _ in range(4 * self.hidden)]  
self.h2 = [0.0] * self.hidden  
self.c2 = [0.0] * self.hidden  
self.Wo2 = [self._rand() for _ in range(self.hidden)]  
self.bo2 = self._rand()

```
def reset(self):
    super().reset()
    self.h2 = [0.0] * self.hidden
    self.c2 = [0.0] * self.hidden

def act(self, obs: int) -> int:
    # first layer
    a1 = super().act(obs)  # advances h,c
    # second layer input = first layer h (copy)
    z = self.h + self.h2
    gates = []
    for i in range(4 * self.hidden):
        s = self.b2[i]
        row = self.W2[i]
        for j, v in enumerate(z):
            s += row[j] * v
        gates.append(s)
    def sig(x): return 1.0/(1.0+math.exp(-x))
    def tanh(x): 
        e = math.exp(x); e2 = math.exp(-x); 
        return (e - e2)/(e + e2)
    i_gate = [sig(gates[i]) for i in range(0, self.hidden)]
    f_gate = [sig(gates[i]) for i in range(self.hidden, 2 * self.hidden)]
    o_gate = [sig(gates[i]) for i in range(2 * self.hidden, 3 * self.hidden)]
    g_gate = [tanh(gates[i]) for i in range(3 * self.hidden, 4 * self.hidden)]
    self.c2 = [f_gate[i] * self.c2[i] + i_gate[i] * g_gate[i] for i in range(self.hidden)]
    self.h2 = [o_gate[i] * tanh(self.c2[i]) for i in range(self.hidden)]
    s = self.bo2
    for i in range(self.hidden):
        s += self.Wo2[i] * self.h2[i]
    y = 1.0/(1.0+math.exp(-s))
    return 1 if y > 0.5 else 0