#!/usr/bin/env python3
from pathlib import Path
import re
import yaml

ROOT = Path('TheoryOfChange_main')
GRAPH_FILE = ROOT / '03_Derivation/graph.yaml'
STATEMENTS_DIR = ROOT / '01_Statements'
OUT = ROOT / '00_Meta' / 'GRAPH_SWEEP_REPORT.md'

FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='replace')


def frontmatter(text: str):
    m = FM_RE.search(text)
    return m.group(1) if m else ''


def load_yaml_like(s: str):
    try:
        return yaml.safe_load('---\n' + s + '\n') or {}
    except Exception:
        return {}


def collect_stmt_meta_by_id():
    by_id = {}
    for p in STATEMENTS_DIR.rglob('*.md'):
        if p.name == 'README.md' or p.parts[-2] == 'SYMBOLS':
            continue
        fm = frontmatter(read(p))
        y = load_yaml_like(fm)
        sid = y.get('id')
        if sid:
            by_id[sid] = {'type': y.get('type'), 'title': y.get('title')}
    return by_id


def main():
    graph = yaml.safe_load(read(GRAPH_FILE))
    nodes = graph.get('nodes', []) or []
    edges = graph.get('edges', []) or []
    node_ids = {n.get('id') for n in nodes if isinstance(n, dict) and n.get('id')}

    endpoints = set()
    embedded_nodes = {}
    for e in edges:
        if not isinstance(e, dict):
            continue
        if 'from' in e or 'to' in e:
            if e.get('from'):
                endpoints.add(e['from'])
            if e.get('to'):
                endpoints.add(e['to'])
        elif 'id' in e:
            # node-like dict sitting inside edges
            embedded_nodes[e['id']] = {'type': e.get('type'), 'title': e.get('title')}

    missing = sorted([i for i in endpoints if i and i not in node_ids])

    stmt_meta = collect_stmt_meta_by_id()

    lines = []
    lines.append('# GRAPH SWEEP REPORT')
    lines.append('')
    lines.append(f'- Node count (nodes list): {len(node_ids)}')
    lines.append(f'- Unique endpoints referenced in edges: {len(endpoints)}')
    lines.append(f'- Missing node ids (referenced in edges but not in nodes): {len(missing)}')
    lines.append('')
    if missing:
        lines.append('## Missing ids and suggested node entries')
        for mid in missing:
            meta = stmt_meta.get(mid) or embedded_nodes.get(mid) or {}
            mtype = meta.get('type', 'DF')
            mtitle = meta.get('title', mid)
            lines.append(f'- {mid} | type: {mtype} | title: {mtitle}')
        lines.append('')
        lines.append('```yaml')
        lines.append('nodes_append:')
        for mid in missing:
            meta = stmt_meta.get(mid) or embedded_nodes.get(mid) or {}
            mtype = meta.get('type', 'DF')
            mtitle = meta.get('title', mid)
            lines.append(f'  - id: {mid}')
            lines.append(f'    type: {mtype}')
            lines.append(f'    title: {mtitle}')
        lines.append('```')
    else:
        lines.append('## No missing node ids detected.')

    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Wrote: {OUT}')


if __name__ == '__main__':
    main()

