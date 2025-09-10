from __future__ import annotations  
import numpy as np

class TransformerLite:  
    """  
    Tiny 2-layer token-mixer with fixed weights (eval-only).  
    Context window 64; 2 heads; d_model=64; d_ff=128. Linear probe on last token.  
    """  
    def init(self, A: int, W_ctx: int = 64, d: int = 64, d_ff: int = 128, heads: int = 2, seed: int = 16180):  
        self.A = int(A); self.W = int(W_ctx); self.d = int(d)  
        self.d_ff = int(d_ff); self.h = int(heads)  
        self.rng = np.random.default_rng(seed)  
    def ortho(shape):  
        a = self.rng.standard_normal(shape).astype(np.float32)  
        # Gram-Schmidt-ish  
        q, _ = np.linalg.qr(a)  
        return q.astype(np.float32)  
        # token embed  
        self.E = ortho((A, d))  
        # attn params (shared for simplicity)  
        self.Wq = ortho((d, d)); self.Wk = ortho((d, d)); self.Wv = ortho((d, d))  
        self.Wo = ortho((d, d))  
        # FF  
        self.W1 = ortho((d, d_ff)); self.b1 = np.zeros((d_ff,), dtype=np.float32)  
        self.W2 = ortho((d_ff, d)); self.b2 = np.zeros((d,), dtype=np.float32)  
        # head  
        self.Whead = ortho((d, 1)); self.bhead = np.zeros((1,), dtype=np.float32)  
        # cache  
        self.buf = np.zeros((self.W, d), dtype=np.float32)  
        self.ptr = 0  
        self.len = 0


    def reset(self):
        self.buf[:] = 0.0; self.ptr = 0; self.len = 0

    def _attn(self, X):
        Q = X @ self.Wq; K = X @ self.Wk; V = X @ self.Wv
        S = (Q @ K.T) / np.sqrt(self.d).astype(np.float32)
        # causal mask
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
        # build sequence in time order
        if self.len < self.W:
            X = self.buf[:self.len]
        else:
            X = np.vstack([self.buf[self.ptr:], self.buf[:self.ptr]])
        # layer 1
        H1 = self._attn(X)
        X1 = X + H1
        F1 = self._ff(X1)
        X2 = X1 + F1
        # layer 2
        H2 = self._attn(X2)
        X3 = X2 + H2
        F2 = self._ff(X3)
        X4 = X3 + F2
        # probe last token
        h = X4[-1]
        p = 1.0/(1.0+np.exp(-(h @ self.Whead + self.bhead)))[0]
        return 1 if p > 0.5 else 0