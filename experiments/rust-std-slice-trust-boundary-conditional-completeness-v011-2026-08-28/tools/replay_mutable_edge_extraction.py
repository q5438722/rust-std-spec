#!/usr/bin/env python3
"""Independently replay retained mutable-edge solver evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutable_edge_extraction as edge


OBLIGATIONS = {
    edge.PRIMARY: "obligation",
    edge.EXACT_OUTPUT: "exact_output_obligation",
}
SOURCE_INSTANCES = {
    "empty_non_zst": (0, 8),
    "empty_zst": (0, 0),
    "singleton_non_zst": (1, 8),
    "singleton_zst": (1, 0),
    "longer_non_zst": (5, 8),
    "longer_zst": (5, 0),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(z3: str, path: Path, expected: str) -> dict[str, Any]:
    process = subprocess.run(
        [z3, "-smt2", str(path)],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    if (
        process.returncode != 0
        or process.stdout != expected + "\n"
        or process.stderr
    ):
        raise ValueError(
            f"{path.name}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )
    return {"solver_result": expected, "smt_sha256": _sha256(path)}


def replay(
    evidence_root: Path,
    z3: str,
    config: edge.EdgeTarget,
) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt.is_file() or not metadata_path.is_file():
            raise ValueError(f"{config.target} {purpose}: evidence is missing")
        metadata = json.loads(metadata_path.read_text())
        edge.validate_target_obligation(config, smt.read_text(), metadata)
        obligations[purpose] = {
            **_run(z3, smt, "unsat"),
            "metadata_sha256": _sha256(metadata_path),
        }

    instances: dict[str, Any] = {}
    for name, (length, element_size) in SOURCE_INSTANCES.items():
        path = evidence_root / f"source_instance_{name}.smt2"
        expected = edge.source_instance_text(
            config,
            length=length,
            element_size=element_size,
        )
        if not path.is_file() or path.read_text() != expected:
            raise ValueError(f"{config.target} {name}: source instance changed")
        instances[name] = _run(z3, path, "sat")

    return {
        "schema_version": 1,
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "obligations": obligations,
        "source_instances": instances,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    parser.add_argument(
        "--artifact-id",
        required=True,
        choices=tuple(edge.TARGET_BY_ARTIFACT),
    )
    args = parser.parse_args()
    result = replay(
        args.evidence_root,
        args.z3,
        edge.TARGET_BY_ARTIFACT[args.artifact_id],
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
