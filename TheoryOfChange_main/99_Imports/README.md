# 99_Imports — Provenance Index

Purpose
- Map original sources (FND files, AI chats, CoreOntology) to canonical statements.
- Maintain traceability without duplicating content.

Example format (sources.yaml)
```
sources:
  - src: TheoryOfChange/02_Foundations/FND_0_Phil-ImmediateDatum.md:1
    claims:
      - id: stmt.immediate-datum
      - id: stmt.change-cannot-begin
  - src: TheoryOfChange/01_CoreOntology/COT_1_Immediate_Observation_of_Change.md:1
    claims:
      - id: stmt.immediate-datum
```

Notes
- This folder is for provenance mapping only; it does not affect backlinks automation.
- Add links from statements to provenance entries in `sources:` frontmatter as needed.
