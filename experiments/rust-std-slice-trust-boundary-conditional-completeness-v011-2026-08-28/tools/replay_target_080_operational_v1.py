#!/usr/bin/env python3
"""Independently replay retained target-080 operational witnesses."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_080_operational_v1 as model
import target_080_operational_witness_v1 as witnesses


def replay(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if payload["target"] != model.TARGET:
        raise RuntimeError("witness target drifted")
    if payload["model_id"] != model.MODEL_ID:
        raise RuntimeError("witness model drifted")
    results: dict[str, Any] = {}
    for name, case in payload["cases"].items():
        primary, reference, steps, correspondence = (
            witnesses.execute_spec(case["spec"])
        )
        if primary != reference:
            raise RuntimeError(
                f"{name}: formal/source interpreters diverged"
            )
        if primary != case["expected"]:
            raise RuntimeError(f"{name}: retained witness drifted")
        if (
            not correspondence["callback_schedule_equal"]
            or correspondence != case["callback_correspondence"]
        ):
            raise RuntimeError(
                f"{name}: retained callback schedule or phase drifted"
            )
        if sorted({step.kind for step in steps}) != case[
            "source_step_kinds"
        ]:
            raise RuntimeError(f"{name}: source-step coverage drifted")
        results[name] = {
            "status": "passed",
            "terminal_status": primary["terminal_status"],
            "callback_state": primary["callback_state"],
            "callback_count": correspondence["callback_count"],
            "callback_schedule_equal": True,
            "phase_sequence_equal": True,
            "permutation_retained": (
                sorted(primary["sequence"])
                == sorted(case["spec"]["sequence"])
            ),
        }
    required = {
        "configuration-heapsort-size",
        "configuration-heapsort-16-bit",
        "fallback-small-sort-and-recursion",
        "network-small-sort-sort13-merge",
        "general-small-sort-scratch-merge",
        "general-small-sort-sort8-direct",
        "network-small-sort-sort9-direct",
        "general-small-sort-presorted-one-direct",
        "recursive-pivot",
        "hoare-partition",
        "cyclic-unroll-one-partition",
        "lomuto-simple-direct",
        "imbalance-fallback-direct",
        "duplicate-class-ancestor-pivot",
        "insertion-copy-on-drop-panic",
        "general-small-sort-merge-restoration",
        "general-small-sort-scratch-unwind-restoration",
        "cyclic-gap-guard-restoration",
        "hoare-gap-guard-restoration",
    }
    missing = required - results.keys()
    if missing:
        raise RuntimeError(f"required witnesses are missing: {sorted(missing)}")
    return {
        "status": "passed",
        "witness_count": len(results),
        "field_complete_correspondence": True,
        "cases": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", required=True, type=Path)
    arguments = parser.parse_args()
    print(json.dumps(replay(arguments.witness), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
