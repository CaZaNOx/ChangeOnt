#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path('TheoryOfChange')
CHATS_DIR = ROOT / '00_Meta' / 'AI_RecursiveChats_slim'
OUT_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Deepread')

# Broad patterns to catch theory-bearing lines
KEY_PATTERNS = [
    r'\bdefine\b', r'Definition', r'^Let\s', r'we define', r'we propose', r'we can say', r'corollary', r'proof', r'proves', r'implies', r'therefore', r'hence', r'metric', r'measure', r'protocol', r'hypothesis', r'testbed', r'simulat', r'architecture', r'agent', r'model', r'rule', r'threshold', r'collapse', r'fixed point', r'limit cycle', r'composition', r'quantale', r'residuation', r'Boolean', r'join', r'compose', r'pointer', r'Reach', r'LocalReach', r'\bTx\b', r'frame', r'breath', r'RTV', r'identity', r'invariant', r'self-similar', r'entropy', r'\bSE\b', r'stabilization energy', r'gauge', r'alignment', r'qualia', r'valence', r'phenomenolog', r'Markov', r'closure', r'attention', r'focus', r'memory', r'drift', r'change cannot', r'continuity', r'non-cessation', r'Immediate Datum', r'performative contradiction', r'subject', r'awareness', r'\bexperience\b'
]

# Coverage hints to recognize clarifications vs new material
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

CLARIFY_CUES = ['means', 'in other words', 'i.e.', 'clarify', 'scope', 'not X but', 'not mere', 'as opposed to']

META_SKIP = ['hello', 'how are you', 'please confirm', 'split the file', 'sections', 'upload', 'character', 'line count']


def read_lines(p: Path):
    return p.read_text(encoding='utf-8', errors='replace').splitlines()


def suggest_bucket(line: str):
    l = line.lower()
    # Meta/noise
    if any(m in l for m in META_SKIP):
        return 'ignore', 'process/admin chatter'
    # Hypothesis/test ideas
    if any(k in l for k in ['hypothesis', 'we could test', 'experiment', 'testbed', 'simulate', 'simulation', 'protocol', 'metric', 'measure', 'agent', 'architecture']):
        return 'hypothesis', 'test/metric/protocol/architecture cue'
    # New definition/derivation
    if re.search(r'\bdefine\b|Definition|^Let\s|we define', line):
        return 'new_df_dr', 'explicit definitional/derivation phrasing'
    # Corollary/add-child
    if any(k in l for k in ['corollary', 'implies', 'therefore', 'hence']):
        return 'add_child', 'implication/corollary phrasing'
    # Clarification to existing
    if any(k in l for k in CLARIFY_CUES) and any(h in l for h in COVERAGE_HINTS.keys()):
        return 'add_to_existing', 'clarification phrasing over known concept'
    # Otherwise undecided but interesting
    return 'needs_review', 'generic theory-bearing cue'


def scan_chat(chat: Path):
    lines = read_lines(chat)
    entries = []
    key_re = re.compile('|'.join(KEY_PATTERNS), re.IGNORECASE)
    for i, line in enumerate(lines, start=1):
        if not key_re.search(line):
            continue
        bucket, rationale = suggest_bucket(line)
        # coverage hint (best-effort)
        cover = ''
        for k, slug in COVERAGE_HINTS.items():
            if k in line.lower():
                cover = slug
                break
        snippet = line.strip().replace('\t', ' ')[:200]
        entries.append((i, bucket, rationale, cover, snippet))
    return entries


def write_deepread(chat: Path, entries):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{chat.stem}_deepread.md"
    counts = Counter(b for _, b, *_ in entries)
    lines = []
    lines.append('---')
    lines.append(f'title: {chat.stem} — Deepread Pointers')
    lines.append('status: evolving')
    lines.append('tags: [meta, mapping, deepread]')
    lines.append('---')
    lines.append(f'# {chat.stem} — Deepread Pointers')
    lines.append(f'Source: [[{chat.as_posix()}]]')
    lines.append('Note: First-pass shallow scan. Record all interesting lines with suggested bucket and brief rationale.')
    lines.append('')
    lines.append('## Summary')
    for k in ['add_to_existing','add_child','new_df_dr','hypothesis','needs_review','ignore']:
        if counts[k]:
            lines.append(f'- {k}: {counts[k]}')
    lines.append('')
    lines.append('## Pointers')
    for i, bucket, rationale, cover, snippet in entries:
        cover_note = f' | covers: {cover}' if cover else ''
        lines.append(f'- L{i}: [{bucket}] {rationale}{cover_note} — {snippet}')
    lines.append('')
    out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return out_path


def main():
    chats = sorted([p for p in CHATS_DIR.glob('AI_*') if p.suffix == '.md'])
    outs = []
    for chat in chats:
        entries = scan_chat(chat)
        outp = write_deepread(chat, entries)
        outs.append(outp)
    print('Deepread pointer files written:')
    for o in outs:
        print('-', o)


if __name__ == '__main__':
    main()

