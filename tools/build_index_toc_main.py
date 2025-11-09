#!/usr/bin/env python3
import re
import sys
import json
from pathlib import Path
from datetime import datetime
import yaml

ROOT = Path('TheoryOfChange_main')
OUT = ROOT / '00_Meta' / 'FULL_PASS_INDEX.md'

FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='replace')


def frontmatter(text: str):
    m = FM_RE.search(text)
    return m.group(1) if m else ''


def parse_yaml(s: str):
    if not s:
        return {}
    try:
        return yaml.safe_load('---\n' + s + '\n') or {}
    except Exception:
        return {}


def first_md_heading(text: str):
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return ''


def collect_entries():
    entries = []
    for p in ROOT.rglob('*.md'):
        rel = p.as_posix()
        t = read(p)
        fm = frontmatter(t)
        data = parse_yaml(fm)
        entry = {
            'path': rel,
            'folder': p.parts[1] if len(p.parts) > 1 else '',
            'subfolder': p.parts[2] if len(p.parts) > 2 else '',
            'id': data.get('id', ''),
            'type': data.get('type', data.get('status', '')),
            'title': data.get('title', '') or first_md_heading(t),
        }
        entries.append(entry)
    return sorted(entries, key=lambda e: e['path'])


def section_title_for(e):
    top = e['path'].split('/')[1] if '/' in e['path'] else e['path']
    if top == '01_Statements' and len(e['path'].split('/')) > 2:
        return f"01_Statements/{e['path'].split('/')[2]}"
    if top == '05_Speculations' and len(e['path'].split('/')) > 2:
        return f"05_Speculations/{e['path'].split('/')[2]}"
    return top


def build_report(entries):
    now = datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    lines = []
    lines.append('# FULL PASS INDEX — TheoryOfChange_main')
    lines.append('')
    lines.append(f'Generated: {now}')
    lines.append('')
    # Summary counts
    counts = {}
    for e in entries:
        key = section_title_for(e)
        counts[key] = counts.get(key, 0) + 1
    lines.append('## Summary (counts by section)')
    for k in sorted(counts):
        lines.append(f'- {k}: {counts[k]} files')
    lines.append('')

    # Detailed sections
    lines.append('## Detailed Index')
    cur = None
    for e in entries:
        sec = section_title_for(e)
        if sec != cur:
            lines.append('')
            lines.append(f'### {sec}')
            cur = sec
        path = e['path']
        id_ = e['id'] or '—'
        type_ = e['type'] or '—'
        title = e['title'] or '—'
        lines.append(f'- `{path}` — id: {id_} | title: {title} | type/status: {type_}')

    return '\n'.join(lines) + '\n'


def main():
    entries = collect_entries()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    report = build_report(entries)
    OUT.write_text(report, encoding='utf-8')
    print(f'Wrote index: {OUT} ({len(entries)} files)')


if __name__ == '__main__':
    main()

