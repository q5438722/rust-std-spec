#!/usr/bin/env python3
"""Independently replay retained SliceIndex trio evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import slice_index_trio as trio


OBLIGATIONS = {
    trio.PRIMARY: "obligation",
    trio.EXACT_OUTPUT: "exact_output_obligation",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(
    z3: str,
    path: Path,
    expected: str,
    *,
    require_payload: bool = False,
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
        or (not require_payload and process.stdout != expected + "\n")
        or (
            require_payload
            and (
                len(lines) < 2
                or "(NormalizedStart x)" not in process.stdout
                or "(y_address y1)" not in process.stdout
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
        "stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
        "model_retained": require_payload,
    }


def _requires_holds(input_record: dict[str, Any]) -> bool:
    values = [input_record[f"value{index}"] for index in range(3)]
    length = input_record["length"]
    byte_length = length * input_record["element_size"]
    return (
        values == [10, 20, 30]
        and length == 3
        and input_record["index_form"] == "usize"
        and input_record["index_tag"] == 0
        and input_record["a"] == 0
        and input_record["allocation"] > 0
        and input_record["address"] > 0
        and input_record["provenance"] > 0
        and input_record["root_borrow"] > 0
        and input_record["single_allocation"] is True
        and input_record["element_size"] >= 0
        and input_record["element_alignment"] > 0
        and input_record["address"] % input_record["element_alignment"] == 0
        and (
            input_record["element_size"] == 0
            or (
                input_record["element_size"]
                >= input_record["element_alignment"]
                and input_record["element_size"]
                % input_record["element_alignment"]
                == 0
            )
        )
        and input_record["allocation_base"] <= input_record["address"]
        and input_record["address"] + byte_length
        <= input_record["allocation_base"] + input_record["allocation_bytes"]
        and byte_length <= input_record["isize_max"]
        and input_record["address"] + byte_length
        <= input_record["address_space_limit"]
        and input_record["alias_readers"] == 0
        and input_record["alias_writers"] == 0
        and input_record["frame_token"] > 0
    )


def _boundary_matches(
    input_record: dict[str, Any], boundary: dict[str, Any]
) -> bool:
    return all(
        boundary[key] == input_record[key]
        for key in (
            "value0",
            "value1",
            "value2",
            "allocation",
            "address",
            "provenance",
            "root_borrow",
            "single_allocation",
            "allocation_base",
            "allocation_bytes",
            "element_size",
            "element_alignment",
            "usize_max",
            "isize_max",
            "address_space_limit",
            "alias_readers",
            "alias_writers",
            "frame_token",
        )
    )


def _reference_well_formed(
    input_record: dict[str, Any], result: dict[str, Any]
) -> bool:
    index = result["index"]
    expected_address = input_record["address"] + (
        0
        if input_record["element_size"] == 0
        else index * input_record["element_size"]
    )
    return (
        result["kind"] == "element"
        and 0 <= index < input_record["length"]
        and result["length"] == 1
        and result["allocation"] == input_record["allocation"]
        and result["address"] == expected_address
        and result["provenance"] == input_record["provenance"]
        and result["parent_borrow"] == input_record["root_borrow"]
        and result["value"] == input_record[f"value{index}"]
    )


def _mutable_frame(
    input_record: dict[str, Any], state: dict[str, Any]
) -> bool:
    return (
        state["length"] == input_record["length"]
        and state["values"][1:]
        == [input_record["value1"], input_record["value2"]]
        and state["allocation"] == input_record["allocation"]
        and state["address"] == input_record["address"]
        and state["provenance"] == input_record["provenance"]
        and state["root_borrow"] == input_record["root_borrow"]
        and state["element_size"] == input_record["element_size"]
        and state["element_alignment"] == input_record["element_alignment"]
        and state["alias_readers"] == input_record["alias_readers"]
        and state["alias_writers"] == input_record["alias_writers"]
        and state["frame_token"] == input_record["frame_token"]
    )


def _contract_holds(
    config: trio.SliceIndexTarget,
    input_record: dict[str, Any],
    boundary: dict[str, Any],
    execution: dict[str, Any],
) -> bool:
    result = execution["result"]
    present = result.get("present")
    return (
        _requires_holds(input_record)
        and _boundary_matches(input_record, boundary)
        and (present is True if config.option_return else present is None)
        and _reference_well_formed(input_record, result)
        and _mutable_frame(input_record, execution["final_state"])
    )


def replay_witness(
    config: trio.SliceIndexTarget, payload: dict[str, Any]
) -> dict[str, Any]:
    input_record = payload["input"]
    boundary = payload["boundary"]
    execution1 = payload["execution1"]
    execution2 = payload["execution2"]
    source = payload["source_result"]
    observed = {
        "requires_holds": _requires_holds(input_record),
        "shared_boundary": _boundary_matches(input_record, boundary),
        "source_result_is_execution1": source == execution1["result"],
        "source_result_is_execution2": source == execution2["result"],
        "execution1_reference_well_formed": _reference_well_formed(
            input_record, execution1["result"]
        ),
        "execution2_reference_well_formed": _reference_well_formed(
            input_record, execution2["result"]
        ),
        "execution1_satisfies_active_contract": _contract_holds(
            config, input_record, boundary, execution1
        ),
        "execution2_satisfies_active_contract": _contract_holds(
            config, input_record, boundary, execution2
        ),
        "exact_output_equal": execution1["result"] == execution2["result"],
        "exact_final_state_equal": (
            execution1["final_state"] == execution2["final_state"]
        ),
        "full_exact_equivalent": execution1 == execution2,
    }
    if observed != payload["expected"]:
        raise ValueError(f"{config.target}: witness replay mismatch: {observed!r}")
    return observed


def replay(
    evidence_root: Path,
    z3: str,
    config: trio.SliceIndexTarget,
) -> dict[str, Any]:
    obligations: dict[str, Any] = {}
    for purpose, stem in OBLIGATIONS.items():
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            raise ValueError(f"{config.target} {purpose}: evidence is missing")
        metadata = json.loads(metadata_path.read_text())
        trio.validate_target_obligation(config, smt_path.read_text(), metadata)
        obligations[purpose] = {
            **_run(z3, smt_path, config.expected_results[purpose]),
            "metadata_sha256": _sha256(metadata_path),
        }

    source_instances: dict[str, Any] = {}
    for name in trio.source_cases(config):
        path = evidence_root / "source_instances" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != trio.source_instance_text(config, name)
        ):
            raise ValueError(f"{config.target} {name}: source instance changed")
        source_instances[name] = _run(
            z3, path, "sat", require_payload=True
        )

    negative_probes: dict[str, Any] = {}
    for name in trio.negative_probe_names(config):
        path = evidence_root / "negative_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != trio.negative_probe_text(config, name)
        ):
            raise ValueError(f"{config.target} {name}: negative probe changed")
        negative_probes[name] = _run(z3, path, "unsat")

    witness_result: dict[str, Any] | None = None
    if config.mutable:
        smt_path = evidence_root / "fixed_reference_witness.smt2"
        payload_path = evidence_root / "fixed_reference_witness.json"
        if (
            not smt_path.is_file()
            or smt_path.read_text() != trio.fixed_witness_text(config)
            or not payload_path.is_file()
        ):
            raise ValueError(f"{config.target}: fixed witness is missing or stale")
        payload = json.loads(payload_path.read_text())
        if payload != trio.witness_payload(config):
            raise ValueError(f"{config.target}: fixed witness payload changed")
        witness_result = {
            **_run(z3, smt_path, "sat", require_payload=True),
            "payload_sha256": _sha256(payload_path),
            "observed": replay_witness(config, payload),
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
        "fixed_reference_witness": witness_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    parser.add_argument(
        "--artifact-id",
        required=True,
        choices=tuple(trio.TARGET_BY_ARTIFACT),
    )
    args = parser.parse_args()
    config = trio.TARGET_BY_ARTIFACT[args.artifact_id]
    print(json.dumps(replay(args.evidence_root, args.z3, config), sort_keys=True))


if __name__ == "__main__":
    main()
