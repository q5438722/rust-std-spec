#!/usr/bin/env python3
"""Independently replay target 013's fixed-boundary final-state witness."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


TARGET = "core::slice::as_chunks_mut"
INPUT_ORDER = "13"
ACTIVE_CONTRACT_SHA256 = (
    "669f8bbc7a27aa64da763386dccd397f1d7e81db22ef7b672e71a40b69ff5e7c"
)


def flatten(chunks: list[list[int]]) -> list[int]:
    return [value for chunk in chunks for value in chunk]


def source_output(
    values: list[int], chunk_size: int, allocation: int, borrow: int
) -> dict[str, Any]:
    rounded = len(values) // chunk_size * chunk_size
    return {
        "chunks_reference": {
            "allocation": allocation,
            "parent_borrow": borrow,
            "start": 0,
            "span": rounded,
            "element_width": chunk_size,
            "projection_kind": "array-chunks",
        },
        "remainder_reference": {
            "allocation": allocation,
            "parent_borrow": borrow,
            "start": rounded,
            "span": len(values) - rounded,
            "element_width": 1,
            "projection_kind": "slice-remainder",
        },
        "chunks": [
            values[index : index + chunk_size]
            for index in range(0, rounded, chunk_size)
        ],
        "remainder": values[rounded:],
    }


def active_conjuncts(
    values: list[int],
    chunk_size: int,
    output: dict[str, Any],
    final: dict[str, Any],
) -> dict[str, bool]:
    chunks = output["chunks"]
    remainder = output["remainder"]
    final_chunks = final["chunks"]
    final_remainder = final["remainder"]
    final_slice = final["slice"]
    rounded = len(chunks) * chunk_size
    return {
        "partition": (
            chunk_size != 0
            and len(remainder) < chunk_size
            and flatten(chunks) + remainder == values
        ),
        "initial_chunks_length": len(chunks) == len(values) // chunk_size,
        "initial_remainder_length": len(remainder) == len(values) % chunk_size,
        "initial_chunk_subranges": all(
            chunk
            == values[index * chunk_size : (index + 1) * chunk_size]
            for index, chunk in enumerate(chunks)
        ),
        "initial_remainder_subrange": remainder == values[rounded:],
        "final_chunks_length": len(final_chunks) == len(chunks),
        "final_remainder_length": len(final_remainder) == len(remainder),
        "final_frame": final_slice == flatten(final_chunks) + final_remainder,
        "final_chunk_subranges": all(
            chunk
            == final_slice[index * chunk_size : (index + 1) * chunk_size]
            for index, chunk in enumerate(final_chunks)
        ),
        "final_remainder_subrange": (
            final_remainder == final_slice[len(final_chunks) * chunk_size :]
        ),
    }


def replay(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    witness = json.loads(raw)
    if (
        witness.get("target") != TARGET
        or witness.get("input_order") != INPUT_ORDER
        or witness.get("active_contract_sha256") != ACTIVE_CONTRACT_SHA256
    ):
        raise ValueError("witness identity or active contract hash mismatch")

    input_record = witness["input"]
    boundary = witness["boundary"]
    values = input_record["slice"]
    chunk_size = input_record["chunk_size"]
    if chunk_size == 0:
        raise ValueError("witness violates the active N != 0 requirement")
    if (
        input_record["allocation"] != boundary["input_allocation"]
        or input_record["borrow"] != boundary["input_borrow"]
    ):
        raise ValueError("witness boundary does not observe the input identity")
    expected_output = source_output(
        values,
        chunk_size,
        boundary["input_allocation"],
        boundary["input_borrow"],
    )
    executions = [witness["execution1"], witness["execution2"]]
    checks = [
        active_conjuncts(values, chunk_size, execution["output"], execution["final"])
        for execution in executions
    ]
    output_equal = executions[0]["output"] == executions[1]["output"]
    final_equal = executions[0]["final"] == executions[1]["final"]
    observed = {
        "same_boundary": True,
        "execution1_satisfies_all_active_conjuncts": (
            executions[0]["output"] == expected_output and all(checks[0].values())
        ),
        "execution2_satisfies_all_active_conjuncts": (
            executions[1]["output"] == expected_output and all(checks[1].values())
        ),
        "exact_output_equal": output_equal,
        "exact_final_state_equal": final_equal,
        "full_exact_equivalent": output_equal and final_equal,
    }
    if observed != witness["expected"]:
        raise ValueError(f"target-013 witness replay mismatch: {observed!r}")
    return {
        "status": "passed",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "active_conjuncts": {
            "execution1": checks[0],
            "execution2": checks[1],
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
