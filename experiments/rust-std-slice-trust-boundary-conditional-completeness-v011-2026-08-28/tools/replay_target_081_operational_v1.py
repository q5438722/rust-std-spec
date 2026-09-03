#!/usr/bin/env python3
"""Independent replay for target-081 operational-v1 witnesses."""

from __future__ import annotations

import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_081_operational_witness_v1 as witnesses


def replay(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if payload["target"] != "core::slice::sort_unstable_by":
        raise ValueError("target-081 witness target drifted")
    if payload["input_order"] != "81":
        raise ValueError("target-081 witness order drifted")
    cases: dict[str, Any] = {}
    for name, retained in payload["cases"].items():
        primary, independent, correspondence = witnesses.execute_spec(
            retained["spec"]
        )
        if primary != retained["primary"]:
            raise ValueError(f"{name}: primary result drifted")
        if independent != retained["independent"]:
            raise ValueError(f"{name}: independent result drifted")
        if correspondence != retained["correspondence"]:
            raise ValueError(f"{name}: correspondence record drifted")
        if not all(
            (
                correspondence["field_complete"],
                correspondence["adapter_schedule_equal"],
                correspondence["adapter_evaluations_are_single"],
                correspondence["observable_interior_state_equal"],
                correspondence["permutation_retained"],
            )
        ):
            raise ValueError(f"{name}: witness is not field-complete")
        cases[name] = correspondence
    statuses = {
        retained["primary"]["terminal_status"]
        for retained in payload["cases"].values()
    }
    if statuses != {"modeled-normal", "modeled-panic", "modeled-abort"}:
        raise ValueError("normal, panic, and abort coverage is required")
    return {
        "status": "passed",
        "target": payload["target"],
        "input_order": payload["input_order"],
        "witness_count": len(cases),
        "field_complete_correspondence": True,
        "single_callback_evaluation": True,
        "observable_interior_state_correspondence": True,
        "terminal_statuses": sorted(statuses),
        "witness_sha256": sha256(path.read_bytes()).hexdigest(),
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", type=Path, required=True)
    arguments = parser.parse_args()
    print(json.dumps(replay(arguments.witness), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
