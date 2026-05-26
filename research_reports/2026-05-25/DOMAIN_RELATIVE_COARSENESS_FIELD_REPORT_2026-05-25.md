# Domain-Relative Coarseness Field Report — 2026-05-25

## Summary

Implemented the bounded CO-faithful coarseness refinement discussed after relation-field/function-like collapse:

- `coarseness_radius` remains the global fallback.
- `coarseness_by_domain` records active public relation/burden-domain coarseness.
- Rows expose `dynamic_shape_domain_coarseness` and the associated public domain.

This is not a new policy or solver. It is telemetry and next-cycle gauge/control support.

## Theory / docs

Added:

- `TheoryOfChange_main/01_Statements/02_Outer_Formation/022C_S-DR-domain-relative-coarseness-field.md`
- `ChangeOntCode/docs/kernel_spec/107_DOMAIN_RELATIVE_COARSENESS_FIELD.md`
- `research_reports/2026-05-25/DOMAIN_RELATIVE_COARSENESS_FIELD_UPDATE_2026-05-25.md`

Updated:

- `TheoryOfChange_main/02_Concepts/C-dynamic-shape-coarseness-field.md`
- kernel docs index / reading guide
- README / NEXT_AI_START_HERE / open ledgers

## Runtime changes

Changed:

- `ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py`
- `ChangeOntCode/agents/co/runtime/surfaces/candidate_surface.py`

New test/probe:

- `ChangeOntCode/agents/co/tests/domain_relative_coarseness_field_invariants.py`
- `ChangeOntCode/experiments/studies/domain_relative_coarseness_field_probe_v1.py`
- output: `ChangeOntCode/outputs/domain_relative_coarseness_field_probe_v1.json`

## Guardrails

The implementation uses only public relation/burden domains already emitted by RelationSurface / relation-field telemetry. It does not use:

- family names;
- native action names;
- hidden state;
- reward hindsight;
- DP/baseline values;
- post-hoc performance.

## Probe result

The probe confirms that two active domains can carry different coarseness values:

- ambiguous/high-hiddenness domain retained finer coarseness;
- concentrated/degradation-relief domain became relatively coarser.

This demonstrates anisotropic coarseness without introducing arbitrary dimensions.

## Checks run

Passed:

- `python tools/validate_toc_main.py`
- `python -m compileall -q ChangeOntCode/agents ChangeOntCode/experiments tools`
- `python -m agents.co.tests.domain_relative_coarseness_field_invariants`
- `python -m agents.co.tests.dynamic_shape_field_invariants`
- `python -m agents.co.tests.relation_field_function_like_collapse_invariants`
- `python -m agents.co.tests.relation_surface_public_effect_invariants`
- `python -m agents.co.tests.no_classical_fallback_fail_closed_invariants`
- `python -m agents.co.tests.code_vs_docs_pipeline_compliance_invariants`
- `python -m experiments.studies.domain_relative_coarseness_field_probe_v1`

## Honest status

This is a conceptually justified refinement and a bounded implementation. It does not claim empirical improvement. Next step remains testing/auditing the current kernel with this telemetry available.
