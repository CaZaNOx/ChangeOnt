"""
Direct-axis placement validation scaffold.

This study no longer predicts bucket labels. It records:
- primitive profile
- environment axes
- direct kernel controls implied by those axes
- observed metrics under an optional explicit study override

The active target is to compare direct control movement under lawful deformations,
not to classify into historical posture buckets.
"""
from __future__ import annotations

import json
from pathlib import Path

from agents.co.placement.legacy.profile_examples import summarized_examples


def main() -> None:
    out = summarized_examples()
    path = Path('canonical_placement_examples_v2.json')
    path.write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
    print(f'wrote {path}')


if __name__ == '__main__':
    main()
