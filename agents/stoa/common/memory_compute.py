from __future__ import annotations

def count_params(shapes) -> int:  
    """  
    shapes: iterable of tensor shapes (tuples); returns total scalar params.  
    """  
    total = 0  
    for shp in shapes:  
        n = 1  
        for d in shp: n *= int(d)  
        total += n  
        return total

def approx_flops_per_step(d_model: int, d_ff: int, ctx: int, layers: int = 2) -> int:  
    """  
    Very rough FLOPs/step for tiny transformer-like block.  
    """  
    attn = layers * (2 * d_model * d_model * ctx) # QK + PV  
    ff = layers * (d_model * d_ff + d_ff * d_model)  
    return int(attn + ff)