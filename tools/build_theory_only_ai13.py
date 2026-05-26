#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from collections import defaultdict

"""
Build a single theory-only document from AI_13 by:
- Including all labeled items (FT/DF/DR/CR/CF/CL/AS) with surrounding context.
- Including unlabeled theory-relevant lines (based on cues/keywords) and assigning a synthetic label.
- Merging repeated content into concept sections; enriching with new info.
- Preserving original line references and heading context.

Output: TheoryOfChange/00_Meta/AI_Summaries/AI_13_THEORY_ONLY.md

Synthetic label legend:
- [[DF* ...]] auto definition cue
- [[FT* ...]] auto foundational cue
- [[DR* ...]] auto derivation cue
- [[CR* ...]] auto corollary cue
- [[CF* ...]] auto counterfactual cue
- [[NT* ...]] auto theory note (fallback)
"""

FILE = Path("TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md")
OUT = Path("TheoryOfChange/00_Meta/AI_Summaries/AI_13_THEORY_ONLY.md")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")
LABEL_LINE_RE = re.compile(r"\[\[[ ]*(FT|DF|DR|CR|CF|CL|AS)[^\]]*\]\]")
TABLE_RE = re.compile(r"^\|.*\|\s*$")

# Cues to infer synthetic label type
CUE_FT = re.compile(r"(?i)foundational truth|undeniable|cannot deny|immediate datum|self-evident")
CUE_DF = re.compile(r"(?i)^\s*(we\s+define|definition|we\s+say|we\s+can\s+define|means\s+that)\b")
CUE_DR = re.compile(r"(?i)we\s+derive|therefore|thus it follows|we\s+conclude|we\s+can\s+show")
CUE_CR = re.compile(r"(?i)corollary|implies that|it implies|as a corollary")
CUE_CF = re.compile(r"(?i)counterfactual|if .* were not|if .* wasn['’]t")

# Theory relevance keywords
THEORY_TERMS = re.compile(
    r"(?i)\b(subject|awareness|experience|ontology|performative contradiction|g[oö]del|markov|frame shift|frame change|meta-operator|operator|state space|space/subject|recursion|drift|closure|derivation|definition|corollary|counterfactual|proof|axiom|assumption)\b"
)

def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())

def infer_synth_label(line: str) -> str:
    if CUE_DF.search(line):
        return "DF*"
    if CUE_FT.search(line):
        return "FT*"
    if CUE_DR.search(line):
        return "DR*"
    if CUE_CR.search(line):
        return "CR*"
    if CUE_CF.search(line):
        return "CF*"
    return "NT*"

