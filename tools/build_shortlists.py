#!/usr/bin/env python3
import re
from pathlib import Path

IN_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Deepread')
OUT_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Shortlists')

TARGET_HINTS = [
    (r'quantale|residuation|boolean|compose|join', 'DF/DR: quantale logic family'),
    (r'markov|closure', 'DF: markov-closure-assumption'),
    (r'pointer|localreach|reach|tx|frame', 'DF/CR: pointer/reach/Tx cluster'),
    (r'breath|rtv|collapse threshold|fixed point|limit cycle', 'DF/DR: breath/RTV cluster'),
    (r'identity|invariant|≈|similarity', 'DF: identity invariants / similarity'),
    (r'entropy|stabilization energy|\bSE\b|gauge|alignment|Γ', 'DF: entropy / SE / gauge'),
    (r'qualia|valence|phenomenolog', 'CL/CR: qualia-gauge curvature / emotion recursive valuation'),
    (r'attention|focus', 'DF/CL: attention-focus / thresholds'),
    (r'prm|metric|measure|protocol', 'DF/HYP: PRM metrics / protocols'),
]


def suggest_target(snippet: str, cover: str) -> str:
    if cover:
        return f'covers {cover} — consider CL add-to-existing or CR add-child'
    for pat, tgt in TARGET_HINTS:
        if re.search(pat, snippet, re.IGNORECASE):
            return tgt
    return 'To triage: map to nearest DF/CR/CL/HYP'


def parse_deepread(path: Path):
    entries = []
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'^- L(\d+): \[(.*?)\] .*?(?:\| covers: ([^\]]+))? — (.*)$', line)
        if m:
            ln = int(m.group(1))
            bucket = m.group(2)
            cover = (m.group(3) or '').strip()
            snippet = m.group(4).strip()
            entries.append((ln, bucket, cover, snippet))
    return entries


def pick_top(entries, per_bucket=5):
    buckets = {'add_to_existing': [], 'add_child': [], 'new_df_dr': [], 'hypothesis': []}
    for ln, bucket, cover, snippet in entries:
        if bucket in buckets and len(buckets[bucket]) < per_bucket:
            buckets[bucket].append((ln, cover, snippet))
    return buckets


def write_shortlist(name: str, buckets):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outp = OUT_DIR / f'{name}_shortlist.md'
    lines = []
    lines.append('---')
    lines.append(f'title: {name} — Prioritized Shortlist (first-pass)')
    lines.append('status: evolving')
    lines.append('tags: [meta, shortlist, promotion]')
    lines.append('---')
    lines.append(f'# {name} — Prioritized Shortlist (first-pass)')
    lines.append(f'Source: [[TheoryOfChange_main/00_Meta/Context/AI_Deepread/{name}_deepread.md]]')
    lines.append('Note: Top items per bucket from deepread; targets are suggestions.')
    lines.append('')
    for bucket in ['add_to_existing','add_child','new_df_dr','hypothesis']:
        items = buckets[bucket]
        lines.append(f'## {bucket}')
        if not items:
            lines.append('- (none)')
        else:
            for ln, cover, snippet in items:
                target = suggest_target(snippet, cover)
                cover_note = f' (covers: {cover})' if cover else ''
                lines.append(f'- L{ln}{cover_note}: {snippet} → {target}')
        lines.append('')
    outp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return outp


def main():
    outputs = []
    for p in sorted(IN_DIR.glob('AI_*_deepread.md')):
        name = p.stem.replace('_deepread','')
        entries = parse_deepread(p)
        buckets = pick_top(entries, per_bucket=5)
        outp = write_shortlist(name, buckets)
        outputs.append(outp)
    print('Shortlists written:')
    for o in outputs:
        print('-', o)


if __name__ == '__main__':
    main()

