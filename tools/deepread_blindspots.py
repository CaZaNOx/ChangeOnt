#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path('TheoryOfChange')
CHATS_DIR = ROOT / '00_Meta' / 'AI_RecursiveChats_slim'
OUT = Path('TheoryOfChange_main/00_Meta/Context/AI_Deepread/BLINDSPOTS.md')

# Must match the broad scan in deepread_ai_chats.py to ensure comparable coverage
KEY_PATTERNS = [
    r'\bdefine\b', r'Definition', r'^Let\s', r'we define', r'we propose', r'we can say', r'corollary', r'proof', r'proves', r'implies', r'therefore', r'hence', r'metric', r'measure', r'protocol', r'hypothesis', r'testbed', r'simulat', r'architecture', r'agent', r'model', r'rule', r'threshold', r'collapse', r'fixed point', r'limit cycle', r'composition', r'quantale', r'residuation', r'Boolean', r'join', r'compose', r'pointer', r'Reach', r'LocalReach', r'\bTx\b', r'frame', r'breath', r'RTV', r'identity', r'invariant', r'self-similar', r'entropy', r'\bSE\b', r'stabilization energy', r'gauge', r'alignment', r'qualia', r'valence', r'phenomenolog', r'Markov', r'closure', r'attention', r'focus', r'memory', r'drift', r'change cannot', r'continuity', r'non-cessation', r'Immediate Datum', r'performative contradiction', r'subject', r'awareness', r'\bexperience\b'
]


def read_lines(p: Path):
    return p.read_text(encoding='utf-8', errors='replace').splitlines()


def scan_hits(lines):
    key_re = re.compile('|'.join(KEY_PATTERNS), re.IGNORECASE)
    hits = [i for i, ln in enumerate(lines, start=1) if key_re.search(ln or '')]
    return hits


def ranges_from_hits(total_lines: int, hits: list[int], max_gap=200):
    # Build ranges of consecutive no-hit segments with length >= max_gap
    hit_set = set(hits)
    no_ranges = []
    start = None
    for i in range(1, total_lines + 1):
        if i not in hit_set:
            if start is None:
                start = i
        else:
            if start is not None:
                end = i - 1
                if end - start + 1 >= max_gap:
                    no_ranges.append((start, end))
                start = None
    if start is not None:
        end = total_lines
        if end - start + 1 >= max_gap:
            no_ranges.append((start, end))
    return no_ranges


def density_by_chunk(total_lines: int, hits: list[int], chunk=1000):
    buckets = {}
    for h in hits:
        idx = (h - 1) // chunk
        buckets[idx] = buckets.get(idx, 0) + 1
    out = []
    chunks = (total_lines + chunk - 1) // chunk
    for idx in range(chunks):
        out.append((idx + 1, buckets.get(idx, 0)))
    return out


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append('---')
    lines.append('title: Deepread Blindspots and Density — AI_1..AI_18')
    lines.append('status: evolving')
    lines.append('tags: [meta, mapping, deepread, blindspots]')
    lines.append('---')
    lines.append('# Deepread Blindspots and Density — AI_1..AI_18')
    lines.append('Note: Long no-hit ranges (>=200 lines) and hit density per 1000 lines to prioritize manual skim where needed.')
    lines.append('')
    chats = sorted([p for p in CHATS_DIR.glob('AI_*') if p.suffix == '.md'])
    for chat in chats:
        L = read_lines(chat)
        hits = scan_hits(L)
        no_ranges = ranges_from_hits(len(L), hits, max_gap=200)
        dens = density_by_chunk(len(L), hits, chunk=1000)
        lines.append(f'## {chat.name}')
        lines.append(f'- Total lines: {len(L)}; Hits: {len(hits)}')
        lines.append('- Long no-hit ranges (>=200 lines):')
        if no_ranges:
            for a, b in no_ranges:
                lines.append(f'  - L{a}–L{b} (len {b-a+1})')
        else:
            lines.append('  - None')
        lines.append('- Density (hits per 1000 lines):')
        lines.append('  - ' + ', '.join([f'{idx}:{cnt}' for idx, cnt in dens]))
        lines.append('')
    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Wrote: {OUT}')


if __name__ == '__main__':
    main()

