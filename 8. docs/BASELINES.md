# BASELINES — Budget-Matched Comparators

We use **budget-matched** baselines: match precision, FLOPs/step, params, context window, and count quotient bookkeeping.

- **FSMCounter**: explicit counter for k-th visit; nearly O(1) per step; cap k≤24.
- **LSTM1/2**: eval-only; hidden=64; no gradient updates; readout predicts “exit now.”
- **TransformerLite**: 2 layers × 2 heads; d_model=64; KV cache truncated to 64; eval-only linear probe.

**Why these?** They represent common “classical” approximators with bounded memory. CO’s edge is not bigger models but **history-adaptive quotienting and gauge** that execute phase flips without hidden state bits.


# Baselines

This repo ships **budget-matched, eval-only** baselines to compare against CO-core mechanisms:

- **FSMCounter** (`baselines/fsm_counter/fsm.py`): exits on a fixed period K; no learning; classical heuristic.
    
- **LSTM1/LSTM2** (`baselines/rnn/lstm.py`): minimal LSTM variants with random weights (no training), to exercise context memory without learning signals.
    
- **TransformerLite** (`baselines/transformer/transformer_lite.py`): toy attention with a fixed context cap.
    

Budget parity tuple to report for each agent:

- **precision**: float32 everywhere
    
- **memory bits**: parameters + KV/state + quotient tables (for CO agents)
    
- **FLOPs/step**: rough per-step compute
    
- **params**: count of trainable parameters (or fixed weights here)
    
- **context window**: max sequence length used
    

These baselines are **not tuned to win**; they exist to enforce fairness and provide classical reference behavior.
