from future import annotations  
from dataclasses import dataclass

@dataclass  
class BudgetCounter:  
    float_bytes: int = 4 # float32  
    params: int = 0  
    state: int = 0  
    flops_per_step: int = 0


    def add_params(self, n: int) -> None:
        self.params += int(n)

    def add_state(self, n: int) -> None:
        self.state += int(n)

    def add_flops(self, n: int) -> None:
        self.flops_per_step += int(n)

    @property
    def memory_bits(self) -> int:
        return 8 * self.float_bytes * (self.params + self.state)
    

    ---
    from **future** import annotations  
from typing import Dict

def param_bits(n_params: int, dtype_bits: int = 32) -> int:  
return int(max(0, n_params) * max(1, dtype_bits))

def dense_param_count(n_in: int, n_out: int, bias: bool = True) -> int:  
return n_in * n_out + (n_out if bias else 0)

def rnn_param_count(n_in: int, n_hidden: int, n_out: int) -> Dict[str, int]:  
"""  
Naive Elman-style RNN param count (input->h + h->h + bias; h->out + bias)  
"""  
ih = dense_param_count(n_in, n_hidden)  
hh = dense_param_count(n_hidden, n_hidden)  
ho = dense_param_count(n_hidden, n_out)  
return {"ih": ih, "hh": hh, "ho": ho, "total": ih + hh + ho}

def lstm_param_count(n_in: int, n_hidden: int, layers: int = 1) -> int:  
"""  
LSTM layer params per layer: 4 gates * (n_in+n_hidden)_n_hidden + 4_n_hidden (bias)  
Stacks sum linearly, with n_in for first layer; then n_in = n_hidden for next.  
"""  
total = 0  
d = n_in  
for _ in range(layers):  
total += 4 * (d + n_hidden) * n_hidden + 4 * n_hidden  
d = n_hidden  
return total
