# ChangeOnt — CO-core (Change Ontology) Project

This repo houses:
- **CO math/logic** (change-first operators, spread numbers, quotienting)
- **CO-core mechanisms** (a–i: HAQ/gauge, variable spawning, density headers, etc.)
- **Parity experiments** with budget-matched classical baselines
- **No fake runs**: any plotted results will be produced by code checked in here.

## Quick start
```bash
# Create env
mamba env create -f environment.yml   # or: conda env create -f environment.yml
mamba activate changeont              # or: conda activate changeont

# Run tests
pytest -q

# Run the parity fixture (skeleton; prints wiring-only until we fill implementations)
python experiments/run_parity.py --help