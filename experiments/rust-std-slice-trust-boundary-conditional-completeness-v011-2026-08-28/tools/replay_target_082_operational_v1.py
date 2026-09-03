#!/usr/bin/env python3
"""Replay target-082 paired operational witnesses."""

from __future__ import annotations

import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_082_operational_v1 as model
import target_082_operational_witness_v1 as witnesses


def replay(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text())
    expected = witnesses.witness_payload()
    if payload != expected:
        raise ValueError("target-082 witness bytes do not replay exactly")
    cases = payload["cases"]
    if not cases:
        raise ValueError("target-082 witness set is empty")
    for name, case in cases.items():
        correspondence = case["correspondence"]
        if not all(
            correspondence[key]
            for key in (
                "field_complete",
                "adapter_events_equal",
                "normal_panic_abort_equal",
                "full_observable_state_equal",
                "source_ordered_temporaries",
                "permutation_retained",
            )
        ):
            raise ValueError(f"{name}: correspondence replay failed")
    statuses = {
        case["primary"]["terminal_status"] for case in cases.values()
    }
    if statuses != {model.NORMAL, model.PANIC, model.ABORT}:
        raise ValueError("target-082 terminal coverage changed")
    required = {
        "duplicate-equal-owned-keys",
        "key-left-panic-prefix",
        "key-right-panic-left-unwind-drop",
        "ord-lt-panic-right-then-left-unwind-drop",
        "right-key-drop-panic-left-unwind-drop",
        "ord-panic-right-drop-double-panic-abort",
        "key-panic-f-drop-double-panic-abort",
        "callback-and-element-interior-mutation",
    }
    if not required <= set(cases):
        raise ValueError("target-082 mandatory witness coverage is missing")
    return {
        "status": "passed",
        "target": payload["target"],
        "input_order": payload["input_order"],
        "case_count": len(cases),
        "terminal_statuses": sorted(statuses),
        "field_complete": True,
        "witness_sha256": sha256(path.read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.witness), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
