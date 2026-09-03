#!/usr/bin/env python3
"""Independent replay support for source-backed pointer target evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Any


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_z3(path: Path, z3: str, expected: str) -> str:
    process = subprocess.run(
        [z3, "-smt2", str(path)],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    lines = process.stdout.splitlines()
    actual = lines[0] if lines else ""
    if (
        process.returncode != 0
        or actual != expected
        or process.stderr != ""
        or (expected == "sat" and len(lines) < 2)
        or (expected == "unsat" and process.stdout != "unsat\n")
    ):
        raise ValueError(
            f"{path.name}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )
    return process.stdout


def replay(module: ModuleType, evidence_root: Path, z3: str) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in (
        (module.PRIMARY, "obligation"),
        (module.EXACT_OUTPUT, "exact_output_obligation"),
    ):
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{module.INPUT_ORDER} {purpose}: obligation is missing")
        metadata = json.loads(metadata_path.read_text())
        text = smt_path.read_text()
        module.validate_target_obligation(text, metadata)
        _run_z3(smt_path, z3, "unsat")
        obligations[purpose] = {
            "solver_result": "unsat",
            "smt_sha256": sha256(smt_path),
            "metadata_sha256": sha256(metadata_path),
        }

    probes: dict[str, Any] = {}
    for name, case in module.PROBE_CASES.items():
        path = evidence_root / "probes" / f"{name}.smt2"
        if not path.is_file():
            raise ValueError(f"{module.INPUT_ORDER} {name}: probe is missing")
        if path.read_text() != module.probe_text(name):
            raise ValueError(
                f"{module.INPUT_ORDER} {name}: probe differs from reviewed text"
            )
        expected = module.PROBE_EXPECTED_RESULTS[name]
        stdout = _run_z3(path, z3, expected)
        probes[name] = {
            "kind": case["kind"],
            "solver_result": expected,
            "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
            "smt_sha256": sha256(path),
            "case": case["values"],
        }

    return {
        "status": "passed",
        "target": module.TARGET,
        "input_order": module.INPUT_ORDER,
        "active_contract_sha256": module.ACTIVE_CONTRACT_SHA256,
        "obligations": obligations,
        "satisfiability_and_rejection_probes": probes,
    }
