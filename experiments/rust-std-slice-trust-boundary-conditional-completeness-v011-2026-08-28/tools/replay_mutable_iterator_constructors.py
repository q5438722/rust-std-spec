#!/usr/bin/env python3
"""Independently replay retained mutable-iterator constructor evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutable_iterator_constructors as constructors


OBLIGATIONS = {
    constructors.PRIMARY: "obligation",
    constructors.EXACT_OUTPUT: "exact_output_obligation",
}
SOURCE_INSTANCES = {
    "empty_non_zst": (0, 8),
    "nonempty_non_zst": (5, 8),
    "nonempty_zst": (5, 0),
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
        or process.stderr != ""
    ):
        raise ValueError(
            f"{path.name}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )
    return {
        "solver_result": expected,
        "smt_sha256": _sha256(path),
    }


def replay(
    evidence_root: Path,
    z3: str,
    config: constructors.ConstructorTarget,
) -> dict[str, Any]:
    observed_obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{config.target} {purpose}: evidence is missing")
        metadata = json.loads(metadata_path.read_text())
        constructors.validate_target_obligation(
            config, smt_path.read_text(), metadata
        )
        observed_obligations[purpose] = {
            **_run(z3, smt_path, "unsat"),
            "metadata_sha256": _sha256(metadata_path),
        }

    observed_instances: dict[str, Any] = {}
    for name, (length, element_size) in SOURCE_INSTANCES.items():
        path = evidence_root / f"source_instance_{name}.smt2"
        expected_text = constructors.source_instance_text(
            config,
            length=length,
            element_size=element_size,
        )
        if not path.is_file() or path.read_text() != expected_text:
            raise ValueError(
                f"{config.target} {name}: source instance changed"
            )
        observed_instances[name] = _run(z3, path, "sat")

    return {
        "schema_version": 1,
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "obligations": observed_obligations,
        "source_instances": observed_instances,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    parser.add_argument(
        "--artifact-id",
        required=True,
        choices=tuple(constructors.TARGET_BY_ARTIFACT),
    )
    args = parser.parse_args()
    config = constructors.TARGET_BY_ARTIFACT[args.artifact_id]
    print(json.dumps(replay(args.evidence_root, args.z3, config), sort_keys=True))


if __name__ == "__main__":
    main()
