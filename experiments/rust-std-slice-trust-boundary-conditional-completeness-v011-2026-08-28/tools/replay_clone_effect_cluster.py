#!/usr/bin/env python3
"""Independently replay retained targets 037/043 solver evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clone_effect_cluster as cluster


OBLIGATIONS = {
    cluster.PRIMARY: "obligation",
    cluster.EXACT_OUTPUT: "exact_output_obligation",
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
    lines = process.stdout.splitlines()
    observed = lines[0] if lines else ""
    if process.returncode != 0 or observed != expected or process.stderr:
        raise ValueError(
            f"{path}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )
    if expected == "sat" and len(lines) < 2:
        raise ValueError(f"{path}: SAT replay did not retain a model")
    return {
        "solver_result": observed,
        "smt_sha256": _sha256(path),
        "model_retained": expected != "sat" or len(lines) >= 2,
    }


def _require_text(path: Path, expected: str) -> None:
    if not path.is_file() or path.read_text() != expected:
        raise ValueError(f"retained SMT input changed: {path}")


def replay(
    evidence_root: Path,
    z3: str,
    config: cluster.CloneEffectTarget,
) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not metadata_path.is_file():
            raise ValueError(f"{config.target} {purpose}: metadata is missing")
        metadata = json.loads(metadata_path.read_text())
        expected_text, expected_metadata = cluster.obligation(config, purpose)
        _require_text(smt, expected_text)
        if metadata != expected_metadata:
            raise ValueError(f"{config.target} {purpose}: metadata changed")
        cluster.validate_target_obligation(config, smt.read_text(), metadata)
        obligations[purpose] = {
            **_run(z3, smt, "unsat"),
            "metadata_sha256": _sha256(metadata_path),
        }

    panic_path = evidence_root / "panic_prefix_obligation.smt2"
    _require_text(panic_path, cluster.panic_obligation_text(config))
    cluster.validate_panic_obligation(config, panic_path.read_text())
    panic_obligation = _run(z3, panic_path, "unsat")

    mismatch_obligation: dict[str, Any] | None = None
    if not config.is_fill:
        path = evidence_root / "length_mismatch_obligation.smt2"
        _require_text(path, cluster.mismatch_obligation_text(config))
        cluster.validate_mismatch_obligation(config, path.read_text())
        mismatch_obligation = _run(z3, path, "unsat")

    source_instances: dict[str, Any] = {}
    for case in cluster.SOURCE_CASES[config.artifact_id]:
        path = evidence_root / "source_instances" / f"{case.name}.smt2"
        _require_text(path, cluster.source_instance_text(config, case))
        source_instances[case.name] = _run(z3, path, "sat")

    negative_probes: dict[str, Any] = {}
    for name in cluster.negative_probe_names(config):
        path = evidence_root / "negative_probes" / f"{name}.smt2"
        _require_text(path, cluster.negative_probe_text(config, name))
        negative_probes[name] = _run(z3, path, "unsat")

    panic_probes: dict[str, Any] = {}
    for index in range(3):
        name = f"panic_at_{index}"
        path = evidence_root / "panic_probes" / f"{name}.smt2"
        _require_text(path, cluster.panic_probe_text(config, index))
        panic_probes[name] = _run(z3, path, "sat")

    mismatch_probes: dict[str, Any] = {}
    if not config.is_fill:
        for trivial in (False, True):
            name = "trivial" if trivial else "default"
            path = evidence_root / "mismatch_probes" / f"{name}.smt2"
            _require_text(
                path,
                cluster.mismatch_probe_text(config, trivial=trivial),
            )
            mismatch_probes[name] = _run(z3, path, "sat")

    return {
        "schema_version": 1,
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "obligations": obligations,
        "panic_prefix_obligation": panic_obligation,
        "length_mismatch_obligation": mismatch_obligation,
        "source_instances": source_instances,
        "negative_probes": negative_probes,
        "panic_probes": panic_probes,
        "mismatch_probes": mismatch_probes,
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
    result = replay(
        args.evidence_root,
        args.z3,
        cluster.TARGET_BY_ARTIFACT[args.artifact_id],
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
