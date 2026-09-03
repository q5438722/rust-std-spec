#!/usr/bin/env python3
"""Replay target 077 selection witnesses against the active contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


TARGET = "core::slice::select_nth_unstable"
INPUT_ORDER = "77"
ACTIVE_CONTRACT_SHA256 = (
    "e570c36bf97546100d3408a95ea9c5f821ba0aed6ebe0e63ef6358d7d713fdaf"
)


def _classes(boundary: dict[str, Any]) -> dict[int, int]:
    raw = boundary.get("class_by_identity")
    if not isinstance(raw, dict):
        raise ValueError("Ord boundary class map is missing")
    return {int(identity): int(value) for identity, value in raw.items()}


def _expected_references(input_record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    length = len(input_record["sequence"])
    index = input_record["index"]
    allocation = input_record["allocation"]
    borrow = input_record["borrow"]

    def reference(start: int, span: int, kind: str) -> dict[str, Any]:
        return {
            "allocation": allocation,
            "parent_borrow": borrow,
            "start": start,
            "span": span,
            "projection_kind": kind,
        }

    return {
        "left_reference": reference(0, index, "left-subslice"),
        "pivot_reference": reference(index, 1, "pivot-element"),
        "right_reference": reference(
            index + 1, length - index - 1, "right-subslice"
        ),
    }


def active_contract(
    input_record: dict[str, Any],
    boundary: dict[str, Any],
    execution: dict[str, Any],
) -> dict[str, bool]:
    initial = input_record["sequence"]
    index = input_record["index"]
    output = execution["output"]
    final = execution["final"]
    sequence = final["sequence"]
    classes = _classes(boundary)
    valid_domain = (
        0 <= index < len(initial)
        and input_record["ord_identity"] == boundary["ord_identity"]
    )
    known_identities = all(identity in classes for identity in sequence)
    pivot_identity = (
        sequence[index] if valid_domain and len(sequence) == len(initial) else None
    )
    expected_references = _expected_references(input_record)
    reference_checks = {
        name: output.get(name) == expected
        for name, expected in expected_references.items()
    }
    left = sequence[:index]
    right = sequence[index + 1 :]
    pivot_class = classes.get(pivot_identity) if pivot_identity is not None else None
    partition = (
        known_identities
        and pivot_class is not None
        and all(classes[identity] <= pivot_class for identity in left)
        and all(classes[identity] >= pivot_class for identity in right)
    )
    checks = {
        "requires_index_in_bounds": valid_domain,
        "final_concat_and_length": (
            len(sequence) == len(initial)
            and final.get("length") == len(initial)
            and output.get("left_length") == index
            and output.get("right_length") == len(initial) - index - 1
        ),
        "returned_range_identities": all(reference_checks.values()),
        "pivot_at_index": (
            pivot_identity is not None
            and output.get("pivot_identity") == pivot_identity
            and output.get("pivot_class") == pivot_class
        ),
        "exact_identity_multiplicity": Counter(sequence) == Counter(initial),
        "ord_partition": partition,
        "in_place_state_identity": (
            final.get("allocation") == input_record["allocation"]
            and final.get("borrow") == input_record["borrow"]
        ),
    }
    return checks


def reviewed_equivalent(
    boundary: dict[str, Any],
    first: dict[str, Any],
    second: dict[str, Any],
) -> bool:
    classes = _classes(boundary)
    first_output = first["output"]
    second_output = second["output"]
    first_final = first["final"]
    second_final = second["final"]
    first_index = first_output["left_length"]
    second_index = second_output["left_length"]

    def side_classes(sequence: list[int], index: int) -> tuple[Counter, Counter]:
        return (
            Counter(classes[identity] for identity in sequence[:index]),
            Counter(classes[identity] for identity in sequence[index + 1 :]),
        )

    exact_output_keys = (
        "left_reference",
        "pivot_reference",
        "right_reference",
        "left_length",
        "right_length",
        "pivot_class",
    )
    return (
        all(first_output[key] == second_output[key] for key in exact_output_keys)
        and Counter(first_final["sequence"]) == Counter(second_final["sequence"])
        and side_classes(first_final["sequence"], first_index)
        == side_classes(second_final["sequence"], second_index)
        and first_final["allocation"] == second_final["allocation"]
        and first_final["borrow"] == second_final["borrow"]
        and first_final["length"] == second_final["length"]
    )


def replay(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = json.loads(raw)
    if (
        payload.get("target") != TARGET
        or payload.get("input_order") != INPUT_ORDER
        or payload.get("active_contract_sha256") != ACTIVE_CONTRACT_SHA256
    ):
        raise ValueError("target-077 witness identity or contract hash changed")
    boundary = payload["boundary"]

    side = payload["exact_side_reordering_counterexample"]
    side_checks = [
        active_contract(side["input"], boundary, side["execution1"]),
        active_contract(side["input"], boundary, side["execution2"]),
    ]
    side_observed = {
        "same_input_and_boundary": True,
        "execution1_satisfies_active_contract": all(side_checks[0].values()),
        "execution2_satisfies_active_contract": all(side_checks[1].values()),
        "exact_equivalent": side["execution1"] == side["execution2"],
        "reviewed_selection_equivalent": reviewed_equivalent(
            boundary, side["execution1"], side["execution2"]
        ),
    }
    if side_observed != side["expected"]:
        raise ValueError(f"side-reordering witness mismatch: {side_observed!r}")

    equal = payload["equal_pivot_positive_witness"]
    equal_checks = [
        active_contract(equal["input"], boundary, equal["execution1"]),
        active_contract(equal["input"], boundary, equal["execution2"]),
    ]
    equal_observed = {
        "same_input_and_boundary": True,
        "execution1_satisfies_active_contract": all(equal_checks[0].values()),
        "execution2_satisfies_active_contract": all(equal_checks[1].values()),
        "pivot_identity_equal": (
            equal["execution1"]["output"]["pivot_identity"]
            == equal["execution2"]["output"]["pivot_identity"]
        ),
        "pivot_class_equal": (
            equal["execution1"]["output"]["pivot_class"]
            == equal["execution2"]["output"]["pivot_class"]
        ),
        "reviewed_selection_equivalent": reviewed_equivalent(
            boundary, equal["execution1"], equal["execution2"]
        ),
    }
    if equal_observed != equal["expected"]:
        raise ValueError(f"equal-pivot witness mismatch: {equal_observed!r}")

    negative_results: dict[str, dict[str, bool]] = {}
    for name, record in payload["negative_witnesses"].items():
        baseline_checks = active_contract(
            record["input"], boundary, record["baseline"]
        )
        candidate_checks = active_contract(
            record["input"], boundary, record["candidate"]
        )
        observed = {
            "baseline_satisfies_active_contract": all(baseline_checks.values()),
            "candidate_satisfies_active_contract": all(
                candidate_checks.values()
            ),
            "reviewed_selection_equivalent": reviewed_equivalent(
                boundary, record["baseline"], record["candidate"]
            ),
        }
        if (
            not observed["baseline_satisfies_active_contract"]
            or observed["candidate_satisfies_active_contract"]
            != record["expected_candidate_satisfies_active_contract"]
        ):
            raise ValueError(f"{name} negative witness mismatch: {observed!r}")
        if observed["reviewed_selection_equivalent"]:
            raise ValueError(f"{name} negative witness was not discriminated")
        negative_results[name] = observed

    expected_negatives = {
        "foreign_identity",
        "wrong_rank_class",
        "partition_crossing",
        "malformed_range",
        "state_drift",
    }
    if set(negative_results) != expected_negatives:
        raise ValueError("target-077 negative witness set changed")

    return {
        "status": "passed",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "exact_side_reordering_counterexample": {
            "active_contract_checks": side_checks,
            "observed": side_observed,
        },
        "equal_pivot_positive_witness": {
            "active_contract_checks": equal_checks,
            "observed": equal_observed,
        },
        "negative_witnesses": negative_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
