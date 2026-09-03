#!/usr/bin/env python3
"""Independently replay target 051's obligations and concrete witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_051


OBLIGATIONS = {
    target_051.PRIMARY: "obligation",
    target_051.EXACT_OUTPUT: "exact_output_obligation",
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
    lines = process.stdout.splitlines()
    if (
        process.returncode != 0
        or not lines
        or lines[0] != expected
        or process.stderr != ""
    ):
        raise ValueError(
            f"{path.name}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )


def validation_error(input_record: dict[str, Any]) -> str:
    length = input_record["length"]
    index0, index1 = input_record["indices"]
    if not 0 <= index0 < length:
        return "IndexOutOfBounds"
    if not 0 <= index1 < length:
        return "IndexOutOfBounds"
    if index0 == index1:
        return "OverlappingIndices"
    return "NoError"


def boundary_matches(
    input_record: dict[str, Any],
    boundary: dict[str, Any],
) -> bool:
    return all(
        boundary[key] == input_record[key]
        for key in (
            "length",
            "values",
            "allocation",
            "address",
            "provenance",
            "borrow",
            "element_size",
            "element_alignment",
            "allocation_base",
            "allocation_bytes",
            "isize_max",
            "address_space_limit",
            "frame_token",
        )
    )


def borrow_well_formed(
    input_record: dict[str, Any],
    borrow: dict[str, Any],
) -> bool:
    index = borrow["index"]
    return (
        0 <= index < input_record["length"]
        and borrow["allocation"] == input_record["allocation"]
        and borrow["address"]
        == input_record["address"] + index * input_record["element_size"]
        and borrow["provenance"] == input_record["provenance"]
        and borrow["parent_borrow"] == input_record["borrow"]
        and borrow["value"] == input_record["values"][index]
    )


def borrow_array_well_formed(
    input_record: dict[str, Any],
    result: dict[str, Any],
) -> bool:
    borrows = result.get("borrows", [])
    return (
        result.get("tag") == "Ok"
        and len(borrows) == 2
        and all(borrow_well_formed(input_record, borrow) for borrow in borrows)
        and borrows[0]["index"] != borrows[1]["index"]
    )


def final_state_holds(
    input_record: dict[str, Any],
    state: dict[str, Any],
    *,
    is_ok: bool,
) -> bool:
    preserved = all(
        state[key] == input_record[key]
        for key in (
            "length",
            "allocation",
            "address",
            "provenance",
            "borrow",
            "element_size",
            "element_alignment",
            "frame_token",
        )
    )
    return preserved and (is_ok or state["values"] == input_record["values"])


def contract_holds(
    input_record: dict[str, Any],
    boundary: dict[str, Any],
    execution: dict[str, Any],
) -> bool:
    if not boundary_matches(input_record, boundary):
        return False
    result = execution["result"]
    state = execution["final_state"]
    error = validation_error(input_record)
    if result["tag"] == "Ok":
        return (
            error == "NoError"
            and borrow_array_well_formed(input_record, result)
            and final_state_holds(input_record, state, is_ok=True)
        )
    if result["tag"] != "Err" or result.get("error") not in {
        "IndexOutOfBounds",
        "OverlappingIndices",
    }:
        return False
    return (
        error != "NoError"
        and final_state_holds(input_record, state, is_ok=False)
    )


def canonical_borrow_indices(input_record: dict[str, Any]) -> list[int]:
    return list(input_record["indices"])


def replay_error_witness(case: dict[str, Any]) -> dict[str, Any]:
    input_record = case["input"]
    boundary = case["boundary"]
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    observed = {
        "shared_boundary": boundary_matches(input_record, boundary),
        "validation_error": validation_error(input_record),
        "execution1_satisfies_contract": contract_holds(
            input_record, boundary, execution1
        ),
        "execution2_satisfies_contract": contract_holds(
            input_record, boundary, execution2
        ),
        "exact_output_equal": execution1["result"] == execution2["result"],
        "exact_final_state_equal": (
            execution1["final_state"] == execution2["final_state"]
        ),
        "exact_equivalent": execution1 == execution2,
    }
    if observed != case["expected"]:
        raise ValueError(f"error witness replay mismatch: {observed!r}")
    return observed


def replay_borrow_witness(case: dict[str, Any]) -> dict[str, Any]:
    input_record = case["input"]
    boundary = case["boundary"]
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    canonical = canonical_borrow_indices(input_record)
    observed = {
        "shared_boundary": boundary_matches(input_record, boundary),
        "validation_error": validation_error(input_record),
        "execution1_borrows_well_formed_and_disjoint": (
            borrow_array_well_formed(input_record, execution1["result"])
        ),
        "execution2_borrows_well_formed_and_disjoint": (
            borrow_array_well_formed(input_record, execution2["result"])
        ),
        "execution1_is_canonical_implementation_result": (
            [item["index"] for item in execution1["result"]["borrows"]]
            == canonical
        ),
        "execution2_is_canonical_implementation_result": (
            [item["index"] for item in execution2["result"]["borrows"]]
            == canonical
        ),
        "execution1_satisfies_contract": contract_holds(
            input_record, boundary, execution1
        ),
        "execution2_satisfies_contract": contract_holds(
            input_record, boundary, execution2
        ),
        "exact_output_equal": execution1["result"] == execution2["result"],
        "exact_final_state_equal": (
            execution1["final_state"] == execution2["final_state"]
        ),
        "exact_equivalent": execution1 == execution2,
    }
    if observed != case["expected"]:
        raise ValueError(f"borrow witness replay mismatch: {observed!r}")
    return observed


def replay(evidence_root: Path, z3: str) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{purpose}: retained obligation is missing")
        text = smt_path.read_text()
        metadata = json.loads(metadata_path.read_text())
        target_051.validate_target_obligation(text, metadata)
        _run_z3(smt_path, z3, "sat")
        obligations[purpose] = {
            "solver_result": "sat",
            "smt_sha256": sha256(smt_path),
            "metadata_sha256": sha256(metadata_path),
        }

    fixed_witnesses: dict[str, Any] = {}
    for name in target_051.WITNESS_CASES:
        path = evidence_root / "witnesses" / f"{name}.smt2"
        if not path.is_file():
            raise ValueError(f"{name}: fixed witness is missing")
        if path.read_text() != target_051.fixed_witness_text(name):
            raise ValueError(f"{name}: fixed witness differs from reviewed text")
        _run_z3(path, z3, "sat")
        fixed_witnesses[name] = {
            "solver_result": "sat",
            "smt_sha256": sha256(path),
        }

    probes: dict[str, Any] = {}
    for name, case in target_051.PROBE_CASES.items():
        path = evidence_root / "probes" / f"{name}.smt2"
        if not path.is_file():
            raise ValueError(f"{name}: rejection probe is missing")
        if path.read_text() != target_051.probe_text(name):
            raise ValueError(f"{name}: rejection probe differs from reviewed text")
        expected = target_051.PROBE_EXPECTED_RESULTS[name]
        _run_z3(path, z3, expected)
        probes[name] = {
            "solver_result": expected,
            "smt_sha256": sha256(path),
            "kind": case["kind"],
        }

    witness_path = evidence_root / "witness.json"
    raw = witness_path.read_bytes()
    witness = json.loads(raw)
    if witness != target_051.witness_payload():
        raise ValueError("target-051 witness payload differs from reviewed values")

    return {
        "status": "passed",
        "target": target_051.TARGET,
        "input_order": target_051.INPUT_ORDER,
        "active_contract_sha256": target_051.ACTIVE_CONTRACT_SHA256,
        "obligations": obligations,
        "fixed_witnesses": fixed_witnesses,
        "rejection_probes": probes,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "out_of_bounds_error_variants": replay_error_witness(
            witness["out_of_bounds_error_variants"]
        ),
        "valid_disjoint_distinct_borrows": replay_borrow_witness(
            witness["valid_disjoint_distinct_borrows"]
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.evidence_root, args.z3), sort_keys=True))


if __name__ == "__main__":
    main()
