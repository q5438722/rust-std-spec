#!/usr/bin/env python3
"""Run the operational-v2 certification closure."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from operational_v2_certification import main


if __name__ == "__main__":
    main()
