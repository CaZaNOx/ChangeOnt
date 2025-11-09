#!/usr/bin/env python3
import re
from pathlib import Path

TRIAGE_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Triage')
OUT = Path('TheoryOfChange_main/00_Meta/Context/AI_Leads_Master.md')

ADD_VALUE_CUES = [
    r'threshold', r'marker', r'protocol', r'metric', r'test', r'deriv', r'topolog', r'causal',
    r'phenomenolog', r'qualia', r'bridge', r'operational', r'algorithm', r'proof', r'construction', r'example'
]

TARGET_HINTS = [
    (r'quantale|residuation|boolean|compose|join', 'quantale logic family (S-DF-quantale-logic / S-DR-quantale-*)'),
    (r'markov|closure', 'markov closure (S-DF-markov-closure-assumption / S-CR-nonclosure-under-tx)'),
    (r'pointer|localreach|reach|tx|frame', 'pointer/reach/Tx cluster'),
    (r'breath|rtv|collapse threshold|fixed point|limit cycle', 'breath/RTV cluster'),
    (r'identity|invariant|≈|similarity', 'identity/invariants/similarity'),
    (r'entropy|stabilization energy|\bse\b|gauge|alignment|Γ', 'entropy/SE/gauge'),
    (r'qualia|valence|phenomenolog', 'qualia/valence bridge'),
    (r'attention|focus', 'attention/thresholds'),
    (r'prm|metric|measure|protocol', 'PRM metrics/protocols'),
]


def parse_triage(path: Path):
    # lines look like: - Lnnn | bucket | coverage → target — snippet
    entries = []
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'^- L(\d+) \| ([^|]+) \| ([^—]+?)(?: → ([^—]+))? — (.*)$', line)
        if not m:
            continue
        ln = int(m.group(1))
        bucket = m.group(2).strip()
        coverage = m.group(3).strip()
        target = (m.group(4) or '').strip()
        snippet = m.group(5).strip()
        entries.append((ln, bucket, coverage, target, snippet))
    return entries


def is_add_value(snippet: str) -> bool:
    s = snippet.lower()
    return any(re.search(p, s) for p in ADD_VALUE_CUES)


def hint_target(snippet: str, existing_target: str) -> str:
    if existing_target:
        return existing_target
    for pat, tgt in TARGET_HINTS:
        if re.search(pat, snippet, re.IGNORECASE):
            return tgt
    return ''


def keep_entry(bucket: str, coverage: str, snippet: str) -> bool:
    cov = coverage.lower()
    if bucket in ('add_child', 'new_df_dr', 'hypothesis'):
        return True
    if bucket in ('needs_review', 'add_to_existing'):
        # keep if not obviously fully covered or adds value/context
        if cov.startswith('unknown') or cov.startswith('cover-slug-not-found'):
            return True
        if cov.startswith('likely-covered') and is_add_value(snippet):
            return True
        # if cov == covered but snippet has add-value cues, also keep
        if cov.startswith('covered') and is_add_value(snippet):
            return True
    return False


def main():
    sections = []
    for triage in sorted(TRIAGE_DIR.glob('AI_*_triage.md')):
        name = triage.stem.replace('_triage', '')
        entries = parse_triage(triage)
        keep = []
        for ln, bucket, coverage, target, snippet in entries:
            if keep_entry(bucket, coverage, snippet):
                target2 = hint_target(snippet, target)
                keep.append((ln, bucket, coverage, target2, snippet))
        if keep:
            sections.append((name, keep))

    lines = []
    lines.append('---')
    lines.append('title: AI Leads — Master Checklist (Actionable Only)')
    lines.append('status: evolving')
    lines.append('tags: [meta, leads, checklist]')
    lines.append('---')
    lines.append('# AI Leads — Master Checklist (Actionable Only)')
    lines.append('Guidance: Check items off when verified as covered or after applying changes; remove when resolved.')
    lines.append('')
    for name, keep in sections:
        lines.append(f'## {name}')
        for ln, bucket, coverage, target, snippet in keep:
            tgt = f' | target: {target}' if target else ''
            lines.append(f'- [ ] L{ln} | {bucket} | {coverage}{tgt} — {snippet}')
        lines.append('')
    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Wrote master:', OUT)


if __name__ == '__main__':
    main()

