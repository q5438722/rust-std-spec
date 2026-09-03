#!/usr/bin/env python3
"""Independently replay target 029's concrete and exhaustive witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path
from typing import Any


TARGET = "core::slice::binary_search_by"
INPUT_ORDER = "29"
ACTIVE_CONTRACT_SHA256 = (
    "bbea7d2146da8d9116c68e9603460103ed4f7322c785180266a17b23b06c0f6b"
)
ORDERING_RANK = {"Less": -1, "Equal": 0, "Greater": 1}


def is_ordered(profile: list[str]) -> bool:
    return all(
        ORDERING_RANK[left] <= ORDERING_RANK[right]
        for left, right in zip(profile, profile[1:])
    )


def contract_holds(length: int, profile: list[str], result: dict[str, Any]) -> bool:
    tag = result["tag"]
    index = result["index"]
    if tag == "Ok":
        in_bounds = 0 <= index < length
    elif tag == "Err":
        in_bounds = 0 <= index <= length
    else:
        return False
    if not in_bounds or not is_ordered(profile):
        return in_bounds
    if tag == "Ok":
        return profile[index] == "Equal"
    return (
        all(ordering == "Less" for ordering in profile[:index])
        and all(ordering == "Greater" for ordering in profile[index:])
    )


def matching_index_equivalent(
    profile: list[str],
    execution1: dict[str, Any],
    execution2: dict[str, Any],
) -> bool:
    if execution1["callback_final_state"] != execution2["callback_final_state"]:
        return False
    result1 = execution1["result"]
    result2 = execution2["result"]
    if result1["tag"] != result2["tag"]:
        return False
    if result1["tag"] == "Err":
        return result1["index"] == result2["index"]
    return (
        profile[result1["index"]] == "Equal"
        and profile[result2["index"]] == "Equal"
    )


def all_results(length: int) -> list[dict[str, Any]]:
    return [
        *({"tag": "Ok", "index": index} for index in range(length)),
        *({"tag": "Err", "index": index} for index in range(length + 1)),
    ]


def replay_general(witness: dict[str, Any]) -> dict[str, Any]:
    case = witness["general_counterexample"]
    input_record = case["input"]
    boundary = case["boundary"]
    profile = boundary["comparator_results"]
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    final_state = (
        input_record["callback_initial_state"]
        + sum(boundary["callback_state_deltas"])
    )
    observed = {
        "ordered": is_ordered(profile),
        "execution1_satisfies_contract": (
            boundary["element_reads"] == input_record["elements"]
            and execution1["callback_final_state"] == final_state
            and contract_holds(
                input_record["length"], profile, execution1["result"]
            )
        ),
        "execution2_satisfies_contract": (
            boundary["element_reads"] == input_record["elements"]
            and execution2["callback_final_state"] == final_state
            and contract_holds(
                input_record["length"], profile, execution2["result"]
            )
        ),
        "equivalent": matching_index_equivalent(
            profile, execution1, execution2
        ),
    }
    if observed != case["expected"]:
        raise ValueError(
            f"general counterexample replay mismatch: {observed!r}"
        )
    return observed


def replay_sorted_domain() -> dict[str, Any]:
    profiles_checked = 0
    result_pairs_checked = 0
    results = all_results(2)
    for raw_profile in product(ORDERING_RANK, repeat=2):
        profile = list(raw_profile)
        if not is_ordered(profile):
            continue
        profiles_checked += 1
        valid = [
            result
            for result in results
            if contract_holds(2, profile, result)
        ]
        for result1 in valid:
            for result2 in valid:
                result_pairs_checked += 1
                execution1 = {
                    "result": result1,
                    "callback_final_state": 7,
                }
                execution2 = {
                    "result": result2,
                    "callback_final_state": 7,
                }
                if not matching_index_equivalent(
                    profile, execution1, execution2
                ):
                    raise ValueError(
                        "sorted-domain replay found inequivalent valid results: "
                        f"{profile!r}, {result1!r}, {result2!r}"
                    )
    if profiles_checked != 6:
        raise ValueError(
            f"sorted-domain replay checked {profiles_checked} profiles, expected 6"
        )
    return {
        "profiles_checked": profiles_checked,
        "valid_result_pairs_checked": result_pairs_checked,
        "all_pairs_equivalent": True,
    }


def replay_exact_output(witness: dict[str, Any]) -> dict[str, Any]:
    case = witness["exact_output_counterexample"]
    input_record = case["input"]
    boundary = case["boundary"]
    profile = boundary["comparator_results"]
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    observed = {
        "ordered": is_ordered(profile),
        "execution1_satisfies_contract": contract_holds(
            input_record["length"], profile, execution1["result"]
        ),
        "execution2_satisfies_contract": contract_holds(
            input_record["length"], profile, execution2["result"]
        ),
        "matching_index_equivalent": matching_index_equivalent(
            profile, execution1, execution2
        ),
        "exactly_equal": execution1 == execution2,
    }
    if (
        boundary["element_reads"] != input_record["elements"]
        or execution1["callback_final_state"]
        != input_record["callback_initial_state"]
        + sum(boundary["callback_state_deltas"])
        or execution2["callback_final_state"]
        != input_record["callback_initial_state"]
        + sum(boundary["callback_state_deltas"])
    ):
        raise ValueError("exact-output witness violates its fixed boundary")
    if observed != case["expected"]:
        raise ValueError(f"exact-output replay mismatch: {observed!r}")
    return observed


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
        "general_counterexample": replay_general(witness),
        "sorted_domain_sanity": replay_sorted_domain(),
        "exact_output_counterexample": replay_exact_output(witness),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
