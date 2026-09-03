#!/usr/bin/env python3
"""Generate the additive operational-v2 parser-repair certification."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from operational_v2_parser_repair_certification_v1 import main


if __name__ == "__main__":
    main()
