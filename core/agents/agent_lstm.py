from future import annotations  
import numpy as np

class LSTM1:  
    """  
    1-layer LSTM with fixed random weights (eval-only).  
    Input: one-hot over A; Hidden size H=64.  
    Output: sigmoid probability of exit.  
    """  
    def init(self, A: int, H: int = 64, seed: int = 31415):  
        self.A = int(A); self.H = int(H)  
        self.rng = np.random.default_rng(seed)  
    # Xavier-ish init  
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