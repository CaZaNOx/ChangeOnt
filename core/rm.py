def alpha_t(t:int, eta0:float=0.05, t0:int=500, power:float=0.6) -> float:
    return eta0 / ((t + t0)**power)