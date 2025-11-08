#!/usr/bin/env python3
import re
import yaml
from pathlib import Path

ROOT = Path('TheoryOfChange_main')
STATEMENTS_DIR = ROOT / '01_Statements'
SYMBOLS_DIR = STATEMENTS_DIR / 'SYMBOLS'
CONCEPTS_DIR = ROOT / '02_Concepts'

FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)
WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

# Sentinel markers to guard auto-generated sections
RB_BEGIN = '<!-- BEGIN:AUTOGEN:REFERENCED_BY -->'
RB_END = '<!-- END:AUTOGEN:REFERENCED_BY -->'
REL_BEGIN = '<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->'
REL_END = '<!-- END:AUTOGEN:RELATIONSHIPS -->'
UI_BEGIN = '<!-- BEGIN:AUTOGEN:USED_IN -->'
UI_END = '<!-- END:AUTOGEN:USED_IN -->'

def frontmatter(text: str):
    m = FM_RE.search(text)
    return m.group(1) if m else ''

def collect_stmt_links():
    refs = {}  # target -> set(sources)
    stmts = []
    for p in STATEMENTS_DIR.rglob('*.md'):
        # Skip symbol files
        if p.parts[-2] == 'SYMBOLS' or p.name == 'README.md':
            continue
        t = p.read_text(encoding='utf-8', errors='replace')
        fm = frontmatter(t)
        if not fm:
            continue
        # capture block of arrays lines could span
        block = {}
        key = None
        acc = []
        for line in fm.splitlines():
            if any(line.startswith(k+':') for k in ['parents','dependencies','successors']):
                if key and acc:
                    block[key] = '\n'.join(acc)
                key = line.split(':',1)[0]
                acc = [line.split(':',1)[1]]
            elif key:
                acc.append(line)
                if ']' in line:
                    block[key] = '\n'.join(acc)
                    key=None
                    acc=[]
        if key and acc:
            block[key] = '\n'.join(acc)

        used = set()
        for arr in block.values():
            for wk in WIKILINK_RE.findall(arr):
                target = wk.strip().rstrip('.md')
                used.add(target)
        src = p.relative_to(ROOT).with_suffix('').as_posix()
        for tgt in used:
            refs.setdefault(tgt, set()).add(src)
        stmts.append(src)
    return refs

def _replace_block(text: str, begin: str, end: str, new_block: str, fallback_heading: str | None = None) -> str:
    if begin in text and end in text:
        pre = text.split(begin, 1)[0]
        post = text.split(end, 1)[1]
        return pre + new_block + post
    # fallback: try by heading if present
    if fallback_heading and fallback_heading in text:
        pre, rest = text.split(fallback_heading, 1)
        m = re.search(r'\n##\s+', rest)
        if m:
            return pre + new_block + rest[m.start()+1:]
        else:
            return pre + new_block
    # else append
    if not text.endswith('\n'):
        text += '\n'
    return text + new_block

def update_referenced_by(stmt_file: Path, links: list[str]):
    text = stmt_file.read_text(encoding='utf-8', errors='replace')
    header = '## Referenced By\n'
    body = '\n'.join(f'- [[{l}]]' for l in sorted(links)) + '\n'
    block = f"\n{RB_BEGIN}\n{header}{body}{RB_END}\n"
    new_text = _replace_block(text, RB_BEGIN, RB_END, block, fallback_heading='## Referenced By')
    stmt_file.write_text(new_text, encoding='utf-8')

def extract_frontmatter_links(fm: str, key: str) -> list[str]:
    lines = fm.splitlines()
    block = ''
    cap = False
    for line in lines:
        if line.startswith(key+':'):
            cap = True
            block += line.split(':',1)[1] + '\n'
            continue
        if cap:
            block += line + '\n'
            if ']' in line:
                break
    return [wk.strip() for wk in WIKILINK_RE.findall(block)] if block else []

def update_relationships(stmt_file: Path, fm_text: str):
    # Prefer YAML parsing for accuracy
    try:
        data = yaml.safe_load('---\n' + fm_text + '\n') or {}
    except Exception:
        data = {}
    def norm_list(key):
        out = []
        for v in (data.get(key) or []):
            if isinstance(v, str):
                m = WIKILINK_RE.search(v)
                out.append(m.group(1).strip() if m else v)
        # dedupe, preserve order
        seen = set()
        res = []
        for x in out:
            if x not in seen:
                seen.add(x)
                res.append(x)
        return res
    concepts = norm_list('concepts')
    parents = norm_list('parents')
    deps = norm_list('dependencies')
    succ = norm_list('successors')
    # Build block
    header = '## Relationships\n'
    lines = [header]
    if concepts:
        lines.append('- Concepts: ' + '; '.join(f'[[{c}]]' for c in concepts))
    if parents:
        lines.append('- Parents: ' + '; '.join(f'[[{p}]]' for p in parents))
    if deps:
        lines.append('- Dependencies: ' + '; '.join(f'[[{d}]]' for d in deps))
    if succ:
        lines.append('- Successors: ' + '; '.join(f'[[{s}]]' for s in succ))
    block = f"\n{REL_BEGIN}\n" + '\n'.join(lines) + "\n" + f"{REL_END}\n"

    text = stmt_file.read_text(encoding='utf-8', errors='replace')
    new_text = _replace_block(text, REL_BEGIN, REL_END, block, fallback_heading='## Relationships')
    stmt_file.write_text(new_text, encoding='utf-8')

