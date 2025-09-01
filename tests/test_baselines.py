from **future** import annotations  
from baselines.fsm_counter.fsm import FSMCounter  
from baselines.rnn.lstm import LSTM1  
from baselines.transformer.transformer_lite import TransformerLite

def test_baselines_act_signature():  
A = 6  
obs_seq = [i % A for i in range(20)]  
fsm = FSMCounter(period=5); fsm.reset()  
for o in obs_seq:  
a = fsm.act(o)  
assert a in (0,1)  
lstm = LSTM1(A=A, hidden=8, seed=1); lstm.reset()  
for o in obs_seq:  
a = lstm.act(o)  
assert a in (0,1)  
tr = TransformerLite(A=A, d_model=16, heads=2, W=8, seed=2); tr.reset()  
for o in obs_seq:  
a = tr.act(o)  
assert a in (0,1)