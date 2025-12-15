# Graph Viewing Guide

The full derivation graph is in `graph.yaml` (source of truth). A Mermaid snapshot is in `graph.mmd` (332 nodes, 599 edges). To view it in VS Code:

1. Install/enable a Mermaid preview (e.g., the “Markdown Preview Mermaid Support” extension) **and** set `"markdown.preview.mermaid": true` in your user or workspace settings.
2. Open `TheoryOfChange_main/03_Derivation/graph.mmd`.
3. Run `Markdown: Open Preview to the Side` (Cmd/Ctrl+Shift+V). Large graphs can take a moment to render.

If you prefer Graphviz, use a DOT-compatible extension and convert `graph.yaml` to DOT or ask me to generate a `.dot` file. If rendering is slow, I can also generate a filtered subgraph (e.g., foundations only).
