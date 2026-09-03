#!/usr/bin/env python3
"""Independently replay target 052's obligations and concrete witness."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_052


OBLIGATIONS = {
    target_052.PRIMARY: "obligation",
    target_052.EXACT_OUTPUT: "exact_output_obligation",
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


def requires_holds(input_record: dict[str, Any]) -> bool:
    length = input_record["length"]
    index0, index1 = input_record["indices"]
    byte_length = length * input_record["element_size"]
    return (
        length == 3
        and [index0, index1] == [0, 2]
        and 0 <= index0 < length
        and 0 <= index1 < length
        and index0 != index1
        and input_record["allocation"] > 0
        and input_record["address"] > 0
        and input_record["provenance"] > 0
        and input_record["borrow"] > 0
        and input_record["element_size"] > 0
        and input_record["element_alignment"] > 0
        and input_record["address"] % input_record["element_alignment"] == 0
        and input_record["element_size"] % input_record["element_alignment"] == 0
        and input_record["allocation_base"] >= 0
        and input_record["allocation_bytes"] > 0
        and input_record["allocation_base"] <= input_record["address"]
        and input_record["address"] + byte_length
        <= input_record["allocation_base"] + input_record["allocation_bytes"]
        and byte_length <= input_record["isize_max"]
        and input_record["address"] + byte_length
        <= input_record["address_space_limit"]
    )


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
        len(borrows) == 2
        and all(borrow_well_formed(input_record, borrow) for borrow in borrows)
        and borrows[0]["index"] != borrows[1]["index"]
    )


def source_transition_holds(
    input_record: dict[str, Any],
    transition: dict[str, Any],
) -> bool:
    index0, index1 = input_record["indices"]
    first = transition["after_first_write"]
    second = transition["after_second_write"]
    return (
        transition["cloned_indices"] == [index0, index1]
        and first
        == {
            "initialized": [True, False],
            "slot0_index": index0,
        }
        and second
        == {
            "initialized": [True, True],
            "slot0_index": first["slot0_index"],
            "slot1_index": index1,
        }
        and transition["assume_init_after_first_write"] is False
        and transition["assume_init_after_second_write"] is True
        and transition["canonical_borrow_indices"] == [index0, index1]
    )


def contract_holds(
    input_record: dict[str, Any],
    boundary: dict[str, Any],
    execution: dict[str, Any],
) -> bool:
    return (
        requires_holds(input_record)
        and boundary_matches(input_record, boundary)
        and borrow_array_well_formed(input_record, execution["result"])
        and execution["final_state"]["length"] == input_record["length"]
    )


def replay_witness(case: dict[str, Any]) -> dict[str, Any]:
    input_record = case["input"]
    boundary = case["boundary"]
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    canonical = case["source_transition"]["canonical_borrow_indices"]
    observed = {
        "requires_holds": requires_holds(input_record),
        "shared_boundary": boundary_matches(input_record, boundary),
        "source_transition_is_complete": source_transition_holds(
            input_record, case["source_transition"]
        ),
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
        raise ValueError(f"target-052 witness replay mismatch: {observed!r}")
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
        target_052.validate_target_obligation(text, metadata)
        _run_z3(smt_path, z3, "sat")
        obligations[purpose] = {
            "solver_result": "sat",
            "smt_sha256": sha256(smt_path),
            "metadata_sha256": sha256(metadata_path),
        }

    fixed_witnesses: dict[str, Any] = {}
    for name in target_052.WITNESS_CASES:
        path = evidence_root / "witnesses" / f"{name}.smt2"
        if not path.is_file():
            raise ValueError(f"{name}: fixed witness is missing")
        if path.read_text() != target_052.fixed_witness_text(name):
            raise ValueError(f"{name}: fixed witness differs from reviewed text")
        _run_z3(path, z3, "sat")
        fixed_witnesses[name] = {
            "solver_result": "sat",
            "smt_sha256": sha256(path),
        }

    probes: dict[str, Any] = {}
    for name, case in target_052.PROBE_CASES.items():
        path = evidence_root / "probes" / f"{name}.smt2"
        if not path.is_file():
            raise ValueError(f"{name}: rejection probe is missing")
        if path.read_text() != target_052.probe_text(name):
            raise ValueError(f"{name}: rejection probe differs from reviewed text")
        expected = target_052.PROBE_EXPECTED_RESULTS[name]
        _run_z3(path, z3, expected)
        probes[name] = {
            "solver_result": expected,
            "smt_sha256": sha256(path),
            "kind": case["kind"],
        }

    witness_path = evidence_root / "witness.json"
    raw = witness_path.read_bytes()
    witness = json.loads(raw)
    if witness != target_052.witness_payload():
        raise ValueError("target-052 witness payload differs from reviewed values")
    witness_result = replay_witness(
        witness["valid_disjoint_distinct_borrows"]
    )

    return {
        "status": "passed",
        "target": target_052.TARGET,
        "input_order": target_052.INPUT_ORDER,
        "active_contract_sha256": target_052.ACTIVE_CONTRACT_SHA256,
        "obligations": obligations,
        "fixed_witnesses": fixed_witnesses,
        "rejection_probes": probes,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "valid_disjoint_distinct_borrows": witness_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.evidence_root, args.z3), sort_keys=True))


if __name__ == "__main__":
    main()
