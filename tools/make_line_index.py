#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict

CHAT = Path('TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_3_Amavai_RecursiveChat.md')
OUT = Path('TheoryOfChange_main/00_Meta/Context/AI_3_line_index.md')

CATEGORIES = {
    'foundations': [r'Immediate Datum', r'performative contradiction', r'performative-contradiction'],
    'triad': [r'\bsubject\b', r'awareness', r'\bexperience\b'],
    'pointer_reach_tx': [r'pointer', r'Reach', r'LocalReach', r'\bTx\b', r'frame'],
    'breath_rtv': [r'breath', r'RTV', r'collapse threshold', r'fixed point', r'limit cycle'],
    'identity_invariants': [r'identity', r'invariant', r'self-similar'],
    'entropy_se_gauge': [r'entropy', r'SE', r'stabilization energy', r'gauge', r'alignment'],
    'qualia_valence': [r'qualia', r'valence', r'phenomenolog'],
    'math_logic': [r'quantale', r'residuation', r'proof', r'evidence', r'Boolean'],
    'markov_closure': [r'Markov', r'closure'],
    'attention': [r'Attention', r'attention', r'focus'],
    'prm': [r'PRM', r'primitive', r'dissociation', r'cascade'],
}


def read_lines(p: Path):
    return p.read_text(encoding='utf-8', errors='replace').splitlines()


def find_matches(lines):
    cat_hits = defaultdict(list)
    for i, line in enumerate(lines, start=1):
        for cat, pats in CATEGORIES.items():
            for pat in pats:
                if re.search(pat, line, re.IGNORECASE):
                    cat_hits[cat].append(i)
                    break
    return cat_hits


def compress_ranges(sorted_lines, gap=3):
    if not sorted_lines:
        return []
    ranges = []
    start = prev = sorted_lines[0]
    for n in sorted_lines[1:]:
        if n <= prev + gap:
            prev = n
            continue
        ranges.append((start, prev))
        start = prev = n
    ranges.append((start, prev))
    return ranges


def main():
    lines = read_lines(CHAT)
    hits = find_matches(lines)
    out = []
    out.append('---')
    out.append('title: AI_3 Line Index — Theory-bearing Segments')
    out.append('status: evolving')
    out.append('tags: [meta, mapping, AI_3, index]')
    out.append('---')
    out.append('# AI_3 Line Index — Theory-bearing Segments')
    out.append('Source: [[TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_3_Amavai_RecursiveChat]]')
    out.append('Note: Ranges group nearby hits; use as lookup anchors for deep review.')
    out.append('')
    for cat in CATEGORIES:
        rngs = compress_ranges(sorted(set(hits.get(cat, []))))
        out.append(f'## {cat.replace("_"," ").title()}')
        if not rngs:
            out.append('- (no matches)')
        else:
            for a, b in rngs:
                if a == b:
                    out.append(f'- L{a}')
                else:
                    out.append(f'- L{a}–L{b}')
        out.append('')
    OUT.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'Wrote line index: {OUT}')


if __name__ == '__main__':
    main()

