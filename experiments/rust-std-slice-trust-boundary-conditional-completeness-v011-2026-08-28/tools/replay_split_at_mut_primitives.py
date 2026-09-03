#!/usr/bin/env python3
"""Independently replay retained mutable split evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import split_at_mut_primitives as split


OBLIGATIONS = {
    split.PRIMARY: "obligation",
    split.EXACT_OUTPUT: "exact_output_obligation",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(
    z3: str,
    path: Path,
    expected: str,
    *,
    require_model: bool = False,
) -> dict[str, Any]:
    process = subprocess.run(
        [z3, "-smt2", str(path)],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    lines = process.stdout.splitlines()
    if (
        process.returncode != 0
        or process.stderr
        or not lines
        or lines[0] != expected
        or (not require_model and process.stdout != expected + "\n")
        or (
            require_model
            and (
                len(lines) < 2
                or "(x_mid x)" not in process.stdout
                or "(y_split_index y1)" not in process.stdout
            )
        )
    ):
        raise ValueError(
            f"{path.name}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )
    return {
        "solver_result": expected,
        "smt_sha256": _sha256(path),
        "stdout_sha256": hashlib.sha256(
            process.stdout.encode()
        ).hexdigest(),
        "model_retained": require_model,
    }


def replay(
    evidence_root: Path,
    z3: str,
    config: split.SplitTarget,
) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{config.target} {purpose}: evidence is missing")
        metadata = json.loads(metadata_path.read_text())
        split.validate_target_obligation(
            config,
            smt_path.read_text(),
            metadata,
        )
        obligations[purpose] = {
            **_run(z3, smt_path, "unsat"),
            "metadata_sha256": _sha256(metadata_path),
        }

    source_instances: dict[str, Any] = {}
    for name, case in split.source_cases(config).items():
        path = evidence_root / f"source_instance_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != split.source_instance_text(config, case)
        ):
            raise ValueError(f"{config.target} {name}: source instance changed")
        source_instances[name] = _run(
            z3,
            path,
            "sat",
            require_model=True,
        )

    negative_probes: dict[str, Any] = {}
    for name in split.negative_probe_names(config):
        path = evidence_root / f"negative_probe_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != split.negative_probe_text(config, name)
        ):
            raise ValueError(f"{config.target} {name}: negative probe changed")
        negative_probes[name] = _run(z3, path, "unsat")

    return {
        "schema_version": 1,
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "obligations": obligations,
        "source_instances": source_instances,
        "negative_probes": negative_probes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    parser.add_argument(
        "--artifact-id",
        required=True,
        choices=tuple(split.TARGET_BY_ARTIFACT),
    )
    args = parser.parse_args()
    config = split.TARGET_BY_ARTIFACT[args.artifact_id]
    print(json.dumps(replay(args.evidence_root, args.z3, config), sort_keys=True))


if __name__ == "__main__":
    main()