def collect_symbol_usage():
    """Collect symbol usage from statements by looking at:
    - frontmatter symbols_used array (expects path-style wikilinks)
    - wikilinks in the body that point to 01_Statements/SYMBOLS/* (path-style)
    - wikilinks in the body that match a SYMBOLS file stem (short-note style, e.g., [[Sigma_epsilon]])
    """
    # Build resolver for short-note symbol links
    stem_to_path = {}
    for sp in SYMBOLS_DIR.glob('*.md'):
        stem = sp.stem  # e.g., 'Sigma_epsilon'
        rel = sp.relative_to(ROOT).with_suffix('').as_posix()
        stem_to_path[stem] = rel

    usage = {}
    for p in STATEMENTS_DIR.rglob('*.md'):
        if p.parts[-2] == 'SYMBOLS' or p.name == 'README.md':
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        fm = frontmatter(text)
        # 1) symbols_used in frontmatter
        if fm:
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
            for wk in WIKILINK_RE.findall(sym_block):
                sym = wk.strip().rstrip('.md')
                usage.setdefault(sym, set()).add(p.relative_to(ROOT).with_suffix('').as_posix())
        # 2) wikilinks in body to symbol pages or short-note symbol names
        body = text
        m = FM_RE.search(text)
        if m:
            body = text[m.end():]
        for wk in WIKILINK_RE.findall(body):
            target_raw = wk.strip()
            target = target_raw.split('|',1)[0].rstrip('.md')  # strip alias and .md
            key = None
            if target.startswith('01_Statements/SYMBOLS/'):
                key = target
            elif target in stem_to_path:
                key = stem_to_path[target]
            if key:
                usage.setdefault(key, set()).add(p.relative_to(ROOT).with_suffix('').as_posix())
    return usage

def update_symbol_used_in(usage):
    for sym_md in SYMBOLS_DIR.glob('*.md'):
        key = sym_md.relative_to(ROOT).with_suffix('').as_posix()
        links = sorted(usage.get(key, []))
        text = sym_md.read_text(encoding='utf-8', errors='replace')
        header = '## Used In\n'
        body = '\n'.join(f'- [[{l}]]' for l in links) + '\n'
        block = f"\n{UI_BEGIN}\n{header}{body}{UI_END}\n"
        new_text = _replace_block(text, UI_BEGIN, UI_END, block, fallback_heading='## Used In')
        sym_md.write_text(new_text, encoding='utf-8')

def main():
    # Update Referenced By in statements
    refs = collect_stmt_links()
    for p in STATEMENTS_DIR.rglob('*.md'):
        if p.parts[-2] == 'SYMBOLS' or p.name == 'README.md':
            continue
        key = p.relative_to(ROOT).with_suffix('').as_posix()
        incoming = sorted(refs.get(key, []))
        update_referenced_by(p, incoming)
        # update relationships from frontmatter
        t = p.read_text(encoding='utf-8', errors='replace')
        m = FM_RE.search(t)
        if m:
            fm_text = m.group(1)
            update_relationships(p, fm_text)
    # Update symbol Used In
    usage = collect_symbol_usage()
    update_symbol_used_in(usage)
    # Update concept relationships (statements referencing concept; linked concepts in body)
    concept_usage = {}
    for sp in STATEMENTS_DIR.rglob('*.md'):
        if sp.parts[-2] == 'SYMBOLS' or sp.name == 'README.md':
            continue
        txt = sp.read_text(encoding='utf-8', errors='replace')
        m = FM_RE.search(txt)
        if not m:
            continue
        try:
            data = yaml.safe_load('---\n' + m.group(1) + '\n') or {}
        except Exception:
            data = {}
        for v in (data.get('concepts') or []):
            if isinstance(v, str):
                mw = WIKILINK_RE.search(v)
                if mw:
                    cpath = mw.group(1).strip().rstrip('.md')
                    concept_usage.setdefault(cpath, set()).add(sp.relative_to(ROOT).with_suffix('').as_posix())

    def update_concept_relationships(cfile: Path):
        text = cfile.read_text(encoding='utf-8', errors='replace')
        # statements referencing this concept
        key = cfile.relative_to(ROOT).with_suffix('').as_posix()
        stmts = sorted(concept_usage.get(key, []))
        # linked concepts in body
        body = text
        bm = FM_RE.search(text)
        if bm:
            body = text[bm.end():]
        linked = []
        for wk in WIKILINK_RE.findall(body):
            if wk.startswith('02_Concepts/'):
                if wk.rstrip('.md') != key and f'[[{wk}]]' not in linked:
                    linked.append(f'[[{wk}]]')
        header = '## Relationships\n'
        lines = [header]
        if stmts:
            lines.append('### Statements')
            for s in stmts:
                lines.append(f'- [[{s}]]')
        if linked:
            lines.append('### Linked Concepts')
            for c in linked:
                lines.append(f'- {c}')
        block = f"\n{REL_BEGIN}\n" + '\n'.join(lines) + "\n" + f"{REL_END}\n"
        new_text = _replace_block(text, REL_BEGIN, REL_END, block, fallback_heading='## Relationships')
        cfile.write_text(new_text, encoding='utf-8')

    for cp in CONCEPTS_DIR.glob('*.md'):
        if cp.name == 'README.md':
            continue
        update_concept_relationships(cp)

    print('Updated Referenced By for statements, Relationships for statements, Used In for symbols, and Relationships for concepts.')

if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
