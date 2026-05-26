#!/usr/bin/env python3
import re
import sys
from pathlib import Path
import yaml

ROOT = Path('TheoryOfChange_main')
REPO_ROOT = ROOT.parent
STATEMENTS_DIR = ROOT / '01_Statements'
CONCEPTS_DIR = ROOT / '02_Concepts'
SYMBOLS_DIR = STATEMENTS_DIR / 'SYMBOLS'
GRAPH_FILE = ROOT / '03_Derivation/graph.yaml'

FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)
WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

def frontmatter(text: str):
    m = FM_RE.search(text)
    return m.group(1) if m else ''

def load_yaml_like(fm: str):
    try:
        return yaml.safe_load('---\n'+fm+'\n') or {}
    except Exception:
        return {}

def validate_links(arr, path):
    issues = []
    if arr is None:
        return issues
    if not isinstance(arr, list):
        issues.append(f"not-a-list at {path}")
        return issues
    for v in arr:
        if not isinstance(v, str) or not v.startswith('[['):
            issues.append(f"non-wikilink entry '{v}' at {path}")
            continue
        target = v.strip('[]')
        # allow links without .md. Resolve first inside TheoryOfChange_main,
        # then from the repository root so statement frontmatter can point to
        # ChangeOntCode docs without producing false missing-link failures.
        candidates = [
            ROOT / (target + '.md'),
            ROOT / target,
            REPO_ROOT / (target + '.md'),
            REPO_ROOT / target,
        ]
        if not any(c.exists() for c in candidates):
            issues.append(f"missing target for link {v} at {path}")
    return issues

def collect_statement_ids():
    ids = {}
    for p in STATEMENTS_DIR.rglob('*.md'):
        if p.parts[-2] == 'SYMBOLS':
            continue
        t = p.read_text(encoding='utf-8', errors='replace')
        fm = frontmatter(t)
        data = load_yaml_like(fm)
        sid = data.get('id')
        if sid:
            ids[sid] = p
    return ids

def main():
    issues = []

    # 1) Validate statements frontmatter
    for p in STATEMENTS_DIR.rglob('*.md'):
        if p.parts[-2] == 'SYMBOLS':
            continue
        if p.name == 'README.md':
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        fm = frontmatter(text)
        if not fm:
            issues.append(f"No frontmatter: {p}")
            continue
        data = load_yaml_like(fm)
        # required fields
        for key in ['id','type','title','concepts','tags']:
            if key not in data:
                issues.append(f"Missing '{key}' in {p}")
        # concepts must be non-empty
        if isinstance(data.get('concepts'), list) and len(data['concepts']) == 0:
            issues.append(f"Empty 'concepts' in {p}")
        # link arrays
        for key in ['concepts','parents','dependencies','successors']:
            issues += validate_links(data.get(key), f"{p}:{key}")
        # symbols_used
        syms = data.get('symbols_used', [])
        issues += validate_links(syms, f"{p}:symbols_used")

    # 2) Validate symbol files have sections
    for sp in SYMBOLS_DIR.glob('*.md'):
        if sp.name == 'README.md':
            continue
        txt = sp.read_text(encoding='utf-8', errors='replace')
        ok = all(h in txt for h in ['# ', 'Definition (formal):'])
        if not ok:
            issues.append(f"Symbol page missing sections: {sp}")

    # 3) Derivation graph ids exist, and every graph edge endpoint is declared.
    # This prevents stale Mermaid snapshots or orphaned edge endpoints from
    # keeping deleted/renamed statements alive as if they were canonical.
    stmt_ids = collect_statement_ids()
    if GRAPH_FILE.exists():
        graph = yaml.safe_load(GRAPH_FILE.read_text(encoding='utf-8'))
        node_ids = {n['id'] for n in graph.get('nodes', []) if 'id' in n}
        edge_ids = set()
        for edge in graph.get('edges', []) or []:
            src = edge.get('from')
            dst = edge.get('to')
            if src:
                edge_ids.add(src)
            if dst:
                edge_ids.add(dst)
        for nid in sorted(node_ids):
            if nid not in stmt_ids:
                issues.append(f"Graph node id not found in statements: {nid}")
        for eid in sorted(edge_ids):
            if eid not in node_ids:
                issues.append(f"Graph edge endpoint not declared as node: {eid}")
            if eid not in stmt_ids:
                issues.append(f"Graph edge endpoint not found in statements: {eid}")
    else:
        issues.append(f"Missing graph file: {GRAPH_FILE}")

    # 3b) Mermaid graph snapshots must not keep deleted/renamed IDs alive.
    for graph_mmd in [ROOT / '03_Derivation/graph.mmd', ROOT / '03_Derivation/graph_first_layer.mmd']:
        if not graph_mmd.exists():
            issues.append(f"Missing graph snapshot: {graph_mmd}")
            continue
        refs = set(re.findall(r'\bstmt\.[A-Za-z0-9_.-]+', graph_mmd.read_text(encoding='utf-8', errors='replace')))
        for ref in sorted(refs):
            if ref not in stmt_ids:
                issues.append(f"Mermaid graph references missing statement id {ref}: {graph_mmd}")

    # 4) No old symbol links remain
    for p in ROOT.rglob('*.md'):
        if '[[symbols/' in p.read_text(encoding='utf-8', errors='replace'):
            issues.append(f"Found old symbol link in {p}")

    if issues:
        print('Validation issues:')
        for i in issues:
            print('-', i)
        sys.exit(1)
    else:
        print('All checks passed for TheoryOfChange_main.')

if __name__ == '__main__':
    main()
