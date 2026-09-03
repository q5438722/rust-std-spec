#!/usr/bin/env python3
"""Run the fail-closed final Slice campaign reconciliation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from final_reconciliation import main


if __name__ == "__main__":
    main()
