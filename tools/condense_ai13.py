#!/usr/bin/env python3
import re
import sys
from pathlib import Path

"""
Condense a large Markdown chat/ontology file into a short version while
preserving labeled items and section structure, and produce an audit log
of contradictions, drift, and anomalies.

Outputs:
- <out_dir>/AI_13_Short.md (content-preserving but long)
- <out_dir>/AI_13_Audit.md (flagged lines and counts)
- <out_dir>/AI_13_ShortPointers.md (compact, pointer-preserving)

Heuristics:
- Keep all headings (normalize whitespace).
- Keep all bracket labels [[FT..]], [[DF..]], [[CR..]], [[CF..]], [[DR..]], [[AS..]], [[CL..]].
- For paragraphs, keep the first sentence (trimmed) to minimize loss while
  capturing the core claim; deduplicate within a section.
- Keep tables but compress to single-line cells separated by " | ".
- Log any lines containing contradiction markers, TODOs, or flagged terms.
- Log counts and possible missing/duplicate label references.

Note: This does not do semantic contradiction detection; it flags textual
signals and structural anomalies to aid manual review.
"""

LABEL_RE = re.compile(r"\[\[[ ]*(FT|DF|DR|CR|CF|CL|AS)[^\]]*\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")
TABLE_RE = re.compile(r"^\|.*\|\s*$")
FLAG_TERMS = re.compile(
    r"(?i)\b(contradiction|performative contradiction|doesn['’]t make sense|nonsense|drift|g[oö]del|markov|todo|tbd|fixme|\?\?\?|!!!)\b"
)

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

def first_sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    # Avoid splitting on markdown links and abbreviations crudely by limiting split count
    parts = SENTENCE_SPLIT.split(text, maxsplit=1)
    head = parts[0].strip()
    # Normalize spaces
    head = re.sub(r"\s+", " ", head)
    return head

def process(in_path: Path, out_dir: Path, start: int | None = None, end: int | None = None, base: str = "AI_13") -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    # Filenames (support batch ranges)
    if start and end:
        tag = f"{start:05d}-{end:05d}"
    else:
        tag = "full"
    short_path = out_dir / f"{base}_{tag}_Short.md"
    audit_path = out_dir / f"{base}_{tag}_Audit.md"
    ptr_path = out_dir / f"{base}_{tag}_ShortPointers.md"

    label_counts = {}
    section_stack = []
    seen_in_section = set()
    lines_short = []
    lines_audit = []
    lines_ptr = []
    # Track section info for pointer summary
    current_section = {
        "level": 0,
        "title": "",
        "start": 1,
        "end": 0,
        "labels": [],
        "flags": [],
        "paragraphs": 0,
    }

    def flush_section(end_line: int):
        nonlocal current_section
        if current_section["level"] == 0:
            return
        current_section["end"] = end_line
        # Emit pointer summary line
        hdr = "#" * current_section["level"] + " " + current_section["title"]
        lines_ptr.append(hdr)
        lines_ptr.append(
            f"[L{current_section['start']}-L{current_section['end']}] labels={len(current_section['labels'])} flags={len(current_section['flags'])} paragraphs={current_section['paragraphs']}"
        )
        if current_section["labels"]:
            lines_ptr.append("Labels: " + ", ".join(current_section["labels"]))
        if current_section["flags"]:
            # keep only first sentence of flagged lines
            for L, txt in current_section["flags"]:
                lines_ptr.append(f"- L{L}: {first_sentence(txt)}")
        lines_ptr.append("")

    def enter_section(level: int, title: str, line_no: int):
        nonlocal section_stack, seen_in_section
        # Flush previous
        flush_section(line_no - 1)
        # Trim stack to level-1 depth
        while len(section_stack) >= level:
            section_stack.pop()
        section_stack.append(title.strip())
        seen_in_section = set()
        # Start new section
        current_section.clear()
        current_section.update({
            "level": level,
            "title": title.strip(),
            "start": line_no,
            "end": 0,
            "labels": [],
            "flags": [],
            "paragraphs": 0,
        })
        lines_short.append("#" * level + " " + title.strip())

    def add_short(line: str):
        if not line:
            return
        if line in seen_in_section:
            return
        seen_in_section.add(line)
        lines_short.append(line)

    with in_path.open("r", encoding="utf-8", errors="replace") as f:
        for i, raw in enumerate(f, start=1):
            if start and i < start:
                continue
            if end and i > end:
                break
            line = raw.rstrip("\n")

            # Headings
            m = HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                title = m.group(2)
                enter_section(level, title, i)
                continue

            # Labels
            labels = LABEL_RE.findall(line)
            if labels:
                # Count occurrences of each label code type; store full token for audit
                for _code in labels:
                    label_counts[_code] = label_counts.get(_code, 0) + 1
                add_short(line.strip())
                current_section["labels"].append(line.strip())

            # Tables
            elif TABLE_RE.match(line):
                # Keep as-is to preserve structure
                add_short(re.sub(r"\s+", " ", line.strip()))

            else:
                # Paragraphs / bullets: keep first sentence
                s = first_sentence(line)
                # Keep list bullets minimally
                if s.lstrip().startswith(('-', '*')):
                    add_short(s)
                else:
                    # Trim overly long sentences but keep content
                    if s:
                        # Ensure a section exists for orphan lines at batch start
                        if current_section.get("level", 0) == 0:
                            enter_section(1, f"Batch {start or 1}-{end or 'end'}", i)
                        add_short(s)
                        current_section["paragraphs"] += 1

            # Audit flags
            if FLAG_TERMS.search(line):
                lines_audit.append(f"L{i}: {line}")
                current_section["flags"].append((i, line))

    # Flush last section
    flush_section(i if 'i' in locals() else 0)

    # Audit summary header
    lines_audit.insert(0, f"File: {in_path}")
    lines_audit.insert(1, f"Labels: " + ", ".join(f"{k}={label_counts.get(k,0)}" for k in ["FT","DF","DR","CR","CF","CL","AS"]))

    short_path.write_text("\n".join(lines_short).strip() + "\n", encoding="utf-8")
    audit_path.write_text("\n".join(lines_audit).strip() + "\n", encoding="utf-8")
    ptr_path.write_text("\n".join(lines_ptr).strip() + "\n", encoding="utf-8")

def main():
    if len(sys.argv) < 3:
        print("Usage: condense_ai13.py <input_md> <output_dir> [--start N --end M --base NAME]")
        sys.exit(2)
    in_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    # parse optional args
    start = None
    end = None
    base = "AI_13"
    args = sys.argv[3:]
    i = 0
    while i < len(args):
        if args[i] == "--start" and i + 1 < len(args):
            start = int(args[i + 1])
            i += 2
        elif args[i] == "--end" and i + 1 < len(args):
            end = int(args[i + 1])
            i += 2
        elif args[i] == "--base" and i + 1 < len(args):
            base = args[i + 1]
            i += 2
        else:
            i += 1
    process(in_path, out_dir, start=start, end=end, base=base)

if __name__ == "__main__":
    main()
