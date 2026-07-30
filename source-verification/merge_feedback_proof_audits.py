#!/usr/bin/env python3
"""Merge strict fidelity audit shards for feedback proof variants."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CAMPAIGN = ROOT / "feedback-proof"
SHARDS = (
    CAMPAIGN / "audit-result-option.json",
    CAMPAIGN / "audit-memory-slice.json",
    CAMPAIGN / "audit-cmp-ops.json",
    CAMPAIGN / "audit-alloc-std.json",
)


def main() -> None:
    records = []
    shard_summaries = {}
    for path in SHARDS:
        payload = json.loads(path.read_text())
        records.extend(payload["records"])
        shard_summaries[path.name] = payload["summary"]

    ids = [record["variant_id"] for record in records]
    assert len(ids) == 201
    assert len(set(ids)) == len(ids)

    run = json.loads(
        (CAMPAIGN / "runs" / "full-gpt56sol" / "summary.json").read_text()
    )
    proved = {
        result["id"]
        for result in run["results"]
        if result.get("status") == "proved"
    }
    assert set(ids) == proved
    verdicts = Counter(record["strict_verdict"] for record in records)
    body = Counter(record["body_fidelity"] for record in records)
    admissibility = Counter(record["proof_admissibility"] for record in records)
    summary = {
        "passing_variants": len(records),
        "strict_verdicts": dict(verdicts),
        "body_fidelity": dict(body),
        "proof_admissibility": dict(admissibility),
        "shards": shard_summaries,
    }
    assert verdicts == {
        "strict_faithful_admissible": 146,
        "known_mismatch_or_inadmissible": 55,
    }
    (CAMPAIGN / "audit-passing.json").write_text(
        json.dumps(
            {
                "summary": summary,
                "records": sorted(records, key=lambda record: record["variant_id"]),
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
