# SCHEMA — Statements, Concepts, DAG

Statement (one file per statement)
```
---
id: stmt.<slug>                 # stable id (machine)
type: FT|DF|DR|CR|CF|AS|CL      # category
aliases: ["FT 0.2_1"]          # legacy labels (optional)
title: <short human title>
concepts: ["[[02_Concepts/C-...]]"] # wiki links to concept pages
dependencies: ["[[01_Statements/...]]", ...] # wiki links to statements
parents: ["[[01_Statements/...]]"]            # wiki links to statements
successors: ["[[01_Statements/...]]", ...]    # wiki links to statements
symbols_used: ["[[01_Statements/SYMBOLS/Delta]]", "[[01_Statements/SYMBOLS/Entailment]]"]  # wiki links to symbol pages; each must exist in 01_Statements/SYMBOLS/index.yaml
tags: [foundations, ontological, stable, "type/FT", "symbol/Delta"] # Obsidian tags
sources:                        # provenance
  - path: <file:line>
flags: [godel_hole|contradiction|open_proof]
---
Claim (formal):
...

Philosophical Translation (of formal claim):
...  # plain-language restatement of the formal claim for non-math readers

Philosophical Justification:
...  # natural-language rationale (why it follows from X and Y)

Explanation (informal):
...

Derivation (Philosophical):
- ...  # argumentative steps in words (non-formal)

Derivation (Formal/Logical/Mathematical):
```math
...  # equations, logic steps, or reference to proof files
```
Proofs/Corollaries References:
- proof: <link or source ref>
- corollary: stmt.<id>

Pseudocode (optional):
...

Clarifications / Further Context:
- ...  # scope limits, definitions-in-use, examples

Counterfactuals (refs):
- stmt.<id>

Next Steps in Chain:
- suggest: stmt.<id>  # proposed successors to derive/formalize next
```

Concept Page
```
---
id: concept.<slug>
title: <name>
tags: [motif:..., operator:..., domain:..., layer:...]
status: stable|evolving|draft
---
Overview:
...

Canonical statements:
- stmt.<id> (FT)

Dependencies:
- From: concept.<slug>
- To: concept.<slug>

Open items:
- godel_hole: ...
```

DAG Index (graph.yaml)
```
nodes:
  - id: stmt.immediate-datum
    type: FT
edges:
  - from: stmt.immediate-datum
    to: stmt.change-cannot-begin
```
