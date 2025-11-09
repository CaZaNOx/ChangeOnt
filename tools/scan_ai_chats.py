#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path('TheoryOfChange')
CHATS_DIR = ROOT / '00_Meta' / 'AI_RecursiveChats_slim'
OUT_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Pointers')

# Heuristic categories and patterns (broad to avoid missing content)
CATEGORIES = {
    'foundations': [r'Immediate Datum', r'performative contradiction', r'performative-contradiction', r'change cannot (have a )?begin', r'continuity', r'non-cessation'],
    'triad': [r'\bsubject\b', r'awareness', r'\bexperience\b'],
    'pointer_reach_tx': [r'pointer', r'Reach', r'LocalReach', r'\bTx\b', r'frame'],
    'breath_rtv': [r'breath', r'RTV', r'collapse threshold', r'fixed point', r'limit cycle'],
    'identity_invariants': [r'identity', r'invariant', r'self-similar', r'persist', r'stabiliz'],
    'entropy_se_gauge': [r'entropy', r'\bSE\b', r'stabilization energy', r'gauge', r'alignment', r'Γ'],
    'qualia_valence': [r'qualia', r'valence', r'phenomenolog'],
    'math_logic': [r'quantale', r'residuation', r'proof', r'evidence', r'Boolean', r'join', r'compose', r'⊕', r'⊗'],
    'markov_closure': [r'Markov', r'closure'],
    'attention': [r'Attention', r'attention', r'focus'],
    'prm': [r'PRM', r'primitive', r'dissociation', r'cascade', r'loopiness', r'temporal ops', r'MDL', r'variable birth', r'bend metric'],
}

# Simple coverage keywords mapped to known statement slugs (approximate)
COVERAGE_HINTS = {
    'immediate datum': 'S-FT-immediate-datum',
    'performative contradiction': 'S-DF-performative-contradiction',
    'change cannot begin': 'S-DR-change-cannot-begin',
    'continuity': 'S-FT-continuity-noncessation',
    'pointer': 'S-DF-pointer-structural',
    'reach': 'S-DF-reach-relation',
    'localreach': 'S-DF-localreach-topology',
    'rtv': 'S-DF-rtv-operator',
    'breath': 'S-DR-breath-stabilization',
    'identity': 'S-DF-identity-through-change',
    'invariant': 'S-DF-identity-invariants',
    'entropy': 'S-DF-entropy-co',
    'stabilization energy': 'S-DF-stabilization-energy',
    'gauge': 'S-DF-gauge-alignment-field',
    'qualia': 'S-CR-qualia-gauge-curvature',
    'quantale': 'S-DF-quantale-logic',
    'residuation': 'S-DR-quantale-residuation-implication',
    'boolean': 'S-DR-quantale-boolean-flattening-proof',
    'markov': 'S-DF-markov-closure-assumption',
    'attention': 'S-DF-attention-focus',
    'prm': 'S-DF-prm-change-ops',
}


def read_lines(p: Path):
    return p.read_text(encoding='utf-8', errors='replace').splitlines()


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


def classify_line(line: str):
    l = line.lower()
    for key, slug in COVERAGE_HINTS.items():
        if key in l:
            return ('covered-likely', slug)
    # Hypothesis cues
    if any(k in l for k in ['hypothesis', 'we could test', 'simulate', 'metric', 'measure', 'protocol', 'testbed', 'we propose']):
        return ('hypothesis-candidate', '')
    return ('needs-review', '')


def scan_file(p: Path):
    lines = read_lines(p)
    hits = defaultdict(list)
    classifications = []
    for i, line in enumerate(lines, start=1):
        matched = False
        for cat, pats in CATEGORIES.items():
            if any(re.search(pat, line, re.IGNORECASE) for pat in pats):
                hits[cat].append(i)
                matched = True
        if matched:
            cls, slug = classify_line(line)
            classifications.append((i, cls, slug, line.strip()[:180]))
    return hits, classifications


def write_report(chat: Path, hits, classes):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{chat.stem}_pointers.md"
    out = []
    out.append('---')
    out.append(f'title: {chat.stem} — Theory-bearing Pointers')
    out.append('status: evolving')
    out.append('tags: [meta, mapping, pointers]')
    out.append('---')
    out.append(f'# {chat.stem} — Theory-bearing Pointers')
    out.append(f'Source: [[{chat.as_posix()}]]')
    out.append('')
    out.append('## Grouped Line Ranges (by category)')
    for cat in CATEGORIES.keys():
        rngs = compress_ranges(sorted(set(hits.get(cat, []))))
        out.append(f'### {cat.replace("_"," ").title()}')
        if not rngs:
            out.append('- (no matches)')
        else:
            out += [f'- L{a}–L{b}' if a != b else f'- L{a}' for a, b in rngs]
        out.append('')
    out.append('## Classified Snippets (review queue)')
    out.append('- covered-likely: likely already formalized; confirm or link to existing statement')
    out.append('- needs-review: inspect for potential CL/CR/DF')
    out.append('- hypothesis-candidate: route to HYP with a test sketch')
    out.append('')
    for i, cls, slug, snippet in classes:
        slug_note = f' [{slug}]' if slug else ''
        out.append(f'- L{i}: {cls}{slug_note} — {snippet}')
    out.append('')
    out_path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    return out_path


def main():
    chats = sorted([p for p in CHATS_DIR.glob('AI_*') if p.suffix == '.md'])
    outputs = []
    for chat in chats:
        hits, classes = scan_file(chat)
        outp = write_report(chat, hits, classes)
        outputs.append(outp)
    print('Wrote pointer reports:')
    for o in outputs:
        print('-', o)


if __name__ == '__main__':
    main()

