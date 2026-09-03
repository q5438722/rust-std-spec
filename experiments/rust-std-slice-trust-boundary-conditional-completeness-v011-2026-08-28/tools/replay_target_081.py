#!/usr/bin/env python3
"""Independently replay target 081's bounded sort witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import permutations, product
from pathlib import Path
from typing import Any


TARGET = "core::slice::sort_unstable_by"
INPUT_ORDER = "81"
ACTIVE_CONTRACT_SHA256 = (
    "420e250d3b0ae471b64eb3d6474588eaec8acfc7644b5c1dd4420e4c1b2c0597"
)
ORDERINGS = ("Less", "Equal", "Greater")
ORDERING_RANK = {"Less": -1, "Equal": 0, "Greater": 1}
ORDERING_DUAL = {"Less": "Greater", "Equal": "Equal", "Greater": "Less"}


def comparator_map(case: dict[str, Any]) -> dict[tuple[int, int], str]:
    identities = case["boundary"]["input_identities"]
    table = case["boundary"]["comparator_results"]
    if (
        len(identities) != 3
        or len(table) != 3
        or any(len(row) != 3 for row in table)
        or any(value not in ORDERINGS for row in table for value in row)
    ):
        raise ValueError("comparator boundary is not a complete finite 3-by-3 table")
    return {
        (left, right): table[left_index][right_index]
        for left_index, left in enumerate(identities)
        for right_index, right in enumerate(identities)
    }


def sorted_by_comparator(
    output: list[int],
    comparator: dict[tuple[int, int], str],
) -> bool:
    return all(
        ORDERING_RANK[comparator[(output[left], output[right])]] <= 0
        for left in range(3)
        for right in range(left, 3)
    )


def is_total_order(
    identities: list[int],
    comparator: dict[tuple[int, int], str],
) -> bool:
    if any(comparator[(value, value)] != "Equal" for value in identities):
        return False
    for left in identities:
        for right in identities:
            if comparator[(right, left)] != ORDERING_DUAL[
                comparator[(left, right)]
            ]:
                return False
    return all(
        not (
            ORDERING_RANK[comparator[(left, middle)]] <= 0
            and ORDERING_RANK[comparator[(middle, right)]] <= 0
        )
        or ORDERING_RANK[comparator[(left, right)]] <= 0
        for left in identities
        for middle in identities
        for right in identities
    )


def contract_holds(case: dict[str, Any], execution: dict[str, Any]) -> bool:
    input_record = case["input"]
    boundary = case["boundary"]
    identities = input_record["identities"]
    final_slice = execution["final_slice"]
    comparator = comparator_map(case)
    return (
        len(identities) == 3
        and len(set(identities)) == 3
        and boundary["input_identities"] == identities
        and boundary["callback_state_delta"] == 0
        and execution["return_unit"] is True
        and len(final_slice) == 3
        and Counter(final_slice) == Counter(identities)
        and sorted_by_comparator(final_slice, comparator)
        and execution["callback_final_state"]
        == input_record["callback_initial_state"]
        + boundary["callback_state_delta"]
    )


def reviewed_equivalent(
    case: dict[str, Any],
    execution1: dict[str, Any],
    execution2: dict[str, Any],
) -> bool:
    comparator = comparator_map(case)
    left = execution1["final_slice"]
    right = execution2["final_slice"]
    return (
        execution1["return_unit"] == execution2["return_unit"]
        and execution1["callback_final_state"]
        == execution2["callback_final_state"]
        and Counter(left) == Counter(right)
        and all(
            comparator[(left[index], right[index])] == "Equal"
            and comparator[(right[index], left[index])] == "Equal"
            for index in range(3)
        )
    )


def replay_case(case: dict[str, Any]) -> dict[str, Any]:
    comparator = comparator_map(case)
    identities = case["input"]["identities"]
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    observed = {
        "boundary_is_total_order": is_total_order(identities, comparator),
        "execution1_satisfies_active_contract": contract_holds(case, execution1),
        "execution2_satisfies_active_contract": contract_holds(case, execution2),
        "execution1_preserves_exact_multiplicities": (
            Counter(execution1["final_slice"]) == Counter(identities)
        ),
        "execution2_preserves_exact_multiplicities": (
            Counter(execution2["final_slice"]) == Counter(identities)
        ),
        "callback_final_state_equal": (
            execution1["callback_final_state"]
            == execution2["callback_final_state"]
        ),
        "reviewed_equal_key_equivalent": reviewed_equivalent(
            case, execution1, execution2
        ),
        "exact_final_slice_equal": (
            execution1["final_slice"] == execution2["final_slice"]
        ),
    }
    if observed != case["expected"]:
        raise ValueError(f"counterexample replay mismatch: {observed!r}")
    return observed


def replay_total_order_sanity() -> dict[str, Any]:
    identities = [10, 11, 20]
    output_sequences = list(permutations(identities))
    off_diagonal = [
        (left, right)
        for left in identities
        for right in identities
        if left != right
    ]
    profiles_checked = 0
    result_pairs_checked = 0
    for values in product(ORDERINGS, repeat=len(off_diagonal)):
        comparator = {
            (identity, identity): "Equal" for identity in identities
        }
        comparator.update(dict(zip(off_diagonal, values)))
        if not is_total_order(identities, comparator):
            continue
        profiles_checked += 1
        sorted_outputs = [
            list(output)
            for output in output_sequences
            if sorted_by_comparator(list(output), comparator)
        ]
        for left in sorted_outputs:
            for right in sorted_outputs:
                result_pairs_checked += 1
                if Counter(left) != Counter(right) or not all(
                    comparator[(left[index], right[index])] == "Equal"
                    and comparator[(right[index], left[index])] == "Equal"
                    for index in range(3)
                ):
                    raise ValueError(
                        "total-order replay found inequivalent sorted permutations: "
                        f"{comparator!r}, {left!r}, {right!r}"
                    )
    if profiles_checked == 0 or result_pairs_checked == 0:
        raise ValueError("total-order replay did not exercise any valid profile")
    return {
        "profiles_checked": profiles_checked,
        "valid_result_pairs_checked": result_pairs_checked,
        "all_pairs_equal_key_equivalent": True,
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
    return {
        "status": "passed",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "exact_final_slice_counterexample": replay_case(
            witness["exact_final_slice_counterexample"]
        ),
        "general_non_total_counterexample": replay_case(
            witness["general_non_total_counterexample"]
        ),
        "total_order_sanity": replay_total_order_sanity(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
