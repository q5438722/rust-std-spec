#!/usr/bin/env python3
"""Replay target 065's fixed-boundary witnesses."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import search_family
import search_family_replay


def replay(path: Path) -> dict:
    return search_family_replay.replay(search_family.TARGET_065, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
