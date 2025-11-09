#!/usr/bin/env python3
import re
from pathlib import Path

MASTER = Path('TheoryOfChange_main/00_Meta/Context/AI_Leads_Master.md')

def main():
    text = MASTER.read_text(encoding='utf-8')
    out = []
    pruned = 0
    lead_re = re.compile(r"^- \[ \] L\d+ \| [^|]+ \| (covered|likely-covered)\b")
    for line in text.splitlines():
        if lead_re.match(line):
            pruned += 1
            continue
        out.append(line)
    MASTER.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'Pruned {pruned} checked leads (covered/likely-covered).')

if __name__ == '__main__':
    main()

