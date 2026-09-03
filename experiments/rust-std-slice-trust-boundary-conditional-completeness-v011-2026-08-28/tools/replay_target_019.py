#!/usr/bin/env python3
"""Independently replay target 019 evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pointer_target_replay
import target_019


def replay(evidence_root: Path, z3: str) -> dict:
    return pointer_target_replay.replay(target_019, evidence_root, z3)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.evidence_root, args.z3), sort_keys=True))


if __name__ == "__main__":
    main()
