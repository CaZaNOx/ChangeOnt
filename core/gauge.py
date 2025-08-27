from core.rm import alpha_t

class Gauge:
    def __init__(self, A:int, lam:float=1.0, beta:float=0.8, leak:float=0.001):
        self.g = [0.0]*A
        self.lam = lam
        self.beta = beta
        self.leak = leak
        self.t = 0

    def update(self, node:int, pe:float, eu:float):
        a = alpha_t(self.t)
        new = self.g[node] + a*( self.lam*pe - self.beta*eu - self.leak*self.g[node] )
        self.g[node] = min(1.0, max(0.0, new))
        self.t += 1
        return self.g[node]