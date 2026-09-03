#!/usr/bin/env python3
"""Independently replay concrete fixed-boundary witnesses for mutable chunks."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chunk_contract_drift_cluster as cluster


def flatten(chunks: list[list[int]]) -> list[int]:
    return [value for chunk in chunks for value in chunk]


def expected_reference(
    input_record: dict[str, Any],
    *,
    start: int,
    span: int,
    width: int,
    projection_kind: str,
) -> dict[str, Any]:
    return {
        "allocation": input_record["allocation"],
        "address": (
            input_record["address"] + start * input_record["element_size"]
        ),
        "provenance": input_record["provenance"],
        "parent_borrow": input_record["borrow_identity"],
        "start": start,
        "span": span,
        "element_width": width,
        "projection_kind": projection_kind,
    }


def memory_domain_valid(input_record: dict[str, Any]) -> bool:
    length = input_record["length"]
    n = input_record["chunk_size"]
    size = input_record["element_size"]
    alignment = input_record["element_alignment"]
    byte_span = length * size
    return (
        length >= 0
        and n > 0
        and input_record["address"] > 0
        and alignment > 0
        and input_record["address"] % alignment == 0
        and (
            size == 0
            or (size >= alignment and size % alignment == 0)
        )
        and n * size <= input_record["isize_max"]
        and byte_span <= input_record["isize_max"]
        and input_record["address"] + byte_span
        <= input_record["address_space_limit"]
        and input_record["one_allocation"]
        and input_record["initialized"]
        and input_record["writable"]
        and input_record["exclusive_access"]
        and (
            byte_span == 0
            or (
                input_record["allocation"] > 0
                and input_record["provenance"] > 0
                and input_record["allocation_base"]
                <= input_record["address"]
                and input_record["address"] + byte_span
                <= input_record["allocation_base"]
                + input_record["allocation_bytes"]
                <= input_record["address_space_limit"]
            )
        )
        and input_record["borrow_identity"] > 0
        and input_record["frame_token"] > 0
    )


def source_output(
    config: cluster.ChunkTarget,
    input_record: dict[str, Any],
) -> dict[str, Any]:
    values = input_record["slice"]
    n = input_record["chunk_size"]
    chunk_count = len(values) // n
    remainder_count = len(values) % n
    chunk_start = remainder_count if config.reverse else 0
    chunk_span = chunk_count * n
    chunk_values = values[chunk_start : chunk_start + chunk_span]
    output: dict[str, Any] = {
        "chunks_reference": expected_reference(
            input_record,
            start=chunk_start,
            span=chunk_span,
            width=n,
            projection_kind="array-chunks",
        ),
        "chunks": [
            chunk_values[index : index + n]
            for index in range(0, chunk_span, n)
        ],
    }
    if config.has_remainder:
        remainder_start = 0 if config.reverse else chunk_span
        remainder_values = (
            values[:remainder_count]
            if config.reverse
            else values[remainder_start:]
        )
        output.update(
            {
                "remainder_reference": expected_reference(
                    input_record,
                    start=remainder_start,
                    span=remainder_count,
                    width=1,
                    projection_kind="slice-remainder",
                ),
                "remainder": remainder_values,
            }
        )
    return output


def active_conjuncts(
    config: cluster.ChunkTarget,
    input_record: dict[str, Any],
    output: dict[str, Any],
    final: dict[str, Any],
) -> dict[str, bool]:
    values = input_record["slice"]
    n = input_record["chunk_size"]
    chunks = output["chunks"]
    chunk_count = len(values) // n
    remainder_count = len(values) % n
    chunk_start = remainder_count if config.reverse else 0
    chunk_span = chunk_count * n
    checks: dict[str, bool] = {}
    if config.kind == "unchecked":
        checks["ActiveFlattenConjunct"] = flatten(chunks) == values
    else:
        remainder = output["remainder"]
        reconstructed = (
            remainder + flatten(chunks)
            if config.reverse
            else flatten(chunks) + remainder
        )
        checks["ActivePartitionConjunct"] = (
            len(remainder) < n and reconstructed == values
        )
    checks["ActiveChunksLengthConjunct"] = len(chunks) == chunk_count
    if config.has_remainder:
        checks["ActiveRemainderLengthConjunct"] = (
            len(output["remainder"]) == remainder_count
        )
    checks["ActiveInitialChunkSubrangesConjunct"] = all(
        chunk
        == values[
            chunk_start + index * n : chunk_start + (index + 1) * n
        ]
        for index, chunk in enumerate(chunks)
    )
    if config.has_remainder:
        expected_remainder = (
            values[:remainder_count]
            if config.reverse
            else values[chunk_span:]
        )
        checks["ActiveInitialRemainderSubrangeConjunct"] = (
            output["remainder"] == expected_remainder
        )

    final_slice = final["slice"]
    final_chunks = final["chunks"]
    checks["ActiveFinalChunksLengthConjunct"] = (
        len(final_chunks) == len(chunks)
    )
    if config.has_remainder:
        final_remainder = final["remainder"]
        checks["ActiveFinalRemainderLengthConjunct"] = (
            len(final_remainder) == len(output["remainder"])
        )
        reconstructed_final = (
            final_remainder + flatten(final_chunks)
            if config.reverse
            else flatten(final_chunks) + final_remainder
        )
    else:
        final_remainder = []
        reconstructed_final = flatten(final_chunks)
    checks["ActiveFinalFrameConjunct"] = reconstructed_final == final_slice
    checks["ActiveFinalChunkSubrangesConjunct"] = all(
        chunk
        == final_slice[
            chunk_start + index * n : chunk_start + (index + 1) * n
        ]
        for index, chunk in enumerate(final_chunks)
    )
    if config.has_remainder:
        expected_final_remainder = (
            final_slice[:remainder_count]
            if config.reverse
            else final_slice[chunk_span:]
        )
        checks["ActiveFinalRemainderSubrangeConjunct"] = (
            final_remainder == expected_final_remainder
        )
    return checks


def replay(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    witness = json.loads(raw)
    input_order = str(witness.get("input_order", ""))
    if input_order not in cluster.TARGET_BY_ORDER:
        raise ValueError("witness has an unsupported input order")
    config = cluster.TARGET_BY_ORDER[input_order]
    if (
        not config.mutable
        or witness.get("target") != config.target
        or witness.get("active_contract_sha256")
        != config.active_contract_sha256
    ):
        raise ValueError("witness identity or active contract hash mismatch")

    input_record = dict(witness["input"])
    input_record["length"] = len(input_record["slice"])
    if not memory_domain_valid(input_record):
        raise ValueError("witness input violates the source memory domain")
    if (
        config.kind == "unchecked"
        and input_record["length"] % input_record["chunk_size"] != 0
    ):
        raise ValueError("unchecked witness violates exact divisibility")

    boundary = witness["boundary"]
    expected_boundary = {
        key: input_record[key]
        for key in (
            "allocation",
            "address",
            "provenance",
            "element_size",
            "element_alignment",
            "allocation_base",
            "allocation_bytes",
            "one_allocation",
            "initialized",
            "isize_max",
            "address_space_limit",
            "borrow_identity",
            "writable",
            "exclusive_access",
            "frame_token",
        )
    }
    expected_boundary["input_allocation"] = expected_boundary.pop("allocation")
    expected_boundary["input_address"] = expected_boundary.pop("address")
    expected_boundary["input_provenance"] = expected_boundary.pop("provenance")
    if boundary != expected_boundary:
        raise ValueError("witness boundary differs from the fixed input observation")

    expected_output = source_output(config, input_record)
    executions = [witness["execution1"], witness["execution2"]]
    checks = [
        active_conjuncts(
            config,
            input_record,
            execution["output"],
            execution["final"],
        )
        for execution in executions
    ]
    output_equal = executions[0]["output"] == executions[1]["output"]
    final_equal = executions[0]["final"] == executions[1]["final"]
    observed = {
        "same_input": True,
        "same_boundary": True,
        "execution1_satisfies_all_active_conjuncts": (
            executions[0]["output"] == expected_output
            and all(checks[0].values())
        ),
        "execution2_satisfies_all_active_conjuncts": (
            executions[1]["output"] == expected_output
            and all(checks[1].values())
        ),
        "exact_output_equal": output_equal,
        "exact_final_state_equal": final_equal,
        "full_exact_equivalent": output_equal and final_equal,
    }
    if observed != witness["expected"]:
        raise ValueError(f"fixed-boundary replay mismatch: {observed!r}")
    expected_names = set(cluster._active_conjunct_symbols(config))
    if any(set(result) != expected_names for result in checks):
        raise ValueError("replay did not evaluate every active contract conjunct")
    return {
        "schema_version": 1,
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "active_conjuncts": {
            "execution1": checks[0],
            "execution2": checks[1],
        },
        "source_transition_checks": {
            "pointer_cast_preserves_address_and_provenance": True,
            "array_pointer_cast_preserves_address_and_provenance": True,
            "raw_slice_uses_one_initialized_shared_storage": True,
            "returned_mutable_view_aliases_input_storage": True,
            "final_view_projects_the_same_final_slice": True,
        },
        "observed": observed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
