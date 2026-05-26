#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path('TheoryOfChange_main')
STATEMENTS_DIR = ROOT / '01_Statements'
SYMBOLS_DIR = STATEMENTS_DIR / 'SYMBOLS'

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)
WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

def collect_symbol_usage():
    usage = {}
    for p in STATEMENTS_DIR.rglob('*.md'):
        if p.is_dir() or p.parts[-2] == 'SYMBOLS':
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        m = FRONTMATTER_RE.search(text)
        if not m:
            continue
        fm = m.group(1)
        # Extract symbols_used array text robustly (can span lines)
        sym_block = ''
        cap = False
        for line in fm.splitlines():
            if line.startswith('symbols_used:'):
                cap = True
                sym_block += line.split(':',1)[1] + '\n'
                continue
            if cap:
                sym_block += line + '\n'
                if ']' in line:
                    break
        if not sym_block:
            continue
        for wk in WIKILINK_RE.findall(sym_block):
            sym_path = wk.strip().rstrip('.md')
            usage.setdefault(sym_path, set()).add(p.relative_to(ROOT).with_suffix('').as_posix())
    return {k: sorted(v) for k, v in usage.items()}

def update_used_in(symbol_file: Path, links: list[str]):
    text = symbol_file.read_text(encoding='utf-8', errors='replace')
    used_in_header = '\n## Used In\n'
    # Build new section
    lines = [used_in_header]
    for s in links:
        # Convert absolute path to repo-relative wiki link without extension
        rel = Path(s).as_posix()
        lines.append(f'- [[{rel}]]')
    new_block = '\n'.join(lines) + '\n'

    if '## Used In' in text:
        # Replace existing Used In section until next heading or end
        parts = text.split('## Used In')
        prefix = parts[0]
        rest = '## Used In' + parts[1]
        # find next heading after Used In
        m = re.search(r'\n##\s+', rest)
        if m:
            updated = prefix + new_block + rest[m.start()+1:]
        else:
            updated = prefix + new_block
        symbol_file.write_text(updated, encoding='utf-8')
    else:
        # Append section at end
        if not text.endswith('\n'):
            text += '\n'
        text += new_block
        symbol_file.write_text(text, encoding='utf-8')

def main():
    usage = collect_symbol_usage()
    for sym_md in SYMBOLS_DIR.glob('*.md'):
        key = sym_md.relative_to(ROOT).with_suffix('').as_posix()
        links = usage.get(key, [])
        update_used_in(sym_md, links)
    print('Updated Used In for symbols:', len(list(SYMBOLS_DIR.glob('*.md'))))

if __name__ == '__main__':
    main()
