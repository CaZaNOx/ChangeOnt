scope: kernel+STOA (renewal lane)
baseline: PhaseFSM (strong finite-state), LastFSM (reference)
seed: 7
env: {A:8, L:6, p_ren:0.02, p_noise:0.0, T_max:1000}
commands:
  - python -m experiments.runners.renewal_runner --config .\experiments\configs\toy_ren_fsm_phase.yaml --out .\outputs\renewal_fsm_phase
artifacts:
  - .\outputs\renewal_fsm_phase\metrics.jsonl
  - .\outputs\renewal_fsm_phase\budget.csv
hashes:
  - phase_jsonl_sha256: A53EB0100D465DC08FA9ABCED5C26ABDCC123AF3A97378D7500B127E72A75129
notes:
  - JSONL header includes mode: "phase"
  - Determinism verified (identical hash on rerun)
