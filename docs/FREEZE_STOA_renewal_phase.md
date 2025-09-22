scope: STOA freeze — RENEWAL/FSM (Phase baseline)
seed: 7
cmd: python -m experiments.runners.renewal_runner --config .\experiments\configs\_tmp_ren_fsm_phase.yaml --out .\outputs\renewal_fsm_phase
metrics_sha256: A53EB0100D465DC08FA9ABCED5C26ABDCC123AF3A97378D7500B127E72A75129
budget_file: .\outputs\renewal_fsm_phase\budget.csv
header_first_line:
  {"record_type": "header", "runner": "renewal", "seed": 7, "env": {"A": 8, "L_win": 6, "p_ren": 0.02, "p_noise": 0.0, "T_max": 1000}, "float32": true, "mode": "phase"}
