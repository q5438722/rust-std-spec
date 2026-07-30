#!/usr/bin/env python3
"""Reclassify rerun determinism compiler errors as explicit checker limitations."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUMMARY = ROOT / "determinism-all" / "summary.json"

GENERIC_OUTPUT = {
    "std_specs__convert.rs__L48__T__as__Into__U__into",
    "std_specs__convert.rs__L101__T__as__TryInto__U__try_into",
}

UNSIZED_MUTABLE_STATE = {
    "std_specs__slice.rs__L179__T__first_mut",
    "std_specs__slice.rs__L187__T__last_mut",
    "std_specs__slice.rs__L203__T__split_at_mut",
    "std_specs__slice.rs__L213__T__copy_from_slice",
    "std_specs__slice.rs__L243__T__copy_within__R",
}


def main() -> None:
    payload = json.loads(SUMMARY.read_text())
    changed = []
    for result in payload["results"]:
        if result["id"] in GENERIC_OUTPUT:
            assert result.get("status") == "verus_error"
            result["original_status"] = result["status"]
            result["status"] = "unsupported_generic_output_view"
            result["rerun_attempted"] = True
            result["limitation"] = (
                "The generic output type has neither a universal View nor a "
                "generic executable equality available to the checker."
            )
            changed.append(result["id"])
        elif result["id"] in UNSIZED_MUTABLE_STATE:
            assert result.get("status") == "verus_error"
            result["original_status"] = result["status"]
            result["status"] = "unsupported_unsized_mutable_state"
            result["rerun_attempted"] = True
            result["limitation"] = (
                "The checker cannot compare an unsized [T] post-state with "
                "extensional equality; rerunning with unsized_fn_params reaches "
                "the Sized bound in ext_equal."
            )
            changed.append(result["id"])
    assert len(changed) == 7, changed
    SUMMARY.write_text(json.dumps(payload, indent=2) + "\n")
    for result in payload["results"]:
        target_summary = ROOT / "determinism-all" / "targets" / result["id"] / "summary.json"
        if result["id"] in changed:
            target_summary.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"reclassified": changed}, indent=2))


if __name__ == "__main__":
    main()
