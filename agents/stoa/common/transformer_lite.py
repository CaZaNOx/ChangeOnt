from __future__ import annotations  
import numpy as np

class TransformerLiteBaseline:  
    def __init__(self, A: int, W_ctx: int = 64, d: int = 64, d_ff: int = 128, heads: int = 2, seed: int = 16180):  
        self.A = int(A); self.W = int(W_ctx); self.d = int(d)  
        self.d_ff = int(d_ff); self.h = int(heads)  
        self.rng = np.random.default_rng(seed)  
    def ortho(shape):  
        a = self.rng.standard_normal(shape).astype(np.float32)  
        q, _ = np.linalg.qr(a)  
        return q.astype(np.float32)  
    self.E = ortho((A, d))  
    self.Wq = ortho((d, d)); self.Wk = ortho((d, d)); self.Wv = ortho((d, d))  
    self.Wo = ortho((d, d))  
    self.W1 = ortho((d, d_ff)); self.b1 = np.zeros((d_ff,), dtype=np.float32)  
    self.W2 = ortho((d_ff, d)); self.b2 = np.zeros((d,), dtype=np.float32)  
    self.Whead = ortho((d, 1)); self.bhead = np.zeros((1,), dtype=np.float32)  
    self.buf = np.zeros((self.W, d), dtype=np.float32)  
    self.ptr = 0; self.len = 0


    def reset(self):
        self.buf[:] = 0.0; self.ptr = 0; self.len = 0

    def _attn(self, X):
        Q = X @ self.Wq; K = X @ self.Wk; V = X @ self.Wv
        S = (Q @ K.T) / np.sqrt(self.d).astype(np.float32)
        M = np.tril(np.ones_like(S), 0)
        S = S - 1e9*(1.0 - M)
        P = np.exp(S - S.max(axis=-1, keepdims=True))
        P = P / np.maximum(1e-6, P.sum(axis=-1, keepdims=True))
        H = P @ V
        return H @ self.Wo

    def _ff(self, X):
        H = np.maximum(0.0, X @ self.W1 + self.b1)
        return H @ self.W2 + self.b2

    def act(self, obs: int, t_global=None) -> int:
        e = self.E[obs % self.A]
        self.buf[self.ptr] = e
        self.ptr = (self.ptr + 1) % self.W
        self.len = min(self.W, self.len + 1)
        if self.len < self.W:
            X = self.buf[:self.len]
        else:
            X = np.vstack([self.buf[self.ptr:], self.buf[:self.ptr]])
        H1 = self._attn(X); X1 = X + H1
        F1 = self._ff(X1); X2 = X1 + F1
        H2 = self._attn(X2); X3 = X2 + H2
        F2 = self._ff(X3); X4 = X3 + F2
        h = X4[-1]
        p = 1.0/(1.0+np.exp(-(h @ self.Whead + self.bhead)))[0]
        return 1 if p > 0.5 else 0
    

    -----
    from **future** import annotations  
import random  
from typing import List

class TransformerLite:  
"""  
Toy, eval-only attention model (no training). Random weights, context cap W.  
"""  
def **init**(self, A: int, d_model: int = 64, heads: int = 2, W: int = 64, seed: int = 16180):  
self.A = int(A); self.d = int(d_model); self.h = int(heads); self.W = int(W)  
self.ctx: List[int] = []  
self.rng = random.Random(int(seed))  
# random query/key/value and readout vectors (flattened)  
self.Q = [self._rand() for _ in range(self.d)]  
self.K = [self._rand() for _ in range(self.d)]  
self.V = [self._rand() for _ in range(self.d)]  
self.R = [self._rand() for _ in range(self.d)] # readout  
# token embeddings (one-hot projected)  
self.E = [[self._rand() for _ in range(self.d)] for _ in range(self.A)]

```
def _rand(self) -> float:
    return (self.rng.random() - 0.5) * 0.2

def reset(self):
    self.ctx.clear()

def _dot(self, a: List[float], b: List[float]) -> float:
    return sum(ai * bi for ai, bi in zip(a, b))

def act(self, obs: int) -> int:
    # append obs
    self.ctx.append(int(obs))
    if len(self.ctx) > self.W:
        self.ctx = self.ctx[-self.W:]

    # build current query from current token
    e_q = self.E[self.ctx[-1]]
    q = [e_q[i] * self.Q[i] for i in range(self.d)]

    # scores over context
    scores = []
    values = []
    for tok in self.ctx:
        e = self.E[tok]
        k = [e[i] * self.K[i] for i in range(self.d)]
        v = [e[i] * self.V[i] for i in range(self.d)]
        scores.append(self._dot(q, k))
        values.append(v)
    # softmax
    m = max(scores) if scores else 0.0
    exps = [pow(2.718281828, s - m) for s in scores] if scores else [1.0]
    Z = sum(exps) or 1.0
    att = [e / Z for e in exps]
    # attended value
    y = [0.0] * self.d
    for a, v in zip(att, values):
        for i in range(self.d): y[i] += a * v[i]
    # readout
    logit = self._dot(y, self.R)
    # action
    return 1 if logit > 0.0 else 0
