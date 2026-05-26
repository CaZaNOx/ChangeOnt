#!/usr/bin/env python3
import re
import sys
from pathlib import Path

"""
Merge and prune batch ShortPointers/Audit/Short outputs to a compact,
deduplicated, theory-focused set:

Inputs (dir): files like AI_13_00001-05000_ShortPointers.md, ..._Audit.md

Pruning rules (conservative, editable):
- Drop sections with labels=0 and flags=0 (assume meta/back-and-forth without theory).
- Keep all sections with labels>0 OR flags>0.
- Deduplicate labels globally (exact string match of token line).
- Deduplicate flagged sentences globally by normalized text (first sentence already provided).

Outputs in the same dir:
- AI_13_MERGED_ShortPointers.md (merged kept sections with deduped labels/flags)
- AI_13_MERGED_Audit.md (merged flagged lines, deduped by content)
- AI_13_MERGED_Short.md (for each kept section: heading, unique labels, unique flagged lines)
"""

HDR_RE = re.compile(r"^(#{1,6})\s+(.*)$")
META_RE = re.compile(r"^\[L(\d+)-L(\d+)\]\s+labels=(\d+)\s+flags=(\d+)\s+paragraphs=(\d+)")
LABELS_RE = re.compile(r"^Labels:\s*(.*)$")
FLAG_LINE_RE = re.compile(r"^-\s+L(\d+):\s*(.*)$")

def parse_pointer_file(path: Path):
    sections = []
    current = None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = HDR_RE.match(raw)
        if m:
            if current:
                sections.append(current)
            current = {
                "level": len(m.group(1)),
                "title": m.group(2).strip(),
                "lstart": None,
                "lend": None,
                "labels": [],
                "flags": [],
                "paragraphs": 0,
                "source": path.name,
            }
            continue
        if current is None:
            # allow a preface header-less meta line like "# Batch ..."
            continue
        m2 = META_RE.match(raw)
        if m2:
            current["lstart"] = int(m2.group(1))
            current["lend"] = int(m2.group(2))
            # we could record the counts but we'll compute from lists
            continue
        m3 = LABELS_RE.match(raw)
        if m3:
            labels_str = m3.group(1).strip()
            if labels_str:
                # labels stored as raw tokens separated by ", "
                for tok in labels_str.split(", "):
                    if tok:
                        current["labels"].append(tok)
            continue
        m4 = FLAG_LINE_RE.match(raw)
        if m4:
            current["flags"].append((int(m4.group(1)), m4.group(2).strip()))
            continue
        # ignore other lines
    if current:
        sections.append(current)
    return sections

def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip()).lower()

def merge_prune(in_dir: Path, base_prefix: str = "AI_13"):
    pointer_paths = sorted(in_dir.glob(f"{base_prefix}_*_ShortPointers.md"))
    audit_paths = sorted(in_dir.glob(f"{base_prefix}_*_Audit.md"))

    # Parse sections from pointers
    sections = []
    for p in pointer_paths:
        try:
            sections.extend(parse_pointer_file(p))
        except Exception as e:
            print(f"WARN: failed to parse {p}: {e}", file=sys.stderr)

    # Keep only theory-bearing sections
    kept = []
    for s in sections:
        if (s["labels"] or s["flags"]):
            kept.append(s)

    # Deduplicate labels and flags globally
    seen_labels = set()
    seen_flags = set()
    for s in kept:
        uniq_labels = []
        for tok in s["labels"]:
            key = normalize_text(tok)
            if key not in seen_labels:
                seen_labels.add(key)
                uniq_labels.append(tok)
        s["labels"] = uniq_labels
        uniq_flags = []
        for L, txt in s["flags"]:
            key = normalize_text(txt)
            if key not in seen_flags:
                seen_flags.add(key)
                uniq_flags.append((L, txt))
        s["flags"] = uniq_flags

    # Write merged ShortPointers
    mp = in_dir / f"{base_prefix}_MERGED_ShortPointers.md"
    out_lines = []
    for s in kept:
        out_lines.append("#" * s["level"] + " " + s["title"])
        out_lines.append(f"[L{s['lstart']}-L{s['lend']}] labels={len(s['labels'])} flags={len(s['flags'])}")
        if s["labels"]:
            out_lines.append("Labels: " + ", ".join(s["labels"]))
        for L, txt in s["flags"]:
            out_lines.append(f"- L{L}: {txt}")
        out_lines.append("")
    mp.write_text("\n".join(out_lines).strip() + "\n", encoding="utf-8")

    # Write merged Audit
    ma = in_dir / f"{base_prefix}_MERGED_Audit.md"
    audit_lines = ["Merged flagged lines (deduplicated by text):"]
    for s in kept:
        for L, txt in s["flags"]:
            audit_lines.append(f"L{L}: {txt}")
    ma.write_text("\n".join(audit_lines).strip() + "\n", encoding="utf-8")

    # Write merged Short (heading + labels + flags only)
    ms = in_dir / f"{base_prefix}_MERGED_Short.md"
    short_lines = []
    for s in kept:
        short_lines.append("#" * s["level"] + " " + s["title"])
        # Keep theory-bearing tokens
        for tok in s["labels"]:
            short_lines.append(tok)
        # Keep flagged lines as bullets
        for _, txt in s["flags"]:
            short_lines.append(f"- {txt}")
        short_lines.append("")
    ms.write_text("\n".join(short_lines).strip() + "\n", encoding="utf-8")

def main():
    if len(sys.argv) < 2:
        print("Usage: merge_prune_ai13.py <summaries_dir> [--base PREFIX]")
        sys.exit(2)
    in_dir = Path(sys.argv[1])
    base = "AI_13"
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--base" and i + 1 < len(args):
            base = args[i + 1]
            i += 2
        else:
            i += 1
    merge_prune(in_dir, base_prefix=base)

if __name__ == "__main__":
    main()

