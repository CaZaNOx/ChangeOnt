#!/usr/bin/env python3
import re
from pathlib import Path

TRIAGE_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Triage')
OUT_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Triage_Summary')

ADD_VALUE_CUES = [
    r'threshold', r'marker', r'protocol', r'metric', r'test', r'derive', r'topolog', r'causal',
    r'phenomenolog', r'qualia', r'bridge', r'operational', r'algorithm', r'proof', r'construction', r'example'
]


def parse_triage(path: Path):
    entries = []
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'^- L(\d+) \| ([^|]+) \| ([^—]+?) — (.*)$', line)
        if not m:
            continue
        ln = int(m.group(1))
        bucket = m.group(2).strip()
        coverage = m.group(3).strip()
        snippet = m.group(4).strip()
        entries.append((ln, bucket, coverage, snippet))
    return entries


def is_add_value(snippet: str) -> bool:
    s = snippet.lower()
    return any(re.search(p, s) for p in ADD_VALUE_CUES)


def select_covered_no_action(entries):
    covered = []
    for ln, bucket, coverage, snippet in entries:
        cov = coverage.lower()
        if cov.startswith('covered') or cov.startswith('likely-covered'):
            if bucket in ('needs_review', 'add_to_existing') and not is_add_value(snippet):
                covered.append((ln, bucket, coverage, snippet))
    return covered


def write_summary(name: str, items):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outp = OUT_DIR / f'{name}_covered_no_action.md'
    lines = []
    lines.append('---')
    lines.append(f'title: {name} — Covered (No Action Needed)')
    lines.append('status: evolving')
    lines.append('tags: [meta, triage, covered]')
    lines.append('---')
    lines.append(f'# {name} — Covered (No Action Needed)')
    lines.append('Criteria: coverage=covered/likely-covered, bucket∈{needs_review, add_to_existing}, no added-value cues.')
    lines.append('')
    if not items:
        lines.append('- (none)')
    else:
        for ln, bucket, coverage, snippet in items:
            lines.append(f'- L{ln} | {bucket} | {coverage} — {snippet}')
    outp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return outp


def main():
    # Focus first on AI_2 as requested progress
    name = 'AI_2_Avenai_RecursiveChat'
    triage = TRIAGE_DIR / f'{name}_triage.md'
    if not triage.exists():
        print('Triage file not found:', triage)
        return
    entries = parse_triage(triage)
    items = select_covered_no_action(entries)
    outp = write_summary(name, items)
    print('Wrote:', outp)


if __name__ == '__main__':
    main()

