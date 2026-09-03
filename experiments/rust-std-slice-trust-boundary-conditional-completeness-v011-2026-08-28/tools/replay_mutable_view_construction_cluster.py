#!/usr/bin/env python3
"""Independently replay retained mutable-view construction evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutable_view_construction_cluster as cluster


OBLIGATIONS = {
    cluster.PRIMARY: "obligation",
    cluster.EXACT_OUTPUT: "exact_output_obligation",
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
            "(s_return_final s1)",
            "(s_return_final s2)",
            "(s_input_final s1)",
            "(s_input_final s2)",
            "(Equivalent_T x b y1 s1 y2 s2)",
            "false",
        )
        if witness
        else ("(y_length y1)", "(s_input_final s1)")
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
                or any(
                    marker not in process.stdout for marker in markers
                )
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
    config: cluster.MutableViewTarget,
) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{config.target} {purpose}: evidence is missing")
        metadata = json.loads(metadata_path.read_text())
        cluster.validate_target_obligation(
            config,
            smt_path.read_text(),
            metadata,
        )
        obligations[purpose] = {
            **_run(
                z3,
                smt_path,
                config.expected_solver_results[purpose],
            ),
            "metadata_sha256": _sha256(metadata_path),
        }

    witness_smt = evidence_root / "fixed_full_state_witness.smt2"
    witness_json = evidence_root / "fixed_full_state_witness.json"
    if (
        not witness_smt.is_file()
        or witness_smt.read_text()
        != cluster.fixed_full_state_witness_text(config)
        or not witness_json.is_file()
        or json.loads(witness_json.read_text())
        != cluster.witness_payload(config)
    ):
        raise ValueError(f"{config.target}: fixed full-state witness changed")
    witness = {
        **_run(
            z3,
            witness_smt,
            "sat",
            require_model=True,
            witness=True,
        ),
        "payload_sha256": _sha256(witness_json),
    }

    source_instances: dict[str, Any] = {}
    for name in cluster.source_cases(config):
        path = evidence_root / "source_instances" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != cluster.source_instance_text(config, name)
        ):
            raise ValueError(f"{config.target} {name}: source instance changed")
        source_instances[name] = _run(
            z3,
            path,
            "sat",
            require_model=True,
        )

    negative_probes: dict[str, Any] = {}
    for name in cluster.negative_probe_names(config):
        path = evidence_root / "negative_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != cluster.negative_probe_text(config, name)
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
        "fixed_full_state_witness": witness,
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
        choices=tuple(cluster.TARGET_BY_ARTIFACT),
    )
    args = parser.parse_args()
    config = cluster.TARGET_BY_ARTIFACT[args.artifact_id]
    print(json.dumps(replay(args.evidence_root, args.z3, config), sort_keys=True))


if __name__ == "__main__":
    main()
