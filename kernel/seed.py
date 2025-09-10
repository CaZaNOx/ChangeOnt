import random
try:
    import numpy as np
except Exception:
    np = None

def seed_all(seed: int):
    random.seed(seed)
    if np is not None:
        np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    except Exception:
        pass

__all__ = ["seed_all"]