def main():
    if not FILE.exists():
        print(f"Missing input: {FILE}")
        sys.exit(1)

    # Read all lines
    lines = FILE.read_text(encoding="utf-8", errors="replace").splitlines()

    # Track heading path for context
    heading_stack = []  # list of (level, title)

    # Concept sections: key -> data
    concepts = {}
    order = []

    def concept_key_from_context(text: str) -> str:
        # Choose a primary keyword if present
        keys = [
            ("performative contradiction", re.compile(r"(?i)performative contradiction")),
            ("subject/awareness/experience", re.compile(r"(?i)subject|awareness|experience")),
            ("godel holes", re.compile(r"(?i)g[oö]del")),
            ("markov/closure", re.compile(r"(?i)markov|closure|state space")),
            ("frame/operators", re.compile(r"(?i)frame (shift|change)|meta-operator|operator|space/subject")),
            ("recursion/drift", re.compile(r"(?i)recursion|drift")),
            ("assumptions/axioms", re.compile(r"(?i)assumption|axiom")),
            ("definitions", re.compile(r"(?i)definition|we define|we can define|we say")),
            ("derivations/corollaries", re.compile(r"(?i)derive|corollary|therefore|thus")),
            ("ontology of change", re.compile(r"(?i)ontology|change first|change ontology")),
        ]
        for name, rx in keys:
            if rx.search(text):
                return name
        # fallback to last heading title
        if heading_stack:
            return normalize_text(" > ".join(t for _, t in heading_stack[-2:]))
        return "general"

    def get_section(key: str):
        if key not in concepts:
            concepts[key] = {
                "first_line": 10**9,
                "headings": set(),
                "items": [],  # list of dicts with fields
                "label_set": set(),
            }
            order.append(key)
        return concepts[key]

    # Scan lines to gather theory segments
    i = 0
    while i < len(lines):
        raw = lines[i]
        ln = i + 1
        m = HEADING_RE.match(raw)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))
            i += 1
            continue

        has_label = bool(LABEL_LINE_RE.search(raw))
        is_table = bool(TABLE_RE.match(raw))
        theoryish = bool(THEORY_TERMS.search(raw))
        # Start segment on label or theoryish line (not purely empty)
        if (has_label or theoryish or is_table) and raw.strip():
            # Expand segment window: include up to 2 lines before and after while they are non-empty or continue table/list
            start = max(0, i - 2)
            # rewind to not cut through a paragraph/table
            while start > 0 and lines[start].strip() and not HEADING_RE.match(lines[start]):
                if start == 0:
                    break
                if not lines[start - 1].strip():
                    break
                start -= 1
            end = i
            # forward include
            end_ptr = min(len(lines) - 1, i + 6)
            while end < end_ptr:
                nxt = lines[end + 1]
                if HEADING_RE.match(nxt):
                    break
                if not nxt.strip():
                    # allow a single blank inside segment; then stop if next also blank
                    if end + 2 <= len(lines) - 1 and not lines[end + 2].strip():
                        break
                end += 1
            # Determine synthetic label if needed
            seg_text = "\n".join(lines[start:end+1])
            synth = None
            if not has_label:
                synth = infer_synth_label(seg_text)

            key = concept_key_from_context(seg_text)
            sec = get_section(key)
            sec["first_line"] = min(sec["first_line"], ln)
            if heading_stack:
                sec["headings"].add(" > ".join(t for _, t in heading_stack))

            # De-duplicate sentences within the segment
            content_norm_set = set()
            content_lines = []
            for k in range(start, end + 1):
                t = lines[k].rstrip()
                if not t.strip():
                    continue
                # skip pure chat markers like "##### [USER]" unless theory terms
                if HEADING_RE.match(t):
                    continue
                n = normalize_text(t).lower()
                if n in content_norm_set:
                    continue
                content_norm_set.add(n)
                content_lines.append((k + 1, t))

            labels_in_seg = LABEL_LINE_RE.findall(seg_text)
            label_tokens = re.findall(r"\[\[[^\]]+\]\]", seg_text)
            # Build item
            item = {
                "start": start + 1,
                "end": end + 1,
                "synth": synth,  # e.g., DF*, DR*, ... or None
                "labels": label_tokens,  # keep full tokens
                "content": content_lines,
            }
            # Merge enrichment: avoid exact duplicate content blocks
            # Use a fingerprint as normalized concatenation
            fp = "\n".join(n for _, n in content_lines)
            if fp:
                # only add if not present already
                existing_fps = getattr(sec, "_fps", None)
                if existing_fps is None:
                    sec["_fps"] = set()
                    existing_fps = sec["_fps"]
                if fp not in existing_fps:
                    existing_fps.add(fp)
                    sec["items"].append(item)
                    for tok in label_tokens:
                        sec["label_set"].add(tok)
            i = end + 1
            continue

        i += 1

    # Order concepts by first appearance
    ordered = sorted(order, key=lambda k: concepts[k]["first_line"])

    out = []
    out.append("# AI_13 Theory-Only (Merged, Deduplicated)")
    out.append("")
    out.append("Legend: synthetic labels marked with * (DF*, FT*, DR*, CR*, CF*, NT*)")
    out.append("")

    for key in ordered:
        sec = concepts[key]
        if not sec["items"]:
            continue
        out.append(f"## {key}")
        if sec["headings"]:
            out.append("Sources: ")
            for h in sorted(sec["headings"]):
                out.append(f"- {h}")
        if sec["label_set"]:
            out.append("Labels:")
            for tok in sorted(sec["label_set"]):
                out.append(f"- {tok}")
        out.append("")
        # Emit items
        for it in sec["items"]:
            # Label line
            if it["synth"]:
                out.append(f"[[{it['synth']}]] (L{it['start']}-L{it['end']})")
            else:
                out.append(f"(L{it['start']}-L{it['end']})")
            # Content lines
            for L, t in it["content"]:
                out.append(f"- L{L}: {t}")
            out.append("")

    OUT.write_text("\n".join(out).strip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()

