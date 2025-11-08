#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path('TheoryOfChange_main')

# Terms that often signal drift if not tied to CO constructs
RULES = [
    {
        'name': 'probability-language',
        'pattern': re.compile(r'\b(probabilit[y|ies]|probabilistic|probable|likelihood)\b', re.I),
        'suggest': 'Use SRL/Evaluation Surface framing: [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]], [[01_Statements/Definition/S-DF-evaluation-surface]], or add [[01_Statements/Clarification/S-CL-probabilistic-language-srl]].'
    },
    {
        'name': 'time-language',
        'pattern': re.compile(r'\b(time|temporal flow|time flow|timeless)\b', re.I),
        'suggest': 'Use Breath/RTV/σ(ε) phenomenology: [[01_Statements/Corollary/S-CR-perceived-time-breath-index]]. Avoid physical time claims unless bridged.'
    },
    {
        'name': 'consciousness-overclaim',
        'pattern': re.compile(r'\b(conscious(ness)?|sentien(t|ce))\b', re.I),
        'suggest': 'Scope via Cᴸ/proto-conscious locks: [[01_Statements/Definition/S-DF-consciousness-loop]], [[01_Statements/Clarification/S-CL-proto-conscious-min-criteria]].'
    },
    {
        'name': 'recursion-first',
        'pattern': re.compile(r'\brecursion (as|is) (first|primary|found(ation|ational))\b', re.I),
        'suggest': 'Clarify change is foundational: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]], [[01_Statements/Clarification/S-CL-change-vs-recursion-foundation]].'
    },
    {
        'name': 'eternal-recurrence',
        'pattern': re.compile(r'\beternal (recurrence|return)\b', re.I),
        'suggest': 'If spiral mentioned, add: [[01_Statements/Clarification/S-CL-spiral-vs-eternal-recurrence]].'
    },
    {
        'name': 'attention-spotlight',
        'pattern': re.compile(r'\battention\b', re.I),
        'suggest': 'Ensure attention is framed as recursive prioritization: [[01_Statements/Clarification/S-CL-attention-recursive-filter]].'
    },
    {
        'name': 'emotion-qualia',
        'pattern': re.compile(r'\bemotion(s)?\b', re.I),
        'suggest': 'Constrain to recursive valuation unless phenomenology is bridged: [[01_Statements/Clarification/S-CL-emotion-recursive-valuation]].'
    },
]

EXCLUDE_DIRS = {
    ROOT / '05_Speculations' / 'ORIGINALS',
    ROOT / '01_Statements' / 'SYMBOLS',
}

def should_skip(p: Path) -> bool:
    for d in EXCLUDE_DIRS:
        try:
            p.relative_to(d)
            return True
        except ValueError:
            continue
    return False

def main():
    issues = []
    for p in ROOT.rglob('*.md'):
        if should_skip(p) or p.name == 'README.md':
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        # skip frontmatter for simple matching context; scan whole file
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            l = line.strip()
            if not l:
                continue
            for rule in RULES:
                if rule['pattern'].search(l):
                    # If the line already contains a clarifying link, skip
                    suggest = rule['suggest']
                    # detect any [[...]] link to a clarification we suggest
                    if '[[01_Statements/Clarification/' in l or '[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]' in l or '[[01_Statements/Definition/S-DF-evaluation-surface]]' in l or '[[01_Statements/Definition/S-DF-consciousness-loop]]' in l:
                        continue
                    issues.append({
                        'file': str(p),
                        'line': i,
                        'name': rule['name'],
                        'text': l[:200],
                        'suggest': suggest,
                    })
    if not issues:
        print('lint: no drift-prone terms found (outside allowed scopes).')
        return
    print('lint: potential drift-prone usages:')
    for it in issues:
        print(f"- {it['file']}:{it['line']} [{it['name']}] {it['text']}\n  -> {it['suggest']}")

if __name__ == '__main__':
    main()
