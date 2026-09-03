#!/usr/bin/env python3
"""Replay targets 078-079 witnesses against source-step semantics."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


TARGETS = {
    "core::slice::select_nth_unstable_by": {
        "input_order": "78",
        "active_contract_sha256": (
            "8d197563a2e9735beef3c52ff46ea5d3dd44da47b48e3b199654cf3c667490d7"
        ),
        "mode": "compare",
    },
    "core::slice::select_nth_unstable_by_key": {
        "input_order": "79",
        "active_contract_sha256": (
            "9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95"
        ),
        "mode": "key",
    },
}


def _source_relation(boundary: dict[str, Any]) -> dict[str, Any]:
    relation = boundary.get("source_step_relation")
    if not isinstance(relation, dict):
        raise ValueError("callback source-step relation is missing")
    return relation


def _ordering(relation: dict[str, Any], left: int, right: int) -> str:
    table = relation.get("ordering_by_pair")
    if not isinstance(table, dict):
        raise ValueError("comparator Ordering relation is missing")
    result = table.get(f"{left},{right}", table.get("default"))
    if result not in {"Less", "Equal", "Greater"}:
        raise ValueError("comparator Ordering result is invalid")
    return str(result)


def _key(relation: dict[str, Any], identity: int) -> int:
    table = relation.get("key_by_identity")
    if not isinstance(table, dict):
        raise ValueError("key relation is missing")
    if str(identity) in table:
        return int(table[str(identity)])
    if relation.get("default_key") != "identity":
        raise ValueError("unknown key relation default")
    return identity


def _adapter_outcomes(
    mode: str,
    boundary: dict[str, Any],
    state: int,
    left: int,
    right: int,
) -> set[tuple[bool, int]]:
    relation = _source_relation(boundary)
    if relation.get("panic") is not False:
        raise ValueError("normal witness relation unexpectedly permits panic")
    outcomes: set[tuple[bool, int]] = set()
    if mode == "compare":
        ordering = _ordering(relation, left, right)
        delta = int(relation["next_state_delta"])
        outcomes.add((ordering == "Less", state + delta))
        return outcomes

    if relation.get("evaluation_order") != [
        "f(left)",
        "f(right)",
        "Ord::lt",
    ]:
        raise ValueError("key adapter evaluation order changed")
    left_key = _key(relation, left)
    right_key = _key(relation, right)
    key_delta = int(relation["key_next_state_delta"])
    ord_delta = int(relation["ord_next_state_delta"])
    after_left = state + key_delta
    after_right = after_left + key_delta
    outcomes.add((left_key < right_key, after_right + ord_delta))
    return outcomes


def _minimum_source_outcomes(
    mode: str,
    input_record: dict[str, Any],
    boundary: dict[str, Any],
) -> set[tuple[tuple[int, ...], int]]:
    sequence = list(input_record["sequence"])
    if len(sequence) != 2 or input_record["index"] != 0:
        raise ValueError("classification witness is not the length-two min branch")
    candidate = sequence[1]
    accumulator = sequence[0]
    initial_state = int(boundary["initial_callback_state"])
    results: set[tuple[tuple[int, ...], int]] = set()
    for is_less, next_state in _adapter_outcomes(
        mode, boundary, initial_state, candidate, accumulator
    ):
        winner = 1 if is_less else 0
        final = list(sequence)
        final[0], final[winner] = final[winner], final[0]
        results.add((tuple(final), next_state))
    return results


def _insertion_sort_source_outcome(
    mode: str,
    input_record: dict[str, Any],
    boundary: dict[str, Any],
) -> tuple[list[int], int]:
    sequence = list(input_record["sequence"])
    state = int(boundary["initial_callback_state"])
    for tail in range(1, len(sequence)):
        temporary = sequence[tail]
        insertion = tail
        while insertion > 0:
            outcomes = _adapter_outcomes(
                mode,
                boundary,
                state,
                temporary,
                sequence[insertion - 1],
            )
            if len(outcomes) != 1:
                raise ValueError("functional callback produced multiple outcomes")
            is_less, state = next(iter(outcomes))
            if not is_less:
                break
            sequence[insertion] = sequence[insertion - 1]
            insertion -= 1
        sequence[insertion] = temporary
    return sequence, state


def _expected_references(
    input_record: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    length = len(input_record["sequence"])
    index = int(input_record["index"])
    allocation = int(input_record["allocation"])
    borrow = int(input_record["borrow"])

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


def _contract_leq(
    mode: str,
    boundary: dict[str, Any],
    left: int,
    right: int,
) -> bool:
    relation = _source_relation(boundary)
    if mode == "compare":
        return _ordering(relation, left, right) in {"Less", "Equal"}
    return not (_key(relation, right) < _key(relation, left))


def active_contract(
    mode: str,
    input_record: dict[str, Any],
    boundary: dict[str, Any],
    execution: dict[str, Any],
) -> dict[str, bool]:
    initial = list(input_record["sequence"])
    index = int(input_record["index"])
    output = execution["output"]
    final = execution["final"]
    sequence = list(final["sequence"])
    pivot = sequence[index] if len(sequence) == len(initial) else None
    expected_references = _expected_references(input_record)
    left = sequence[:index]
    right = sequence[index + 1 :]
    partition = (
        pivot is not None
        and all(_contract_leq(mode, boundary, value, pivot) for value in left)
        and all(_contract_leq(mode, boundary, pivot, value) for value in right)
    )
    return {
        "requires_index_in_bounds": 0 <= index < len(initial),
        "final_concat_and_lengths": (
            len(sequence) == len(initial)
            and final.get("length") == len(initial)
            and output.get("left_length") == index
            and output.get("right_length") == len(initial) - index - 1
        ),
        "returned_range_identities": all(
            output.get(name) == value
            for name, value in expected_references.items()
        ),
        "pivot_at_index": output.get("pivot_identity") == pivot,
        "exact_identity_multiplicity": Counter(sequence) == Counter(initial),
        "callback_partition": partition,
        "in_place_state_identity": (
            final.get("allocation") == input_record["allocation"]
            and final.get("borrow") == input_record["borrow"]
            and final.get("panicked") is False
        ),
    }


def _profile(
    mode: str,
    boundary: dict[str, Any],
    identity: int,
    pivot: int,
) -> tuple[bool, bool]:
    return (
        _contract_leq(mode, boundary, identity, pivot),
        _contract_leq(mode, boundary, pivot, identity),
    )


def reviewed_equivalent(
    mode: str,
    input_record: dict[str, Any],
    boundary: dict[str, Any],
    first: dict[str, Any],
    second: dict[str, Any],
) -> bool:
    return first == second


def replay(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = json.loads(raw)
    target = payload.get("target")
    identity = TARGETS.get(str(target))
    if identity is None:
        raise ValueError("unknown selection callback target")
    if (
        payload.get("input_order") != identity["input_order"]
        or payload.get("active_contract_sha256")
        != identity["active_contract_sha256"]
    ):
        raise ValueError("witness target identity or contract hash changed")
    mode = str(identity["mode"])
    input_record = payload["input"]
    boundary = payload["boundary"]
    counterexample = payload["functional_boundary_diagnostic"]
    first = counterexample["execution1"]
    second = counterexample["execution2"]
    source_outcomes = _minimum_source_outcomes(mode, input_record, boundary)
    first_source = (
        tuple(first["final"]["sequence"]),
        int(first["final"]["callback_state"]),
    ) in source_outcomes
    second_source = (
        tuple(second["final"]["sequence"]),
        int(second["final"]["callback_state"]),
    ) in source_outcomes
    first_checks = active_contract(
        mode, input_record, boundary, first
    )
    second_checks = active_contract(
        mode, input_record, boundary, second
    )
    observed = {
        "same_input_and_boundary": True,
        "execution1_is_source_reachable": first_source,
        "execution2_is_source_reachable": second_source,
        "execution1_satisfies_active_contract": all(first_checks.values()),
        "execution2_satisfies_active_contract": all(second_checks.values()),
        "exact_equivalent": first == second,
        "reviewed_selection_equivalent": reviewed_equivalent(
            mode, input_record, boundary, first, second
        ),
        "only_difference": "callback-visible-final-state",
    }
    if observed != counterexample["expected"]:
        raise ValueError(f"classification witness mismatch: {observed!r}")

    source_witness = payload["bounded_source_execution_witness"]
    source_sequence, source_state = _insertion_sort_source_outcome(
        mode,
        source_witness["input"],
        source_witness["boundary"],
    )
    source_observed = {
        "sequence": source_sequence,
        "callback_state": source_state,
    }
    if source_observed != source_witness["expected"]:
        raise ValueError(
            f"bounded source witness mismatch: {source_observed!r}"
        )

    negative_results: dict[str, Any] = {}
    for name, record in payload["negative_witnesses"].items():
        baseline_checks = active_contract(
            mode, input_record, boundary, record["baseline"]
        )
        candidate_checks = active_contract(
            mode, input_record, boundary, record["candidate"]
        )
        candidate_contract = all(candidate_checks.values())
        if (
            not all(baseline_checks.values())
            or candidate_contract
            != record["candidate_satisfies_active_contract"]
        ):
            raise ValueError(f"{name} active-contract witness mismatch")
        equivalent = reviewed_equivalent(
            mode,
            input_record,
            boundary,
            record["baseline"],
            record["candidate"],
        )
        if name == "callback_final_state_drift" and equivalent:
            raise ValueError("callback state drift was not distinguished")
        negative_results[name] = {
            "baseline_satisfies_active_contract": True,
            "candidate_satisfies_active_contract": candidate_contract,
            "reviewed_selection_equivalent": equivalent,
        }

    return {
        "status": "passed",
        "target": target,
        "input_order": identity["input_order"],
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "functional_boundary_diagnostic": {
            "source_outcomes": sorted(
                [
                    {"sequence": list(sequence), "callback_state": state}
                    for sequence, state in source_outcomes
                ],
                key=lambda item: (item["callback_state"], item["sequence"]),
            ),
            "execution1_active_contract_checks": first_checks,
            "execution2_active_contract_checks": second_checks,
            "observed": observed,
        },
        "bounded_source_execution_witness": source_observed,
        "negative_witnesses": negative_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
