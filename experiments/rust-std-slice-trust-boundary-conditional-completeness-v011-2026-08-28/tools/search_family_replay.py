#!/usr/bin/env python3
"""Independent concrete replay for the bounded Slice search-wrapper models."""

from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path
from typing import Any

from search_family import SearchTarget


ORDERING_RANK = {"Less": -1, "Equal": 0, "Greater": 1}
KEY_RANK = {"KLow": -1, "KMid": 0, "KHigh": 1}


def compare_rank(left: int, right: int) -> str:
    if left < right:
        return "Less"
    if left == right:
        return "Equal"
    return "Greater"


def result_in_bounds(length: int, result: dict[str, Any]) -> bool:
    tag = result.get("tag")
    index = result.get("index")
    if not isinstance(index, int):
        return False
    if tag == "Ok":
        return 0 <= index < length
    if tag == "Err":
        return 0 <= index <= length
    return False


def insertion_point(
    length: int, profile: list[str], index: int
) -> bool:
    return (
        0 <= index <= length
        and all(value == "Less" for value in profile[:index])
        and all(value == "Greater" for value in profile[index:])
    )


def binary_contract_holds(
    length: int,
    profile: list[str],
    ordered: bool,
    result: dict[str, Any],
) -> bool:
    if not result_in_bounds(length, result):
        return False
    if not ordered:
        return True
    index = result["index"]
    if result["tag"] == "Ok":
        return profile[index] == "Equal"
    return insertion_point(length, profile, index)


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


def partitioned(profile: list[bool]) -> bool:
    return not (profile[1] and not profile[0])


def partition_point_at(profile: list[bool], index: int) -> bool:
    return (
        0 <= index <= len(profile)
        and all(profile[:index])
        and not any(profile[index:])
    )


def partition_contract_holds(profile: list[bool], index: int) -> bool:
    if not 0 <= index <= len(profile):
        return False
    return not partitioned(profile) or partition_point_at(profile, index)


def all_results(length: int) -> list[dict[str, Any]]:
    return [
        *({"tag": "Ok", "index": index} for index in range(length)),
        *({"tag": "Err", "index": index} for index in range(length + 1)),
    ]


def _profile(
    config: SearchTarget,
    input_record: dict[str, Any],
    boundary: dict[str, Any],
) -> tuple[list[str] | list[bool], bool]:
    if boundary["element_reads"] != input_record["elements"]:
        raise ValueError("witness element reads differ from the fixed input")
    if config.kind == "ord":
        expected = [
            compare_rank(value, input_record["search_value"])
            for value in boundary["element_reads"]
        ]
        if boundary["comparator_results"] != expected:
            raise ValueError("Ord comparator observations do not match the adapter")
        ordered = boundary["element_reads"][0] <= boundary["element_reads"][1]
        return expected, ordered
    if config.kind == "key":
        keys = boundary["extracted_keys"]
        expected = [
            compare_rank(KEY_RANK[value], KEY_RANK[input_record["search_key"]])
            for value in keys
        ]
        if boundary["comparator_results"] != expected:
            raise ValueError("key comparator observations do not match the adapter")
        return expected, KEY_RANK[keys[0]] <= KEY_RANK[keys[1]]
    predicates = boundary["predicate_results"]
    return predicates, partitioned(predicates)


def _final_state(
    input_record: dict[str, Any], boundary: dict[str, Any]
) -> int:
    return (
        input_record["callback_initial_state"]
        + sum(boundary["callback_state_deltas"])
    )


