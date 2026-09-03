#!/usr/bin/env python3
"""Run the fail-closed operational-v2 campaign reconciliation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from operational_v2_reconciliation import main


if __name__ == "__main__":
    main()
