#!/usr/bin/env python3
import re
from pathlib import Path

DEEPREAD_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Deepread')
STATEMENTS_DIR = Path('TheoryOfChange_main/01_Statements')
CONCEPTS_DIR = Path('TheoryOfChange_main/02_Concepts')
OUT_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Triage')

# Hints to propose likely targets when no explicit cover slug was detected
TARGET_HINTS = [
    (r'quantale|residuation|boolean|compose|join', 'S-DF-quantale-logic / S-DR-quantale-*'),
    (r'markov|closure', 'S-DF-markov-closure-assumption / S-CR-nonclosure-under-tx'),
    (r'pointer|localreach|reach|tx|frame', 'pointer/reach/Tx cluster (S-DF-pointer-structural, S-DF-reach-relation, S-DF-localreach-topology, S-DF-tx-operator)'),
    (r'breath|rtv|collapse threshold|fixed point|limit cycle', 'breath/RTV cluster (S-DF-rtv-operator, S-DR-breath-stabilization, S-DR-rtv-collapse-threshold, S-DF-breath-field-global-integrator)'),
    (r'identity|invariant|≈|similarity', 'identity cluster (S-DF-identity-through-change, S-DF-identity-invariants, S-DF-similarity-operator)'),
    (r'entropy|stabilization energy|\bSE\b|gauge|alignment|Γ', 'entropy / SE / gauge (S-DF-entropy-co, S-DF-stabilization-energy, S-DF-gauge-alignment-field)'),
    (r'qualia|valence|phenomenolog', 'qualia/valence (S-CR-qualia-gauge-curvature, S-CL-emotion-recursive-valuation)'),
    (r'attention|focus', 'attention (S-DF-attention-focus / S-CL-attention-recursive-filter)'),
    (r'prm|metric|measure|protocol', 'PRM metrics / protocols (S-DF-prm-*, S-DF-change-benchmark-protocol, S-DF-extended-audit-indicators)'),
]


def load_slug_index():
    idx = {}
    for p in STATEMENTS_DIR.rglob('S-*.md'):
        idx[p.stem] = p
    for p in CONCEPTS_DIR.glob('*.md'):
        idx[p.stem] = p
    return idx


def parse_entries(path: Path):
    entries = []
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'^- L(\d+): \[(.*?)\] (.*?)?(?:\| covers: ([^\]]+))? — (.*)$', line)
        if not m:
            continue
        ln = int(m.group(1))
        bucket = m.group(2)
        # exclude explicit ignores
        if bucket.strip().lower() == 'ignore':
            continue
        cover = (m.group(4) or '').strip()
        snippet = m.group(5).strip()
        entries.append((ln, bucket, cover, snippet))
    return entries


def find_target_hint(snippet: str):
    for pat, tgt in TARGET_HINTS:
        if re.search(pat, snippet, re.IGNORECASE):
            return tgt
    return ''


def triage_entries(entries, slug_index):
    triaged = []
    for ln, bucket, cover, snippet in entries:
        coverage = 'unknown'
        target = ''
        if cover:
            # map cover like 'S-DF-identity-through-change' to file
            p = slug_index.get(cover)
            if p:
                coverage = f'covered ({cover})'
                target = f'CL add-to-existing or CR add-child for {cover}'
            else:
                coverage = 'cover-slug-not-found'
        if coverage == 'unknown':
            hint = find_target_hint(snippet)
            if hint:
                coverage = 'likely-covered'
                target = hint
        triaged.append((ln, bucket, coverage, target, cover, snippet))
    return triaged


def write_triage(chat_name: str, deepread_path: Path, triaged):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outp = OUT_DIR / f'{chat_name}_triage.md'
    lines = []
    lines.append('---')
    lines.append(f'title: {chat_name} — Full Triage (all non-ignored leads)')
    lines.append('status: evolving')
    lines.append('tags: [meta, triage, promotion]')
    lines.append('---')
    lines.append(f'# {chat_name} — Full Triage (all non-ignored leads)')
    lines.append(f'Source: [[{deepread_path.as_posix()}]]')
    lines.append('Columns: line | bucket | coverage | suggested target | snippet')
    lines.append('')
    for ln, bucket, coverage, target, cover, snippet in triaged:
        tgt = f' → {target}' if target else ''
        lines.append(f'- L{ln} | {bucket} | {coverage}{tgt} — {snippet}')
    outp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return outp


def main():
    slug_index = load_slug_index()
    outputs = []
    for p in sorted(DEEPREAD_DIR.glob('AI_*_deepread.md')):
        chat_name = p.stem.replace('_deepread','')
        entries = parse_entries(p)
        triaged = triage_entries(entries, slug_index)
        outp = write_triage(chat_name, p, triaged)
        outputs.append(outp)
    print('Triage files written:')
    for o in outputs:
        print('-', o)


if __name__ == '__main__':
    main()

