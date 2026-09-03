#!/usr/bin/env python3
"""Independently replay target 022's UNSAT obligations and SAT domain probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_022


OBLIGATIONS = {
    target_022.PRIMARY: "obligation",
    target_022.EXACT_OUTPUT: "exact_output_obligation",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_z3(path: Path, z3: str, expected: str) -> None:
    process = subprocess.run(
        [z3, "-smt2", str(path)],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    if (
        process.returncode != 0
        or process.stdout != f"{expected}\n"
        or process.stderr != ""
    ):
        raise ValueError(
            f"{path.name}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )


def replay(evidence_root: Path, z3: str) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{purpose}: retained obligation is missing")
        metadata = json.loads(metadata_path.read_text())
        text = smt_path.read_text()
        target_022.validate_target_obligation(text, metadata)
        _run_z3(smt_path, z3, "unsat")
        obligations[purpose] = {
            "solver_result": "unsat",
            "smt_sha256": sha256(smt_path),
            "metadata_sha256": sha256(metadata_path),
        }

    probes: dict[str, Any] = {}
    for name in target_022.PROBE_CASES:
        path = evidence_root / "probes" / f"{name}.smt2"
        if not path.is_file():
            raise ValueError(f"{name}: retained satisfiability probe is missing")
        if path.read_text() != target_022.probe_text(name):
            raise ValueError(f"{name}: satisfiability probe differs from reviewed text")
        expected = target_022.PROBE_EXPECTED_RESULTS[name]
        _run_z3(path, z3, expected)
        probes[name] = {
            "solver_result": expected,
            "smt_sha256": sha256(path),
            "case": target_022.PROBE_CASES[name],
        }

    return {
        "status": "passed",
        "target": target_022.TARGET,
        "input_order": target_022.INPUT_ORDER,
        "active_contract_sha256": target_022.ACTIVE_CONTRACT_SHA256,
        "obligations": obligations,
        "satisfiability_probes": probes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.evidence_root, args.z3), sort_keys=True))


if __name__ == "__main__":
    main()
