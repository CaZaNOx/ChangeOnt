#!/usr/bin/env python3
import re
from pathlib import Path

BLINDSPOTS = Path('TheoryOfChange_main/00_Meta/Context/AI_Deepread/BLINDSPOTS.md')
CHATS_DIR = Path('TheoryOfChange/00_Meta/AI_RecursiveChats_slim')
OUT_DIR = Path('TheoryOfChange_main/00_Meta/Context/AI_Deepread')

META_SKIP = ['hello', 'how are you', 'please confirm', 'split the file', 'sections', 'upload', 'character', 'line count', 'start section', 'Section']

RELAXED_PATTERNS = [
    r'\bshould\b', r'\bwe could\b', r'\bwe can\b', r'\btherefore\b', r'\bhence\b',
    r'\bdefine\b', r'Definition', r'protocol', r'metric', r'test', r'experiment',
    r'agent', r'architecture', r'model', r'bridge', r'phenomenolog', r'valence', r'qualia',
    r'identity', r'invariant', r'pointer', r'Reach', r'LocalReach', r'breath', r'RTV', r'\bTx\b',
    r'gauge', r'alignment', r'entropy', r'\bSE\b', r'stabilization energy', r'memory', r'drift',
    r'markov', r'closure', r'quantale', r'compose', r'join', r'proof', r'residuation'
]


def parse_ranges(md: Path):
    text = md.read_text(encoding='utf-8')
    items = []
    cur = None
    for line in text.splitlines():
        if line.startswith('## '):
            name = line[3:].strip()
            cur = name
        elif line.strip().startswith('- L') and '–' in line:
            m = re.search(r'L(\d+)–L(\d+)', line)
            if m and cur:
                a, b = int(m.group(1)), int(m.group(2))
                items.append((cur, a, b))
    return items


def review_range(chat_path: Path, a: int, b: int):
    lines = chat_path.read_text(encoding='utf-8', errors='replace').splitlines()
    hits = []
    relx = re.compile('|'.join(RELAXED_PATTERNS), re.IGNORECASE)
    for idx in range(max(1, a), min(b, len(lines)) + 1):
        ln = lines[idx - 1].strip()
        if not ln:
            continue
        low = ln.lower()
        if any(ms in low for ms in META_SKIP):
            continue
        if len(ln) >= 50 or relx.search(ln):
            hits.append((idx, ln[:220]))
    return hits


def write_review(chat_name: str, hits):
    outp = OUT_DIR / f"{chat_name.replace('.md','')}_blindspot_review.md"
    lines = []
    lines.append('---')
    lines.append(f'title: {chat_name} — Blindspot Review')
    lines.append('status: evolving')
    lines.append('tags: [meta, mapping, blindspot]')
    lines.append('---')
    lines.append(f'# {chat_name} — Blindspot Review')
    lines.append(f'Source: [[TheoryOfChange/00_Meta/AI_RecursiveChats_slim/{chat_name}]]')
    lines.append('Note: Relaxed scan over no‑hit ranges; manual follow‑up recommended.')
    lines.append('')
    if not hits:
        lines.append('- No candidate lines found under relaxed scan.')
    else:
        for idx, snippet in hits:
            lines.append(f'- L{idx}: {snippet}')
    outp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return outp


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ranges = parse_ranges(BLINDSPOTS)
    outputs = []
    for chat_name, a, b in ranges:
        chat_path = CHATS_DIR / chat_name
        if not chat_path.exists():
            continue
        hits = review_range(chat_path, a, b)
        outp = write_review(chat_name, hits)
        outputs.append(outp)
    print('Wrote blindspot review files:')
    for o in outputs:
        print('-', o)


if __name__ == '__main__':
    main()

