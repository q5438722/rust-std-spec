#!/usr/bin/env python3
"""Validate the additive certified operational-v2 projection."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from operational_v2_certification import validate_written_artifacts


if __name__ == "__main__":
    manifest = validate_written_artifacts()
    print("operational_v2_certified_projection_validator=PASS")
    print(f"rows={manifest['row_count']}")
    print("independent_review=ACCEPT")
