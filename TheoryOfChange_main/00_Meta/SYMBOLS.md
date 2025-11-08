# SYMBOLS — Single Source of Truth

Purpose
- Prevent symbol drift by maintaining one authoritative registry.
- Extend (not duplicate) the existing map at `TheoryOfChange/Symbol_Map.md:1`.

How to use
- Each symbol must have its own definition file in `01_Statements/SYMBOLS/` and an entry in `01_Statements/SYMBOLS/index.yaml`.
- Reference the per-symbol file from statements and concepts when using symbols.

Table (core)
| Symbol | Name/Meaning                 | Scope             | Notes |
|--------|------------------------------|-------------------|-------|
| Δ      | Difference / tension         | field-level       | see Symbol_Map.md |
| δ      | Local change                 | subject-local     |  "   |
| ε      | Sensitivity threshold        | modulation        |  "   |
| σ(ε)   | Sensitivity fluctuation      | modulation        |  "   |
| μ_mod  | Minimal modulation unit      | modulation        |  "   |
| α      | Warp parameter (HAQ)         | control           |  "   |
| ⇘(x)   | Field-level pointer to prior | trace/pointer     |  "   |
| ↶(x)   | Local pointer to prior       | trace/pointer     |  "   |
| ⇘²(x)  | Meta-pointer                 | trace/pointer     |  "   |
| ↻      | Breath loop                  | recursion         |  "   |
| ⊘      | Collapse                     | validation        |  "   |
| ⥤      | Structural entailment        | derivation        | replaces → |
| ⊗      | Composition (inf‑convolution)| logic/quantale     | see quantale logic |
| ⊕      | Join (min)                   | logic/quantale     |  |
| θ      | Threshold                    | validation        |  |
| τ      | Bend/Effort                  | metric/energy     |  |
| ∂      | Local differential           | analysis          |  |
| ≈      | Approximate similarity       | structural        |  |
| ≠, ≡   | Difference / identity        | structural        |  |

Registry template (use for new entries)
```
## <symbol>
- Name: <name>
- Scope: <domain or layer>
- Definition: <precise, non-ambiguous>
- Related: <other symbols>
- Examples:
  - In statements: <ids>
  - In math: ```math ... ```
```

Per-symbol files (authoritative definitions)
- Directory: `01_Statements/SYMBOLS/`
- Template fields: name, scope, definition, related, examples, cross-references.

Link
- Original comprehensive sheet: `TheoryOfChange/Symbol_Map.md:1`
