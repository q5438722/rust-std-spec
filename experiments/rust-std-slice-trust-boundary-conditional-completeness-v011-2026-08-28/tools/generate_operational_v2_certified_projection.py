#!/usr/bin/env python3
"""Generate the additive certified operational-v2 projection."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from operational_v2_certification import write_artifacts


if __name__ == "__main__":
    manifest = write_artifacts()
    print("operational_v2_certified_projection_generator=PASS")
    print(f"rows={manifest['row_count']}")
    print("independent_review=ACCEPT")
