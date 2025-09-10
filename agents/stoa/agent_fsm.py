from future import annotations

class FSMCounter:  
    """  
    Minimal baseline: counts local steps and attempts exit every k steps.  
    This is deliberately simple (no training).  
    """  
    def init(self, k_cap: int = 24):  
        self.k_cap = int(k_cap)  
        self.t = 0

    
    def reset(self) -> None:
        self.t = 0

    def act(self, obs, t_global=None) -> int:
        self.t += 1
        return 1 if (self.t % max(1, self.k_cap // 2)) == 0 else 0
    