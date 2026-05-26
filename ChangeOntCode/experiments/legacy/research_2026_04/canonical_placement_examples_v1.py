from __future__ import annotations

import json
from pathlib import Path

from agents.co.placement.legacy.profile_examples import summarized_examples


def main() -> None:
    out = summarized_examples()
    out_path = Path("canonical_placement_examples_v1.json")
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(out_path)


if __name__ == "__main__":
    main()
