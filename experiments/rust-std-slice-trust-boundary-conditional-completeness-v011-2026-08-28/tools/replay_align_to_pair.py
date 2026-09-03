#!/usr/bin/env python3
"""Replay retained align_to pair solver evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import align_to_pair as align


OBLIGATIONS = {
    align.PRIMARY: "obligation",
    align.EXACT_OUTPUT: "exact_output_obligation",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(
    z3: str,
    path: Path,
    expected: str,
    *,
    require_model: bool = False,
    witness: bool = False,
) -> dict[str, Any]:
    process = subprocess.run(
        [z3, "-smt2", str(path)],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    lines = process.stdout.splitlines()
    markers = (
        (
            "(s_final_bytes s1)",
            "(s_final_bytes s2)",
            "(s_final_middle s1)",
            "(s_final_middle s2)",
            "(Equivalent_T x b y1 s1 y2 s2)",
            "false",
        )
        if witness
        else (
            "(y_branch y1)",
            "(y_middle_values y1)",
            "(s_final_source s1)",
        )
    )
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
                or any(marker not in process.stdout for marker in markers)
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
    config: align.AlignTarget,
) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{config.target} {purpose}: evidence missing")
        metadata = json.loads(metadata_path.read_text())
        align.validate_target_obligation(
            config, smt_path.read_text(), metadata
        )
        obligations[purpose] = {
            **_run(
                z3,
                smt_path,
                config.expected_solver_results[purpose],
            ),
            "metadata_sha256": _sha256(metadata_path),
        }

    source_instances: dict[str, Any] = {}
    for name in align.source_cases(config):
        path = evidence_root / "source_instances" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != align.source_instance_text(config, name)
        ):
            raise ValueError(f"{config.target} {name}: source case changed")
        source_instances[name] = _run(
            z3, path, "sat", require_model=True
        )

    negative_probes: dict[str, Any] = {}
    for name in align.negative_probe_names(config):
        path = evidence_root / "negative_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != align.negative_probe_text(config, name)
        ):
            raise ValueError(f"{config.target} {name}: probe changed")
        negative_probes[name] = _run(z3, path, "unsat")

    fixed_witness: dict[str, Any] | None = None
    if config.mutable:
        smt_path = evidence_root / "fixed_full_state_witness.smt2"
        payload_path = evidence_root / "fixed_full_state_witness.json"
        if (
            not smt_path.is_file()
            or smt_path.read_text()
            != align.fixed_full_state_witness_text(config)
            or not payload_path.is_file()
            or json.loads(payload_path.read_text())
            != align.witness_payload(config)
        ):
            raise ValueError(f"{config.target}: fixed witness changed")
        fixed_witness = {
            **_run(
                z3,
                smt_path,
                "sat",
                require_model=True,
                witness=True,
            ),
            "payload_sha256": _sha256(payload_path),
        }

    return {
        "schema_version": 1,
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "obligations": obligations,
        "source_instances": source_instances,
        "negative_probes": negative_probes,
        "fixed_full_state_witness": fixed_witness,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    parser.add_argument(
        "--artifact-id",
        required=True,
        choices=tuple(align.TARGET_BY_ARTIFACT),
    )
    args = parser.parse_args()
    config = align.TARGET_BY_ARTIFACT[args.artifact_id]
    print(
        json.dumps(
            replay(args.evidence_root, args.z3, config),
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
