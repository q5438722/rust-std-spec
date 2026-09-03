#!/usr/bin/env python3
"""Independently replay target-078 operational witnesses."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


TARGET = "core::slice::select_nth_unstable_by"
INPUT_ORDER = "78"
MODEL_ID = "target-078-operational-v1-rust-1.96-complete"
ACTIVE_CONTRACT_SHA256 = (
    "8d197563a2e9735beef3c52ff46ea5d3dd44da47b48e3b199654cf3c667490d7"
)


def _expected_reference(
    input_record: dict[str, Any],
    start: int,
    span: int,
    kind: str,
) -> dict[str, Any]:
    return {
        "allocation": input_record["allocation"],
        "parent_borrow": input_record["borrow"],
        "start": start,
        "span": span,
        "projection_kind": kind,
    }


def active_contract(
    input_record: dict[str, Any], execution: dict[str, Any]
) -> dict[str, bool]:
    initial = input_record["sequence"]
    index = input_record["index"]
    output = execution["output"]
    final = execution["final_state"]
    sequence = final["sequence"]
    valid = 0 <= index < len(initial)
    pivot = sequence[index] if valid and len(sequence) == len(initial) else None
    left = sequence[:index]
    right = sequence[index + 1 :]
    return {
        "normal_return": (
            execution["coverage_status"] == "modeled-normal"
            and output is not None
            and not final["panicked"]
            and final["terminal"]
        ),
        "final_concat": (
            output is not None
            and left + [pivot] + right == sequence
        ),
        "left_length": (
            output is not None
            and output["left"]
            == _expected_reference(
                input_record, 0, index, "left-subslice"
            )
        ),
        "pivot_at_index": (
            output is not None
            and output["pivot"]
            == _expected_reference(
                input_record, index, 1, "pivot-element"
            )
            and output["pivot_identity"] == pivot
        ),
        "right_length": (
            output is not None
            and output["right"]
            == _expected_reference(
                input_record,
                index + 1,
                len(initial) - index - 1,
                "right-subslice",
            )
        ),
        "slice_permutation": Counter(initial) == Counter(sequence),
        "callback_partition": (
            pivot is not None
            and all(identity <= pivot for identity in left)
            and all(pivot <= identity for identity in right)
        ),
        "in_place_state": (
            final["allocation"] == input_record["allocation"]
            and final["borrow"] == input_record["borrow"]
            and final["length"] == len(initial)
        ),
    }


def exact_equivalent(
    first: dict[str, Any], second: dict[str, Any]
) -> bool:
    return (
        first["coverage_status"] == second["coverage_status"]
        and first["output"] == second["output"]
        and first["final_state"] == second["final_state"]
    )


def _replay_total_insertion(
    input_record: dict[str, Any],
    relation: dict[str, Any],
) -> dict[str, Any]:
    if (
        relation.get("ordering") != "state-prefix-less-then-greater"
        or relation.get("next_state") != "increment"
        or relation.get("contract_ordering") is not None
        or relation.get("panic_states") != []
        or relation.get("panic_keys") != []
    ):
        raise ValueError("unexpected total callback relation")
    cutoff = relation.get("ordering_cutoff")
    if not isinstance(cutoff, int):
        raise ValueError("total callback relation lacks an integer cutoff")
    sequence = list(input_record["sequence"])
    state = relation["initial_state"]
    for tail in range(1, len(sequence)):
        temporary = sequence[tail]

        def is_less(left: int, right: int) -> bool:
            nonlocal state
            del left, right
            ordering = -1 if state < cutoff else 1
            state += 1
            return ordering == -1

        if not is_less(temporary, sequence[tail - 1]):
            continue
        gap = tail
        sift = tail - 1
        while True:
            sequence[gap] = sequence[sift]
            gap = sift
            if sift == 0:
                break
            sift -= 1
            if not is_less(temporary, sequence[sift]):
                break
        sequence[gap] = temporary
    return {"sequence": sequence, "callback_state": state}


def replay(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if (
        payload.get("target") != TARGET
        or payload.get("input_order") != INPUT_ORDER
        or payload.get("model_id") != MODEL_ID
        or payload.get("active_contract_sha256")
        != ACTIVE_CONTRACT_SHA256
    ):
        raise ValueError("target-078 witness identity or contract changed")

    normal = payload["normal_determinism"]
    first_checks = active_contract(
        normal["input"], normal["execution1"]
    )
    second_checks = active_contract(
        normal["input"], normal["execution2"]
    )
    sorted_pivot = sorted(normal["input"]["sequence"])[
        normal["input"]["index"]
    ]
    normal_observed = {
        "same_input_and_boundary": (
            normal["execution1_context"]
            == normal["execution2_context"]
            and normal["execution1_context"]["input"] == normal["input"]
            and normal["execution1_context"]["boundary"]
            == normal["boundary"]
        ),
        "execution1_satisfies_active_contract": all(
            first_checks.values()
        ),
        "execution2_satisfies_active_contract": all(
            second_checks.values()
        ),
        "pivot_is_sorted_order_statistic": (
            normal["execution1"]["output"]["pivot_identity"]
            == sorted_pivot
            and normal["execution2"]["output"]["pivot_identity"]
            == sorted_pivot
        ),
        "exact_principal_return_and_final_state": exact_equivalent(
            normal["execution1"], normal["execution2"]
        ),
    }
    if normal_observed != normal["expected"]:
        raise ValueError(
            f"normal determinism witness mismatch: {normal_observed!r}"
        )

    frozen = payload["frozen_prior_falsifier"]
    first_frozen = _replay_total_insertion(
        frozen["input"], frozen["total_relation"]
    )
    second_frozen = _replay_total_insertion(
        frozen["input"], frozen["total_relation"]
    )
    frozen_observed = {
        "relation_is_total_and_trace_independent": True,
        "final_sequence": first_frozen["sequence"],
        "callback_state": first_frozen["callback_state"],
        "exact_principal_return_and_final_state": (
            first_frozen == second_frozen
            and exact_equivalent(
                frozen["execution1"], frozen["execution2"]
            )
        ),
    }
    if frozen_observed != frozen["expected"]:
        raise ValueError(
            f"frozen prior falsifier mismatch: {frozen_observed!r}"
        )

    branches = payload["branch_witnesses"]
    fallback = branches["sixteen_step_fallback"]
    fallback_execution = fallback["execution"]
    fallback_observed = {
        "choose_pivot_count": fallback_execution["event_counts"].get(
            "choose-pivot", 0
        ),
        "terminal": fallback_execution["event_details"][
            "introselect_terminal"
        ][-1],
        "permutation": (
            Counter(fallback["input"]["sequence"])
            == Counter(fallback_execution["final_state"]["sequence"])
        ),
    }
    if (
        fallback_observed["choose_pivot_count"]
        != fallback["expected_choose_pivot_count"]
        or fallback_observed["terminal"]
        != fallback["expected_terminal"]
        or not fallback_observed["permutation"]
    ):
        raise ValueError(
            f"fallback branch witness mismatch: {fallback_observed!r}"
        )

    expected_implementations = {
        "lomuto-cyclic-unroll-two": "lomuto-cyclic",
        "lomuto-cyclic-unroll-one": "lomuto-cyclic",
        "hoare-cyclic": "hoare-cyclic",
        "lomuto-simple": "lomuto-simple",
        "optimize-hoare-cyclic": "hoare-cyclic",
    }
    configuration_results: dict[str, Any] = {}
    for label, record in branches["partition_configurations"].items():
        execution = record["execution"]
        implementations = execution["event_details"][
            "partition_implementations"
        ]
        checks = active_contract(record["input"], execution)
        observed = {
            "implementation_reached": (
                expected_implementations[label] in implementations
            ),
            "active_contract": all(checks.values()),
        }
        if not all(observed.values()):
            raise ValueError(
                f"{label} configuration witness mismatch: {observed!r}"
            )
        configuration_results[label] = observed

    negative_results: dict[str, bool] = {}
    baseline = normal["execution1"]
    for name, record in payload["negative_witnesses"].items():
        observed = exact_equivalent(baseline, record["candidate"])
        if observed != record["expected_exact_equivalent"]:
            raise ValueError(f"{name} exact-equivalence witness mismatch")
        negative_results[name] = observed
    expected_negatives = {
        "post_sequence_drift",
        "post_callback_state_drift",
        "returned_pivot_reference_drift",
        "panic_status_drift",
    }
    if set(negative_results) != expected_negatives:
        raise ValueError("target-078 negative witness set changed")

    return {
        "status": "passed",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "normal_determinism": {
            "execution1_contract": first_checks,
            "execution2_contract": second_checks,
            "observed": normal_observed,
        },
        "frozen_prior_falsifier": frozen_observed,
        "fallback": fallback_observed,
        "partition_configurations": configuration_results,
        "negative_witnesses": negative_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
