#!/usr/bin/env python3
"""Independently replay target 106's retained UNSAT obligations."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_106


OBLIGATIONS = {
    target_106.PRIMARY: "obligation",
    target_106.EXACT_OUTPUT: "exact_output_obligation",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(evidence_root: Path, z3: str) -> dict[str, Any]:
    observed: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{purpose}: retained obligation is missing")
        metadata = json.loads(metadata_path.read_text())
        text = smt_path.read_text()
        target_106.validate_target_obligation(text, metadata)
        process = subprocess.run(
            [z3, "-smt2", str(smt_path)],
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        if (
            process.returncode != 0
            or process.stdout != "unsat\n"
            or process.stderr != ""
        ):
            raise ValueError(
                f"{purpose}: expected clean unsat replay, got "
                f"rc={process.returncode}, stdout={process.stdout!r}, "
                f"stderr={process.stderr!r}"
            )
        observed[purpose] = {
            "solver_result": "unsat",
            "smt_sha256": sha256(smt_path),
            "metadata_sha256": sha256(metadata_path),
        }
    return {
        "status": "passed",
        "target": target_106.TARGET,
        "input_order": target_106.INPUT_ORDER,
        "active_contract_sha256": target_106.ACTIVE_CONTRACT_SHA256,
        "obligations": observed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.evidence_root, args.z3), sort_keys=True))


if __name__ == "__main__":
    main()
