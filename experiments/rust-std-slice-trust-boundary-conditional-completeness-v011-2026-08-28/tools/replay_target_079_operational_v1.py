#!/usr/bin/env python3
"""Independently replay target-079 operational-v1 witnesses."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


TARGET = "core::slice::select_nth_unstable_by_key"
INPUT_ORDER = "79"
MODEL_ID = "target-079-key-ord-drop-operational-v1-rust-1.96-complete"
ACTIVE_CONTRACT_SHA256 = (
    "9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95"
)


def _normal_contract(
    input_record: dict[str, Any],
    execution: dict[str, Any],
) -> dict[str, bool]:
    initial = input_record["sequence"]
    index = input_record["index"]
    final = execution["final_state"]["sequence"]
    output = execution["output"]
    pivot = final[index]
    left = final[:index]
    right = final[index + 1 :]
    return {
        "normal-return": (
            execution["termination"] == "normal"
            and execution["coverage_status"] == "modeled-normal"
            and output is not None
        ),
        "final-concat": left + [pivot] + right == final,
        "left-length": output["left"]["span"] == index,
        "pivot-at-index": (
            output["pivot"]["start"] == index
            and output["pivot_identity"] == pivot
        ),
        "right-length": (
            output["right"]["span"] == len(initial) - index - 1
        ),
        "slice-permutation": Counter(initial) == Counter(final),
        "key-partition": (
            all(value <= pivot for value in left)
            and all(pivot <= value for value in right)
        ),
        "in-place": (
            execution["final_state"]["allocation"]
            == input_record["allocation"]
            and execution["final_state"]["borrow"]
            == input_record["borrow"]
        ),
    }


def replay(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if (
        payload.get("target") != TARGET
        or payload.get("input_order") != INPUT_ORDER
        or payload.get("model_id") != MODEL_ID
        or payload.get("active_contract_sha256")
        != ACTIVE_CONTRACT_SHA256
    ):
        raise ValueError("target-079 witness identity or contract changed")

    normal = payload["normal"]
    first = normal["execution1"]
    second = normal["execution2"]
    contract = _normal_contract(normal["input"], first)
    if not all(contract.values()) or first != second:
        raise ValueError("normal exact-determinism witness failed")

    ordinary = payload["ordinary_panic"]
    if (
        ordinary["termination"] != "panic"
        or ordinary["final_state"]["sequence"] != [3, 2, 4, 1]
        or Counter(ordinary["final_state"]["sequence"])
        != Counter([4, 3, 2, 1])
        or ordinary["output"] is not None
    ):
        raise ValueError("ordinary unwind restoration witness failed")

    aborted = payload["abort"]
    if (
        aborted["termination"] != "abort"
        or aborted["coverage_status"] != "modeled-abort"
        or aborted["final_state"]["sequence"] != [3, 4, 4, 1]
        or aborted["final_state"]["callback_state"] != 15
        or Counter(aborted["final_state"]["sequence"])
        == Counter([4, 3, 2, 1])
        or aborted["output"] is not None
    ):
        raise ValueError("abort interrupted-state witness failed")

    lifecycle = payload[
        "lt_panic_right_cleanup_left_drop_panic"
    ]
    events = lifecycle["events"]
    if (
        lifecycle["termination"] != "abort"
        or [event["action"] for event in events]
        != [
            "key-left",
            "key-right",
            "ord-lt",
            "drop-right",
            "drop-left",
        ]
        or events[-2]["panicked"]
        or not events[-1]["panicked"]
        or not events[-1]["unwinding"]
        or events[0]["owned_key"] == events[1]["owned_key"]
    ):
        raise ValueError("owned-key cleanup lifecycle witness failed")

    negatives = payload["negative_exact_equivalence"]
    if any(candidate == first for candidate in negatives.values()):
        raise ValueError("negative exact-equivalence witness collapsed")

    return {
        "status": "passed",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "normal_contract": contract,
        "ordinary_panic_restored": True,
        "abort_retained_interrupted_state": True,
        "missing_cleanup_path_replayed": True,
        "negative_exact_equivalence": {
            name: False for name in negatives
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), sort_keys=True))


if __name__ == "__main__":
    main()
