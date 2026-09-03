#!/usr/bin/env python3
"""Independent replay for targets 080 and 082 unstable-sort evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import permutations, product
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_080
import target_082
from unstable_sort_companions import TargetConfig


MODULE_BY_TARGET = {
    target_080.TARGET: target_080,
    target_082.TARGET: target_082,
}


def _int_map(raw: dict[str, Any], label: str) -> dict[int, int]:
    if not isinstance(raw, dict):
        raise ValueError(f"{label} must be an object")
    try:
        return {int(key): int(value) for key, value in raw.items()}
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must map integer strings to integers") from exc


def class_map(
    config: TargetConfig,
    boundary: dict[str, Any],
) -> dict[int, int]:
    if config.mode == "ord":
        return _int_map(
            boundary.get("ord_class_by_identity"),
            "ord_class_by_identity",
        )
    keys = _int_map(
        boundary.get("key_by_identity"),
        "key_by_identity",
    )
    classes = _int_map(
        boundary.get("ord_class_by_key"),
        "ord_class_by_key",
    )
    try:
        return {
            identity: classes[key]
            for identity, key in keys.items()
        }
    except KeyError as exc:
        raise ValueError("an extracted key lacks an Ord class") from exc


def contract_holds(
    config: TargetConfig,
    case: dict[str, Any],
    execution: dict[str, Any],
) -> bool:
    input_record = case["input"]
    boundary = case["boundary"]
    identities = input_record["identities"]
    final_slice = execution["final_slice"]
    classes = class_map(config, boundary)
    try:
        sorted_result = all(
            classes[final_slice[left]] <= classes[final_slice[right]]
            for left in range(3)
            for right in range(left, 3)
        )
    except KeyError:
        return False
    return (
        len(identities) == 3
        and len(set(identities)) == 3
        and set(identities) <= set(classes)
        and isinstance(boundary.get("callback_state_delta"), int)
        and boundary["callback_state_delta"] >= 0
        and execution["return_unit"] is True
        and len(final_slice) == 3
        and Counter(final_slice) == Counter(identities)
        and sorted_result
        and execution["callback_final_state"]
        == input_record["callback_initial_state"]
        + boundary["callback_state_delta"]
    )


def reviewed_equivalent(
    config: TargetConfig,
    boundary: dict[str, Any],
    execution1: dict[str, Any],
    execution2: dict[str, Any],
) -> bool:
    left = execution1["final_slice"]
    right = execution2["final_slice"]
    if (
        execution1["return_unit"] != execution2["return_unit"]
        or execution1["callback_final_state"]
        != execution2["callback_final_state"]
        or Counter(left) != Counter(right)
        or len(left) != len(right)
    ):
        return False
    classes = class_map(config, boundary)
    try:
        return all(
            classes[left[index]] == classes[right[index]]
            for index in range(len(left))
        )
    except KeyError:
        return False


def replay_exact_case(
    config: TargetConfig,
    case: dict[str, Any],
) -> dict[str, bool]:
    execution1 = case["execution1"]
    execution2 = case["execution2"]
    observed = {
        "execution1_satisfies_active_contract": contract_holds(
            config, case, execution1
        ),
        "execution2_satisfies_active_contract": contract_holds(
            config, case, execution2
        ),
        "same_fixed_boundary": True,
        "identity_multiplicities_equal": (
            Counter(execution1["final_slice"])
            == Counter(execution2["final_slice"])
        ),
        "callback_final_state_equal": (
            execution1["callback_final_state"]
            == execution2["callback_final_state"]
        ),
        "reviewed_equal_class_equivalent": reviewed_equivalent(
            config, case["boundary"], execution1, execution2
        ),
        "exact_final_slice_equal": (
            execution1["final_slice"] == execution2["final_slice"]
        ),
    }
    if observed != case["expected"]:
        raise ValueError(f"exact witness replay mismatch: {observed!r}")
    return observed


def replay_negative_cases(
    config: TargetConfig,
    witness: dict[str, Any],
) -> dict[str, bool]:
    exact = witness["exact_final_slice_counterexample"]
    observed: dict[str, bool] = {}
    for name in (
        "unequal_class_negative_witness",
        "foreign_identity_negative_witness",
        "callback_state_drift_negative_witness",
    ):
        case = witness[name]
        equivalent = reviewed_equivalent(
            config,
            case["boundary"],
            case["execution1"],
            case["execution2"],
        )
        if equivalent != case["expected_reviewed_equivalent"]:
            raise ValueError(f"{name}: equivalence polarity changed")
        observed[name] = not equivalent
    callback_case = witness["callback_state_drift_negative_witness"]
    second_contract = contract_holds(
        config,
        {
            "input": exact["input"],
            "boundary": callback_case["boundary"],
        },
        callback_case["execution2"],
    )
    if (
        second_contract
        != callback_case["expected_execution2_satisfies_active_contract"]
    ):
        raise ValueError("callback-state drift contract polarity changed")
    observed["callback_state_drift_rejected_by_contract"] = not second_contract
    return observed


def replay_bounded_sanity() -> dict[str, Any]:
    identities = (10, 11, 20)
    outputs = list(permutations(identities))
    profiles_checked = 0
    result_pairs_checked = 0
    for values in product(range(3), repeat=3):
        classes = dict(zip(identities, values))
        sorted_outputs = [
            output
            for output in outputs
            if all(
                classes[output[left]] <= classes[output[right]]
                for left in range(3)
                for right in range(left, 3)
            )
        ]
        profiles_checked += 1
        for left in sorted_outputs:
            for right in sorted_outputs:
                result_pairs_checked += 1
                if Counter(left) != Counter(right) or not all(
                    classes[left[index]] == classes[right[index]]
                    for index in range(3)
                ):
                    raise ValueError(
                        "total Ord profile admitted unequal-class sorted outputs"
                    )
    return {
        "class_profiles_checked": profiles_checked,
        "valid_result_pairs_checked": result_pairs_checked,
        "all_pairs_equal_class_equivalent": True,
    }


def replay(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    witness = json.loads(raw)
    module = MODULE_BY_TARGET.get(witness.get("target"))
    if module is None:
        raise ValueError("unknown unstable-sort companion target")
    config = module.CONFIG
    if (
        witness.get("input_order") != config.input_order
        or witness.get("active_contract_sha256")
        != config.active_contract_sha256
    ):
        raise ValueError("witness identity or active contract hash mismatch")
    return {
        "status": "passed",
        "target": config.target,
        "input_order": config.input_order,
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "exact_final_slice_counterexample": replay_exact_case(
            config, witness["exact_final_slice_counterexample"]
        ),
        "negative_equivalence_witnesses": replay_negative_cases(
            config, witness
        ),
        "bounded_sanity": replay_bounded_sanity(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
