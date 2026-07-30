#!/usr/bin/env python3
"""Merge exhaustive Rust source-resolution audit shards."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "surrogate-audit"
INPUTS = (
    REPORT / "resolved-core-primitives.json",
    REPORT / "resolved-core-generics.json",
    REPORT / "resolved-alloc-impls.json",
)


def main() -> None:
    records = []
    for path in INPUTS:
        payload = json.loads(path.read_text())
        for record in payload["records"]:
            record = dict(record)
            if (
                record["proof_admissibility"] == "wrong_or_missing_target"
                and record["source_kind"] != "non_std_target_absent"
                and record["body_fidelity"] == "alternate_implementation"
            ):
                record["proof_admissibility"] = "ordinary_acyclic"
            records.append(record)

    ids = [record["id"] for record in records]
    assert len(records) == 104, len(records)
    assert len(set(ids)) == len(ids), "duplicate source-resolution records"

    body = Counter(record["body_fidelity"] for record in records)
    admissibility = Counter(record["proof_admissibility"] for record in records)
    strict = sum(
        record["body_fidelity"] in {"exact_body", "mechanical_desugaring"}
        and record["proof_admissibility"] == "ordinary_acyclic"
        for record in records
    )
    known_invalid = sum(
        record["proof_admissibility"]
        in {
            "peer_cycle",
            "target_equivalent_axiom",
            "wrong_or_missing_target",
        }
        or record["body_fidelity"]
        in {
            "alternate_implementation",
            "circular_or_target_axiom",
            "ambiguous_mapping",
        }
        for record in records
    )
    unresolved = len(records) - strict - known_invalid
    summary = {
        "records": len(records),
        "body_fidelity": dict(body),
        "proof_admissibility": dict(admissibility),
        "strict_faithful_admissible": strict,
        "known_mismatch_or_inadmissible": known_invalid,
        "source_unresolved": unresolved,
    }
    assert summary["strict_faithful_admissible"] == 60
    assert summary["known_mismatch_or_inadmissible"] == 43
    assert summary["source_unresolved"] == 1

    (REPORT / "source-resolution-overrides.json").write_text(
        json.dumps(
            {
                "summary": summary,
                "records": sorted(records, key=lambda record: record["id"]),
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
