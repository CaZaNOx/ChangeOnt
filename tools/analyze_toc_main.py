#!/usr/bin/env python3
import re
from pathlib import Path
import yaml
from collections import defaultdict

ROOT = Path('TheoryOfChange_main')
STATEMENTS_DIR = ROOT / '01_Statements'
CONCEPTS_DIR = ROOT / '02_Concepts'
GRAPH_FILE = ROOT / '03_Derivation/graph.yaml'
OUT = ROOT / '00_Meta' / 'QUALITY_REPORT.md'

FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='replace')


def frontmatter(text: str):
    m = FM_RE.search(text)
    return m.group(1) if m else ''


def load_yaml_like(fm: str):
    try:
        return yaml.safe_load('---\n' + fm + '\n') or {}
    except Exception:
        return {}


def collect_statements():
    stmts = {}
    for p in STATEMENTS_DIR.rglob('*.md'):
        if p.parts[-2] == 'SYMBOLS' or p.name == 'README.md':
            continue
        t = read(p)
        fm = frontmatter(t)
        data = load_yaml_like(fm)
        sid = data.get('id', '')
        stmts[p] = data | {'__id': sid}
    return stmts


def collect_concepts():
    concepts = {}
    for p in CONCEPTS_DIR.glob('*.md'):
        t = read(p)
        fm = frontmatter(t)
        data = load_yaml_like(fm)
        cid = data.get('id', '')
        concepts[p] = data | {'__id': cid}
    return concepts


def load_graph():
    if not GRAPH_FILE.exists():
        return set(), []
    g = yaml.safe_load(read(GRAPH_FILE)) or {}
    nodes = {n['id'] for n in g.get('nodes', []) if isinstance(n, dict) and 'id' in n}
    edges = [(e.get('from'), e.get('to')) for e in g.get('edges', []) if isinstance(e, dict)]
    return nodes, edges


def analyze():
    stmts = collect_statements()
    concepts = collect_concepts()
    node_ids, edges = load_graph()

    # Build statement id -> path, and concept id -> path
    stmt_id_to_path = {v['__id']: p for p, v in stmts.items() if v.get('__id')}
    concept_id_to_path = {v['__id']: p for p, v in concepts.items() if v.get('__id')}

    # Optional metadata gaps
    missing_sources = []
    empty_symbols_used = []
    for p, v in stmts.items():
        if not v.get('sources'):
            missing_sources.append(p)
        if v.get('symbols_used') in (None, []) and v.get('type') not in ('CL', 'AS', 'CF'):
            # symbols often less relevant for clarifications/assumptions/counterfactuals
            empty_symbols_used.append(p)

    # Graph coverage
    in_graph = []
    not_in_graph = []
    for p, v in stmts.items():
        sid = v.get('__id')
        (in_graph if sid in node_ids else not_in_graph).append((sid, p))

    # Edge degrees
    indeg = defaultdict(int)
    outdeg = defaultdict(int)
    for u, v in edges:
        if u:
            outdeg[u] += 1
        if v:
            indeg[v] += 1
    zero_in = sorted([n for n in node_ids if indeg[n] == 0])
    zero_out = sorted([n for n in node_ids if outdeg[n] == 0])

    # Concept coverage via statements' concepts frontmatter
    concept_to_statements = defaultdict(list)
    for p, v in stmts.items():
        for link in v.get('concepts', []) or []:
            # Expect '[[02_Concepts/<file>]]'
            target = link.strip('[]')
            # Normalize to concept id by reading that file's id if present
            target_path = ROOT / (target + ('' if target.endswith('.md') else '.md'))
            if target_path.exists():
                # load concept file and get id
                fm = frontmatter(read(target_path))
                cdata = load_yaml_like(fm)
                cid = cdata.get('id', target)
                sid = v.get('__id') or p.name
                concept_to_statements[cid].append(sid)
            else:
                concept_to_statements[target].append(v.get('__id') or p.name)

    concepts_with_zero_refs = []
    for p, v in concepts.items():
        cid = v.get('id', p.stem)
        if len(concept_to_statements.get(cid, [])) == 0:
            concepts_with_zero_refs.append((cid, p))

    # Statements with unknown concept IDs (path exists but concept missing id)
    statements_with_unidentified_concepts = []
    for p, v in stmts.items():
        for link in v.get('concepts', []) or []:
            target = link.strip('[]')
            target_path = ROOT / (target + ('' if target.endswith('.md') else '.md'))
            if target_path.exists():
                fm = frontmatter(read(target_path))
                cdata = load_yaml_like(fm)
                if not cdata.get('id'):
                    statements_with_unidentified_concepts.append((p, target_path))

    # Build report
    lines = []
    lines.append('# QUALITY REPORT — TheoryOfChange_main')
    lines.append('')
    lines.append('## Summary')
    lines.append(f'- Statements total: {len(stmts)}')
    lines.append(f'- Concepts total: {len(concepts)}')
    lines.append(f'- Graph nodes: {len(node_ids)}, edges: {len(edges)}')
    lines.append(f'- Statements missing sources: {len(missing_sources)}')
    lines.append(f'- Statements with empty symbols_used (non-CL/AS/CF): {len(empty_symbols_used)}')
    lines.append(f'- Statements not in graph: {len(not_in_graph)}')
    lines.append(f'- Graph nodes with zero in-degree: {len(zero_in)}')
    lines.append(f'- Graph nodes with zero out-degree: {len(zero_out)}')
    lines.append(f'- Concepts with zero referencing statements: {len(concepts_with_zero_refs)}')
    lines.append('')

    def list_paths(title, items, fmt=lambda x: str(x)):
        lines.append(f'## {title}')
        if not items:
            lines.append('- None')
        else:
            for it in items:
                lines.append(f'- {fmt(it)}')
        lines.append('')

    list_paths('Statements missing sources', missing_sources, lambda p: p.as_posix())
    list_paths('Statements with empty symbols_used (non-CL/AS/CF)', empty_symbols_used, lambda p: p.as_posix())
    list_paths('Statements not present in derivation graph', sorted(not_in_graph), lambda t: f"{t[0]} — {t[1].as_posix()}")
    list_paths('Graph nodes with zero in-degree', zero_in, lambda s: s)
    list_paths('Graph nodes with zero out-degree', zero_out, lambda s: s)
    list_paths('Concepts with zero statements referencing them', sorted(concepts_with_zero_refs), lambda t: f"{t[0]} — {t[1].as_posix()}")
    list_paths('Statements that link to concept pages missing an id', sorted(set(statements_with_unidentified_concepts)), lambda t: f"stmt: {t[0].as_posix()} | concept: {t[1].as_posix()}")

    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Wrote report: {OUT}')


if __name__ == '__main__':
    analyze()

