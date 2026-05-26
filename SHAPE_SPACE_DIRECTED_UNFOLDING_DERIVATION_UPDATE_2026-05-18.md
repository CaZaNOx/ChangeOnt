# Shape / CO-space / directed unfolding derivation update — 2026-05-18

## Purpose

This update closes a theory-ordering gap identified during conceptual review: `shape`, `space`, `directedness`, `tension`, `coarseness`, and `dynamic shape update` were already implied by the first outer route, but not yet explicitly derived in one canonical bridge.

## Added canonical statement

- `TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md`

The file derives:
- shape-as-such;
- local shape-state;
- CO-space;
- directed unfolding / proto-sequencing;
- tension;
- burden as retained continuation-relevant tension;
- coarseness field;
- point-as-ball;
- dynamic shape update.

## Added concept page

- `TheoryOfChange_main/02_Concepts/C-dynamic-shape-coarseness-field.md`

## Updated references

- `TheoryOfChange_main/01_Statements/02_Outer_Formation/README.md`
- `TheoryOfChange_main/02_Concepts/C-outer-formation-route.md`
- `TheoryOfChange_main/03_Derivation/Derivation.md`
- `TheoryOfChange_main/03_Derivation/graph.yaml`
- `TheoryOfChange_main/03_Derivation/graph.mmd`
- `TheoryOfChange_main/03_Derivation/graph_first_layer.mmd`
- `TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md`
- `CANONICAL_STRUCTURE_MAP.md`
- `OPEN_POINTS_AND_FUTURE_WORK.md`

## Important boundary

The new derivation began as a theory target. As of 2026-05-21 the repo includes a first-pass persistent DynamicShapeField implementation, but not a final mathematical coarseness topology or empirical proof.

Current code implements:
- static public six-question shape prior;
- current branch/relation/burden surfaces;
- local shape-gauged resolver timing in CommitmentSurface;
- first-pass persistent DynamicShapeField with coarseness_radius, projection_horizon, relation_density, burden_persistence, hiddenness_pressure, admissibility_pressure, and gauge_confidence.

It does not yet implement a final topology, fully grounded coefficients, family-wide dynamic-shape ablation evidence, or robot/simulation validation.

## Checks run

```text
python tools/validate_toc_main.py
python -m compileall -q tools ChangeOntCode/tools ChangeOntCode/agents ChangeOntCode/experiments
cd ChangeOntCode && PYTHONPATH=. python -m pytest -q \
  agents/co/tests/canonical_structure_docs_invariants.py \
  agents/co/tests/code_vs_docs_pipeline_compliance_invariants.py
```

Results:
- TheoryOfChange_main validator: PASS
- compileall: PASS
- selected docs/code compliance invariants: 4 passed

## Remaining open work

- harden the first-pass DynamicShapeField implementation and formula grounding;
- run family-wide static-vs-dynamic ablations;
- verify no-oracle/no-reward-hindsight behavior under real traces;
- connect dynamic shape to multi-step branch identity and later robot/simulation problems;
- keep the current implementation structurally provisional until deeper evidence exists.