def _replay_case(
    config: SearchTarget,
    case: dict[str, Any],
    *,
    exact: bool,
) -> dict[str, Any]:
    input_record = case["input"]
    boundary = case["boundary"]
    profile, domain_holds = _profile(config, input_record, boundary)
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    expected_state = _final_state(input_record, boundary)
    states_match = (
        execution1["callback_final_state"] == expected_state
        and execution2["callback_final_state"] == expected_state
    )
    if config.kind == "partition":
        assert isinstance(profile[0], bool)
        first_holds = states_match and partition_contract_holds(
            profile, execution1["index"]
        )
        second_holds = states_match and partition_contract_holds(
            profile, execution2["index"]
        )
        observed = {
            "domain_profile": (
                "partitioned" if domain_holds else "non-partitioned"
            ),
            "execution1_satisfies_contract": first_holds,
            "execution2_satisfies_contract": second_holds,
            "exactly_equal": execution1 == execution2,
        }
    else:
        assert isinstance(profile[0], str)
        first_holds = states_match and binary_contract_holds(
            input_record["length"],
            profile,
            domain_holds,
            execution1["result"],
        )
        second_holds = states_match and binary_contract_holds(
            input_record["length"],
            profile,
            domain_holds,
            execution2["result"],
        )
        if exact:
            observed = {
                "domain_profile": "ordered" if domain_holds else "unordered",
                "execution1_satisfies_contract": first_holds,
                "execution2_satisfies_contract": second_holds,
                "matching_index_equivalent": matching_index_equivalent(
                    profile, execution1, execution2
                ),
                "exactly_equal": execution1 == execution2,
            }
        else:
            observed = {
                "domain_profile": "ordered" if domain_holds else "unordered",
                "execution1_satisfies_contract": first_holds,
                "execution2_satisfies_contract": second_holds,
                "reviewed_equivalent": matching_index_equivalent(
                    profile, execution1, execution2
                ),
            }
    if observed != case["expected"]:
        raise ValueError(f"fixed witness replay mismatch: {observed!r}")
    return observed


def _ordered_sanity(config: SearchTarget) -> dict[str, Any]:
    profiles_checked = 0
    valid_result_pairs_checked = 0
    results = all_results(2)
    domains: list[tuple[list[str], bool]] = []
    if config.kind == "ord":
        for left, right, target in product((-1, 0, 1), repeat=3):
            if left <= right:
                domains.append(
                    (
                        [
                            compare_rank(left, target),
                            compare_rank(right, target),
                        ],
                        True,
                    )
                )
    else:
        for left, right, target in product(KEY_RANK.values(), repeat=3):
            if left <= right:
                domains.append(
                    (
                        [
                            compare_rank(left, target),
                            compare_rank(right, target),
                        ],
                        True,
                    )
                )
    for profile, ordered in domains:
        profiles_checked += 1
        valid = [
            result
            for result in results
            if binary_contract_holds(2, profile, ordered, result)
        ]
        for result1, result2 in product(valid, repeat=2):
            valid_result_pairs_checked += 1
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
                    "ordered-domain replay found inequivalent contract results"
                )
    return {
        "profiles_checked": profiles_checked,
        "valid_result_pairs_checked": valid_result_pairs_checked,
        "all_pairs_equivalent": True,
    }


def _partitioned_sanity() -> dict[str, Any]:
    profiles_checked = 0
    valid_index_pairs_checked = 0
    for raw_profile in product((False, True), repeat=2):
        profile = list(raw_profile)
        if not partitioned(profile):
            continue
        profiles_checked += 1
        valid = [
            index
            for index in range(3)
            if partition_contract_holds(profile, index)
        ]
        for left, right in product(valid, repeat=2):
            valid_index_pairs_checked += 1
            if left != right:
                raise ValueError(
                    "partitioned-domain replay found distinct valid indices"
                )
    return {
        "profiles_checked": profiles_checked,
        "valid_index_pairs_checked": valid_index_pairs_checked,
        "all_pairs_exactly_equal": True,
    }


def replay(config: SearchTarget, path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    witness = json.loads(raw)
    if (
        witness.get("target") != config.target
        or witness.get("input_order") != config.input_order
        or witness.get("active_contract_sha256")
        != config.active_contract_sha256
    ):
        raise ValueError("witness identity or active contract hash mismatch")
    sanity = (
        _partitioned_sanity()
        if config.kind == "partition"
        else _ordered_sanity(config)
    )
    return {
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "general_counterexample": _replay_case(
            config, witness["general_counterexample"], exact=False
        ),
        config.sanity_purpose.replace("-", "_"): sanity,
        "exact_output_counterexample": _replay_case(
            config, witness["exact_output_counterexample"], exact=True
        ),
    }
